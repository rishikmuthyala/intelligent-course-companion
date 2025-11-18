"""
Demo Setup Script for AI Course Companion
Creates sample course data and processes it into the vector database
"""

import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add scripts to path
sys.path.append(str(Path(__file__).parent / "scripts"))

from scripts.rag_pipeline import RAGPipeline


def setup_demo_data():
    """Set up demo course data"""
    
    print("\n" + "="*70)
    print("🎓 AI COURSE COMPANION - DEMO SETUP")
    print("="*70)
    
    # Create transcripts directory structure
    transcripts_dir = Path("./transcripts")
    demo_data_dir = Path("./demo_data")
    
    print("\n📂 Setting up course directories...")
    
    # Course 1: CS 446 - Search Engines
    cs446_dir = transcripts_dir / "12345_cs446_search_engines"
    cs446_dir.mkdir(parents=True, exist_ok=True)
    
    # Course 2: CS 360 - Computer Systems  
    cs360_dir = transcripts_dir / "12346_cs360_computer_systems"
    cs360_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"   ✅ Created: {cs446_dir}")
    print(f"   ✅ Created: {cs360_dir}")
    
    # Copy demo transcripts
    print("\n📄 Copying demo transcripts...")
    
    demo_files = {
        "CS446_Lecture_1.txt": cs446_dir / "Lecture_1_Introduction_to_IR.txt",
        "CS446_Lecture_2.txt": cs446_dir / "Lecture_2_Web_Crawling.txt",
        "CS360_Lecture_1.txt": cs360_dir / "Lecture_1_Operating_Systems.txt",
    }
    
    for source, dest in demo_files.items():
        source_path = demo_data_dir / source
        if source_path.exists():
            shutil.copy(source_path, dest)
            print(f"   ✅ Copied: {source} → {dest.name}")
        else:
            print(f"   ⚠️  Missing: {source}")
    
    return True


def process_demo_data():
    """Process demo data into vector database"""
    
    print("\n" + "="*70)
    print("🔄 PROCESSING TRANSCRIPTS INTO VECTOR DATABASE")
    print("="*70)
    
    try:
        # Initialize RAG pipeline
        print("\n→ Initializing RAG Pipeline...")
        pipeline = RAGPipeline()
        
        # Process and store all transcripts
        print("→ Processing transcripts...")
        result = pipeline.process_and_store_transcripts()
        
        print("\n" + "="*70)
        print("✅ PROCESSING COMPLETE")
        print("="*70)
        print(f"   Files processed: {result.get('files_processed', 0)}")
        print(f"   Chunks created: {result.get('chunks_created', 0)}")
        print(f"   Courses: {result.get('courses_processed', 0)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error processing data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_demo_queries():
    """Test some demo queries"""
    
    print("\n" + "="*70)
    print("🧪 TESTING DEMO QUERIES")
    print("="*70)
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
        
        pipeline = RAGPipeline()
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        test_queries = [
            ("12345_cs446_search_engines", "What is PageRank and how does it work?"),
            ("12346_cs360_computer_systems", "Explain the difference between processes and threads"),
        ]
        
        for course_id, question in test_queries:
            print(f"\n📚 Course: {course_id}")
            print(f"❓ Question: {question}")
            
            # Get context
            context_chunks = pipeline.query(
                course_id=course_id,
                search_query=question,
                num_results=3
            )
            
            if not context_chunks:
                print("   ❌ No context found")
                continue
            
            print(f"   ✅ Found {len(context_chunks)} relevant chunks")
            
            # Generate answer
            context = "\n\n---\n\n".join(context_chunks)
            
            system_prompt = """You are an AI teaching assistant. Answer based on the course transcript context provided. Be clear and concise."""
            
            user_prompt = f"""Context from lecture:
{context}

Question: {question}

Provide a clear, concise answer:"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = llm.invoke(messages)
            
            print(f"\n💡 Answer:")
            print(f"   {response.content[:200]}...")
            print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Query test error: {e}")
        return False


def show_demo_info():
    """Show information about the demo"""
    
    print("\n" + "="*70)
    print("🎉 DEMO READY!")
    print("="*70)
    
    print("\n📚 Available Courses:")
    print("   • CS 446 - Search Engines (ID: 12345_cs446_search_engines)")
    print("     - Lecture 1: Introduction to Information Retrieval")
    print("     - Lecture 2: Web Crawling and Graph Algorithms")
    print()
    print("   • CS 360 - Computer Systems (ID: 12346_cs360_computer_systems)")
    print("     - Lecture 1: Introduction to Operating Systems")
    
    print("\n🚀 Next Steps:")
    print("   1. Start the backend:")
    print("      cd backend")
    print("      python3 -m uvicorn main:app --reload")
    print()
    print("   2. Start the frontend (in a new terminal):")
    print("      cd frontend")
    print("      npm run dev")
    print()
    print("   3. Open http://localhost:5173 in your browser")
    print()
    print("   4. Try these questions:")
    print("      • What is PageRank?")
    print("      • How does a web crawler work?")
    print("      • What's the difference between processes and threads?")
    print("      • Explain deadlock in operating systems")
    
    print("\n📸 For LinkedIn Demo:")
    print("   1. Show the frontend interface")
    print("   2. Ask a question about search engines or operating systems")
    print("   3. Show the AI-generated answer with source context")
    print("   4. Demonstrate querying different courses")
    
    print("\n" + "="*70)


def main():
    """Main demo setup"""
    
    print("\n🎓 Setting up AI Course Companion Demo...")
    
    # Check if OpenAI key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not set in .env file")
        print("   Please add your OpenAI API key to continue")
        return False
    
    # Setup demo data
    if not setup_demo_data():
        print("\n❌ Failed to setup demo data")
        return False
    
    # Process into vector DB
    if not process_demo_data():
        print("\n❌ Failed to process demo data")
        return False
    
    # Test queries
    if not test_demo_queries():
        print("\n⚠️  Query tests failed, but demo data is ready")
    
    # Show info
    show_demo_info()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

