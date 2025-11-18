"""
RAG (Retrieval-Augmented Generation) pipeline for processing transcripts.

This module handles:
- Loading transcript files
- Chunking documents
- Creating embeddings
- Storing in ChromaDB
- Querying the vector database
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

# ChromaDB imports
import chromadb
from chromadb.config import Settings

# LangChain imports
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()


class RAGPipeline:
    """Main class for managing the RAG pipeline."""
    
    def __init__(self):
        """Initialize the RAG pipeline with necessary components."""
        print("Initializing RAG Pipeline...")
        
        # Load API keys and configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self.transcripts_dir = Path("./transcripts")
        
        # Initialize OpenAI Embeddings
        print("   → Initializing OpenAI Embeddings (text-embedding-3-small)...")
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=self.openai_api_key
        )
        
        # Initialize LLM for Q&A (will be used later)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=self.openai_api_key
        )
        
        # Initialize ChromaDB persistent client
        print(f"   → Initializing ChromaDB (persist_directory: {self.chroma_persist_dir})...")
        self.chroma_client = chromadb.PersistentClient(
            path=self.chroma_persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Collection name for storing all course transcripts
        self.collection_name = "course_transcripts"
        
        # Initialize or get existing collection
        try:
            self.collection = self.chroma_client.get_collection(name=self.collection_name)
            print(f"   → Using existing ChromaDB collection: {self.collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Course lecture transcripts with embeddings"}
            )
            print(f"   → Created new ChromaDB collection: {self.collection_name}")
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            is_separator_regex=False
        )
        
        # Track processed files to avoid reprocessing
        self.processed_files_path = Path(self.chroma_persist_dir) / "processed_files.json"
        
        print("   ✅ RAG Pipeline initialized successfully!")
    
    def process_and_store_transcripts(self) -> Dict[str, Any]:
        """
        Main function to process all transcripts and store in ChromaDB.
        
        Returns:
            Dictionary with processing statistics
        """
        print("\n" + "=" * 60)
        print("Starting Transcript Processing Pipeline")
        print("=" * 60)
        
        result = {
            "success": False,
            "files_processed": 0,
            "chunks_created": 0,
            "courses_processed": [],
            "errors": []
        }
        
        # Check if transcripts directory exists
        if not self.transcripts_dir.exists():
            print(f"❌ Transcripts directory not found: {self.transcripts_dir}")
            result["errors"].append(f"Transcripts directory not found: {self.transcripts_dir}")
            return result
        
        # Get previously processed files
        processed_files = self.get_processed_files()
        print(f"\n→ Previously processed files: {len(processed_files)}")
        
        # Find all transcript files
        transcript_files = list(self.transcripts_dir.glob("*/*.txt"))
        print(f"→ Found {len(transcript_files)} total transcript file(s)")
        
        # Group files by course
        files_by_course = {}
        for file_path in transcript_files:
            # Skip if already processed
            if str(file_path) in processed_files:
                continue
            
            # Extract course_id from path (transcripts/course_id/file.txt)
            course_id = file_path.parent.name
            if course_id not in files_by_course:
                files_by_course[course_id] = []
            files_by_course[course_id].append(file_path)
        
        if not files_by_course:
            print("\n✅ All files are already processed. No new transcripts to process.")
            result["success"] = True
            return result
        
        print(f"\n→ Processing {sum(len(files) for files in files_by_course.values())} new file(s) across {len(files_by_course)} course(s)")
        
        # Process each course's transcripts
        for course_id, course_files in files_by_course.items():
            print(f"\n📚 Processing Course ID: {course_id}")
            print(f"   Files to process: {len(course_files)}")
            
            course_chunks_total = 0
            
            for file_idx, file_path in enumerate(course_files, 1):
                try:
                    print(f"\n   [{file_idx}/{len(course_files)}] Processing: {file_path.name}")
                    
                    # Load the transcript file
                    documents = self.load_transcript(file_path)
                    if not documents:
                        print(f"      ⚠️  No content loaded from {file_path.name}")
                        continue
                    
                    print(f"      → Loaded document with {len(documents[0].page_content)} characters")
                    
                    # Add course metadata to documents
                    for doc in documents:
                        doc.metadata = {
                            "course_id": course_id,
                            "file_name": file_path.name,
                            "file_path": str(file_path),
                            "lecture_title": file_path.stem  # filename without extension
                        }
                    
                    # Chunk the documents
                    chunks = self.chunk_documents(documents)
                    print(f"      → Created {len(chunks)} chunks")
                    
                    # Store chunks in ChromaDB
                    self.store_in_chromadb(chunks, course_id)
                    
                    # Mark file as processed
                    self.mark_file_processed(str(file_path))
                    
                    # Update statistics
                    result["files_processed"] += 1
                    course_chunks_total += len(chunks)
                    result["chunks_created"] += len(chunks)
                    
                    print(f"      ✓ Successfully processed and stored {len(chunks)} chunks")
                    
                except Exception as e:
                    error_msg = f"Error processing {file_path.name}: {str(e)}"
                    print(f"      ❌ {error_msg}")
                    result["errors"].append(error_msg)
                    continue
            
            if course_chunks_total > 0:
                result["courses_processed"].append({
                    "course_id": course_id,
                    "files": len(course_files),
                    "chunks": course_chunks_total
                })
                print(f"\n   ✅ Course {course_id} complete: {len(course_files)} files, {course_chunks_total} chunks")
        
        result["success"] = result["files_processed"] > 0
        
        # Print summary
        print("\n" + "=" * 60)
        print("Processing Summary")
        print("=" * 60)
        print(f"✓ Files processed: {result['files_processed']}")
        print(f"✓ Total chunks created: {result['chunks_created']}")
        print(f"✓ Courses processed: {len(result['courses_processed'])}")
        if result["errors"]:
            print(f"⚠️  Errors encountered: {len(result['errors'])}")
        
        return result
    
    def load_transcript(self, file_path: Path) -> List[Document]:
        """
        Load a single transcript file.
        
        Args:
            file_path: Path to the transcript file
        
        Returns:
            List of LangChain Document objects
        """
        try:
            # Use TextLoader to load the file
            loader = TextLoader(str(file_path), encoding='utf-8')
            documents = loader.load()
            return documents
        except Exception as e:
            print(f"      ❌ Error loading file {file_path}: {str(e)}")
            # Try with different encoding if UTF-8 fails
            try:
                loader = TextLoader(str(file_path), encoding='latin-1')
                documents = loader.load()
                return documents
            except:
                return []
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks.
        
        Args:
            documents: List of documents to chunk
        
        Returns:
            List of chunked documents
        """
        # Use the text splitter to create chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Preserve and enhance metadata for each chunk
        for i, chunk in enumerate(chunks):
            # Add chunk-specific metadata
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)
            chunk.metadata["chunk_size"] = len(chunk.page_content)
        return chunks
    
    def store_in_chromadb(self, chunks: List[Document], course_id: str):
        """
        Store document chunks in ChromaDB with course metadata.
        
        Args:
            chunks: Document chunks to store
            course_id: Course identifier for metadata
        """
        if not chunks:
            return
        
        # Prepare data for ChromaDB
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # Generate unique IDs for each chunk
        # Format: course_id_filename_chunkindex
        ids = []
        for chunk in chunks:
            file_name = chunk.metadata.get("file_name", "unknown").replace(".txt", "")
            chunk_idx = chunk.metadata.get("chunk_index", 0)
            chunk_id = f"{course_id}_{file_name}_{chunk_idx}"
            ids.append(chunk_id)
        
        # Generate embeddings using OpenAI
        embeddings_list = self.embeddings.embed_documents(texts)
        
        # Store in ChromaDB collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings_list,
            documents=texts,
            metadatas=metadatas
        )
    
    def query(self, course_id: str, search_query: str, num_results: int = 3) -> List[str]:
        """
        Query a specific course's content using similarity search.
        
        Args:
            course_id: Course to query
            search_query: Search query/question
            num_results: Number of results to return (default: 3)
        
        Returns:
            List of the most relevant text chunks
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embeddings.embed_query(search_query)
            
            # Perform similarity search with metadata filtering
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=num_results,
                where={"course_id": course_id}  # Filter by course_id
            )
            
            # Extract and return the text chunks
            if results and results['documents'] and results['documents'][0]:
                return results['documents'][0]
            else:
                return []
                
        except Exception as e:
            print(f"Error querying course {course_id}: {str(e)}")
            return []
    
    def query_course(self, course_id: str, question: str) -> Dict[str, Any]:
        """
        Query a specific course's content with full RAG pipeline.
        
        Args:
            course_id: Course to query
            question: User's question
        
        Returns:
            Dictionary with answer and source chunks
        """
        # Use the simpler query method for now
        chunks = self.query(course_id, question, num_results=5)
        
        return {
            "course_id": course_id,
            "question": question,
            "relevant_chunks": chunks,
            "num_chunks": len(chunks)
        }
    
    def get_processed_files(self) -> set:
        """
        Get set of already processed files.
        
        Returns:
            Set of processed file paths
        """
        if self.processed_files_path.exists():
            try:
                with open(self.processed_files_path, 'r') as f:
                    data = json.load(f)
                    return set(data.get("processed_files", []))
            except:
                # Fallback for old format or corrupted file
                return set()
        return set()
    
    def mark_file_processed(self, file_path: str):
        """
        Mark a file as processed.
        
        Args:
            file_path: Path to the processed file
        """
        # Ensure directory exists
        self.processed_files_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get current processed files
        processed = self.get_processed_files()
        processed.add(file_path)
        
        # Save updated list
        with open(self.processed_files_path, 'w') as f:
            json.dump({
                "processed_files": list(processed),
                "last_updated": datetime.now().isoformat()
            }, f, indent=2)


# Custom prompt template for course-specific Q&A
COURSE_QA_PROMPT = PromptTemplate(
    template="""You are an AI assistant for a specific course. Answer the question based ONLY on the provided course materials.
    
    If the answer cannot be found in the course materials, say "I cannot find information about this in the course materials."
    
    Course materials:
    {context}
    
    Question: {question}
    
    Answer:""",
    input_variables=["context", "question"]
)


if __name__ == "__main__":
    # Test the RAG pipeline independently
    import sys
    
    try:
        pipeline = RAGPipeline()
        
        # Process transcripts
        print("\n📄 Processing transcripts...")
        result = pipeline.process_and_store_transcripts()
        
        # Test query functionality if processing was successful
        if result["success"] and result["courses_processed"]:
            print("\n" + "=" * 60)
            print("Testing Query Functionality")
            print("=" * 60)
            
            # Test with the first processed course
            test_course = result["courses_processed"][0]
            course_id = test_course["course_id"]
            
            # Example queries
            test_queries = [
                "What are the main topics covered in this course?",
                "What was discussed in the first lecture?",
                "Explain the key concepts"
            ]
            
            print(f"\n🔍 Testing queries for Course ID: {course_id}")
            
            for query in test_queries[:1]:  # Test just one query for now
                print(f"\nQuery: {query}")
                results = pipeline.query(course_id, query, num_results=3)
                
                if results:
                    print(f"Found {len(results)} relevant chunks:")
                    for i, chunk in enumerate(results, 1):
                        preview = chunk[:200] + "..." if len(chunk) > 200 else chunk
                        print(f"\n  Chunk {i}: {preview}")
                else:
                    print("No results found for this query.")
        
        print("\n✅ RAG Pipeline test complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
