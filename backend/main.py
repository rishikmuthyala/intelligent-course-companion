"""
Main FastAPI server for the Intelligent Course Companion MVP.

This module provides the REST API endpoints for:
- Syncing Canvas course transcripts
- Querying course content using RAG
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent / "scripts"))

# Import our custom modules
from scripts.advanced_scraper import AdvancedCanvasScraper
from scripts.rag_pipeline import RAGPipeline

# LangChain imports for answer synthesis
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Course Companion API",
    description="Backend API for AI-powered course Q&A",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    source_chunks: List[str] = []
    course_id: str
    question: str


class SyncResponse(BaseModel):
    status: str
    message: str
    details: Optional[str] = None


class SyncStatus(BaseModel):
    is_running: bool
    last_sync: Optional[str] = None
    courses_found: int = 0
    transcripts_downloaded: int = 0
    files_processed: int = 0


class TranscriptRequest(BaseModel):
    transcript: str


class TranscriptSummary(BaseModel):
    summary: str
    detailed_notes: str
    key_points: List[str] = []
    topics: List[str] = []
    important_concepts: List[str] = []
    study_tips: List[str] = []
    practice_questions: List[str] = []
    session_id: str  # For follow-up Q&A


class FollowUpRequest(BaseModel):
    session_id: str
    question: str


# Global state for tracking sync status
sync_status = {
    "is_running": False,
    "last_sync": None,
    "last_result": None
}


# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Intelligent Course Companion API"}


async def run_sync_pipeline():
    """
    Background task to run the full sync pipeline.
    This runs: scraping -> RAG processing -> storage
    """
    global sync_status
    from datetime import datetime
    
    try:
        print("\n" + "=" * 60)
        print("STARTING BACKGROUND SYNC PIPELINE")
        print("=" * 60)
        
        sync_status["is_running"] = True
        sync_status["last_sync"] = datetime.now().isoformat()
        
        # Step 1: Run the advanced scraper
        print("\n[Step 1/2] Running Advanced Canvas Scraper...")
        canvas_username = os.getenv("CANVAS_USERNAME", "")
        canvas_password = os.getenv("CANVAS_PASSWORD", "")
        
        if not canvas_username or not canvas_password:
            raise ValueError("Canvas credentials not found in environment variables")
        
        # Initialize and run advanced scraper
        scraper = AdvancedCanvasScraper(canvas_username, canvas_password)
        scraper_result = await scraper.scrape_all_courses()
        
        print(f"\nScraper Result: {scraper_result}")
        sync_status["last_result"] = {
            "scraper": scraper_result,
            "rag": None
        }
        
        # Step 2: Run the RAG pipeline
        print("\n[Step 2/2] Running RAG Pipeline...")
        pipeline = RAGPipeline()
        rag_result = pipeline.process_and_store_transcripts()
        
        print(f"\nRAG Result: {rag_result}")
        sync_status["last_result"]["rag"] = rag_result
        
        print("\n" + "=" * 60)
        print("SYNC PIPELINE COMPLETED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Sync pipeline error: {str(e)}")
        sync_status["last_result"] = {"error": str(e)}
    
    finally:
        sync_status["is_running"] = False


# Sync endpoint - triggers scraping and processing
@app.post("/sync", response_model=SyncResponse)
async def sync_courses(background_tasks: BackgroundTasks):
    """
    Trigger the scraper to download new transcripts and process them.
    This runs the full pipeline: scraping -> RAG processing -> storage.
    """
    # Check if sync is already running
    if sync_status["is_running"]:
        return SyncResponse(
            status="already_running",
            message="A sync operation is already in progress. Please wait for it to complete.",
            details=f"Started at: {sync_status['last_sync']}"
        )
    
    # Start the sync pipeline in the background
    background_tasks.add_task(run_sync_pipeline)
    
    return SyncResponse(
        status="started",
        message="Data synchronization started in the background.",
        details="The sync process will download new transcripts and process them into the vector database. This may take several minutes."
    )


# Add a status endpoint to check sync progress
@app.get("/sync/status", response_model=SyncStatus)
async def get_sync_status():
    """Get the current status of the sync operation."""
    status = SyncStatus(
        is_running=sync_status["is_running"],
        last_sync=sync_status["last_sync"]
    )
    
    # Add statistics from last result if available
    if sync_status["last_result"]:
        if "scraper" in sync_status["last_result"]:
            scraper_data = sync_status["last_result"]["scraper"]
            status.courses_found = scraper_data.get("courses_found", 0)
            status.transcripts_downloaded = scraper_data.get("transcripts_downloaded", 0)
        
        if "rag" in sync_status["last_result"]:
            rag_data = sync_status["last_result"]["rag"]
            status.files_processed = rag_data.get("files_processed", 0)
    
    return status


# List available courses endpoint
@app.get("/courses")
async def list_courses():
    """
    List all available courses that have been synced.
    Returns course IDs and names from the last sync.
    """
    courses = []
    
    # Check if we have sync results with course data
    if sync_status["last_result"] and "scraper" in sync_status["last_result"]:
        scraper_data = sync_status["last_result"]["scraper"]
        if "courses" in scraper_data:
            courses = scraper_data["courses"]
    
    # If no courses from sync status, check the transcripts directory
    if not courses:
        transcripts_dir = Path("./transcripts")
        if transcripts_dir.exists():
            course_dirs = [d for d in transcripts_dir.iterdir() if d.is_dir()]
            courses = [{"id": d.name, "name": f"Course {d.name}"} for d in course_dirs]
    
    return {
        "courses": courses,
        "total": len(courses),
        "message": "Run /sync to update course list" if not courses else None
    }


# Query endpoint - Q&A for specific course
@app.post("/query/{course_id}", response_model=QueryResponse)
async def query_course(course_id: str, request: QueryRequest):
    """
    Query a specific course's content using RAG.
    
    Args:
        course_id: The Canvas course ID to query
        request: Contains the user's question
    
    Returns:
        QueryResponse with the AI-generated answer based on course materials
    """
    try:
        # Validate input
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        if not course_id or not course_id.strip():
            raise HTTPException(status_code=400, detail="Course ID cannot be empty")
        
        print(f"\n📚 Query Request - Course: {course_id}, Question: {request.question}")
        
        # Step 1: Initialize RAG pipeline
        pipeline = RAGPipeline()
        
        # Step 2: Retrieve relevant context chunks from ChromaDB
        print("   → Retrieving relevant context from vector database...")
        context_chunks = pipeline.query(
            course_id=course_id,
            search_query=request.question,
            num_results=5  # Get top 5 most relevant chunks
        )
        
        if not context_chunks:
            print("   ⚠️  No relevant context found for this course")
            return QueryResponse(
                answer="I couldn't find any relevant information about this topic in the course materials. This could mean the course hasn't been synced yet, or the topic isn't covered in the available transcripts.",
                source_chunks=[],
                course_id=course_id,
                question=request.question
            )
        
        print(f"   → Found {len(context_chunks)} relevant chunks")
        
        # Step 3: Synthesize answer using OpenAI
        print("   → Synthesizing answer with GPT-4o-mini...")
        
        # Combine context chunks into a single context string
        context = "\n\n---\n\n".join(context_chunks)
        
        # Create the prompt for answer synthesis
        system_prompt = """You are an AI assistant helping students understand course material. 
        Answer questions based EXCLUSIVELY on the provided course transcript context.
        
        Important instructions:
        1. Only use information from the provided context
        2. If the answer is not in the context, say "I cannot find information about this in the course materials"
        3. Be clear, concise, and helpful
        4. If relevant, quote or paraphrase specific parts of the context
        5. Do not make up information or use external knowledge"""
        
        user_prompt = f"""Answer the following question based exclusively on the provided context from the course transcripts.
        
Context from course materials:
{context}

Question: {request.question}

Answer:"""
        
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Generate the answer
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        answer = response.content
        
        print("   ✅ Answer generated successfully")
        
        # Return the response
        return QueryResponse(
            answer=answer,
            source_chunks=context_chunks[:3],  # Return top 3 chunks as sources
            course_id=course_id,
            question=request.question
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"   ❌ Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your question: {str(e)}"
        )


# Global storage for transcript sessions (in production, use Redis or database)
transcript_sessions = {}


# Summarize endpoint - Enhanced AI-powered transcript summarization with RAG
@app.post("/summarize", response_model=TranscriptSummary)
async def summarize_transcript(request: TranscriptRequest):
    """
    Generate comprehensive AI-powered notes from a lecture transcript.
    Uses RAG to enable follow-up questions.
    
    Args:
        request: Contains the transcript text to summarize
    
    Returns:
        TranscriptSummary with detailed notes, study guide, and session ID for Q&A
    """
    try:
        # Validate input
        if not request.transcript or not request.transcript.strip():
            raise HTTPException(status_code=400, detail="Transcript cannot be empty")
        
        transcript = request.transcript
        word_count = len(transcript.split())
        
        print(f"\n📝 Enhanced Summarization Request - Word count: {word_count}")
        
        # Create session ID for follow-up questions
        import uuid
        session_id = str(uuid.uuid4())
        
        # Store transcript in session for RAG-based Q&A
        transcript_sessions[session_id] = {
            "transcript": transcript,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        
        # Limit transcript for prompts but keep full version for Q&A
        max_words = 4000
        transcript_for_prompts = transcript
        if word_count > max_words:
            transcript_words = transcript.split()[:max_words]
            transcript_for_prompts = ' '.join(transcript_words)
            print(f"   → Using first {max_words} words for analysis")
        
        # Initialize ChatOpenAI with higher quality model
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,  # Lower for more consistent educational content
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Step 1: Generate Quick Summary
        print("   → Generating executive summary...")
        summary_prompt = f"""Provide a brief 2-3 paragraph executive summary of this lecture.

Transcript:
{transcript_for_prompts}

Summary:"""
        
        summary_response = llm.invoke([
            SystemMessage(content="You are an expert educator. Create clear, engaging summaries."),
            HumanMessage(content=summary_prompt)
        ])
        summary = summary_response.content.strip()
        
        # Step 2: Generate Detailed Notes
        print("   → Generating detailed study notes...")
        notes_prompt = f"""Create comprehensive study notes from this lecture transcript. 

Requirements:
- Organize by major sections/topics
- Include detailed explanations of concepts
- Add examples where mentioned
- Explain technical terms
- Write in a clear, student-friendly style
- Use bullet points and headers for organization
- Aim for completeness - these are the student's primary study resource

Transcript:
{transcript_for_prompts}

Detailed Study Notes:"""
        
        notes_response = llm.invoke([
            SystemMessage(content="You are an expert note-taker and educator. Create detailed, comprehensive notes that help students deeply understand the material."),
            HumanMessage(content=notes_prompt)
        ])
        detailed_notes = notes_response.content.strip()
        
        # Step 3: Extract Key Points
        print("   → Identifying key takeaways...")
        keypoints_prompt = f"""Extract the 7 most important key points from this lecture. These should be the critical concepts a student MUST remember.

Transcript:
{transcript_for_prompts}

Return ONLY the 7 key points, one per line:"""
        
        keypoints_response = llm.invoke([
            SystemMessage(content="You are an expert at identifying critical learning objectives."),
            HumanMessage(content=keypoints_prompt)
        ])
        
        key_points = [
            line.strip().lstrip('•-*0123456789.').strip() 
            for line in keypoints_response.content.strip().split('\n') 
            if line.strip()
        ][:7]
        
        # Step 4: Identify Important Concepts
        print("   → Extracting important concepts...")
        concepts_prompt = f"""List 5-8 important concepts or terms from this lecture that students should deeply understand.

Transcript:
{transcript_for_prompts}

Return as comma-separated list:"""
        
        concepts_response = llm.invoke([
            SystemMessage(content="You are an expert at identifying key terminology and concepts."),
            HumanMessage(content=concepts_prompt)
        ])
        
        important_concepts = [
            concept.strip()
            for concept in concepts_response.content.strip().split(',')
            if concept.strip()
        ][:8]
        
        # Step 5: Extract Topics
        print("   → Categorizing topics...")
        topics_prompt = f"""Identify the main topics/themes covered. Return comma-separated, lowercase.

Transcript:
{transcript_for_prompts[:2000]}

Topics:"""
        
        topics_response = llm.invoke([
            SystemMessage(content="You are an expert at categorizing educational content."),
            HumanMessage(content=topics_prompt)
        ])
        
        topics = [
            topic.strip().lower()
            for topic in topics_response.content.strip().split(',')
            if topic.strip()
        ][:6]
        
        # Step 6: Generate Study Tips
        print("   → Creating study recommendations...")
        study_tips_prompt = f"""Based on this lecture content, provide 4-5 specific study tips to help students master this material.

Transcript:
{transcript_for_prompts}

Study tips (one per line):"""
        
        study_tips_response = llm.invoke([
            SystemMessage(content="You are an expert study coach. Provide actionable, specific study strategies."),
            HumanMessage(content=study_tips_prompt)
        ])
        
        study_tips = [
            tip.strip().lstrip('•-*0123456789.').strip()
            for tip in study_tips_response.content.strip().split('\n')
            if tip.strip()
        ][:5]
        
        # Step 7: Generate Practice Questions
        print("   → Generating practice questions...")
        questions_prompt = f"""Create 5 practice questions that test understanding of this lecture material. Include a mix of conceptual and application questions.

Transcript:
{transcript_for_prompts}

Questions (one per line):"""
        
        questions_response = llm.invoke([
            SystemMessage(content="You are an expert at creating educational assessments."),
            HumanMessage(content=questions_prompt)
        ])
        
        practice_questions = [
            q.strip().lstrip('•-*0123456789.').strip()
            for q in questions_response.content.strip().split('\n')
            if q.strip()
        ][:5]
        
        print(f"   ✅ Enhanced summarization complete (Session: {session_id[:8]}...)")
        
        return TranscriptSummary(
            summary=summary,
            detailed_notes=detailed_notes,
            key_points=key_points,
            topics=topics,
            important_concepts=important_concepts,
            study_tips=study_tips,
            practice_questions=practice_questions,
            session_id=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"   ❌ Error generating summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while summarizing the transcript: {str(e)}"
        )


# Follow-up Q&A endpoint for transcript sessions
@app.post("/summarize/ask")
async def ask_about_transcript(request: FollowUpRequest):
    """
    Answer follow-up questions about a previously summarized transcript using RAG.
    
    Args:
        request: Contains session_id and question
    
    Returns:
        Detailed answer based on the transcript content
    """
    try:
        # Validate session
        if request.session_id not in transcript_sessions:
            raise HTTPException(
                status_code=404, 
                detail="Session not found. Please regenerate the summary."
            )
        
        session = transcript_sessions[request.session_id]
        transcript = session["transcript"]
        
        print(f"\n💬 Follow-up Question - Session: {request.session_id[:8]}...")
        print(f"   Question: {request.question}")
        
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Use the transcript as context to answer the question
        answer_prompt = f"""You are a knowledgeable teaching assistant. Answer the student's question based EXCLUSIVELY on the lecture transcript provided.

Lecture Transcript:
{transcript}

Student Question: {request.question}

Instructions:
- Provide a detailed, comprehensive answer
- Use specific information and examples from the lecture
- If the lecture doesn't cover this topic, clearly state that
- Explain concepts thoroughly as if teaching the student
- Be encouraging and educational in tone

Answer:"""
        
        answer_response = llm.invoke([
            SystemMessage(content="You are an expert teaching assistant helping students understand lecture material. Provide detailed, educational responses."),
            HumanMessage(content=answer_prompt)
        ])
        
        answer = answer_response.content.strip()
        
        print(f"   ✅ Answer generated")
        
        return {
            "answer": answer,
            "session_id": request.session_id,
            "question": request.question
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"   ❌ Error answering question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your question: {str(e)}"
        )


@app.get("/api/transcripts/{course_id}/{filename}")
async def get_transcript(course_id: str, filename: str):
    """
    Serve transcript files for auto-loading
    """
    try:
        transcript_path = Path(__file__).parent / "transcripts" / course_id / filename
        
        if not transcript_path.exists():
            raise HTTPException(status_code=404, detail="Transcript not found")
        
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(content=content)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error reading transcript: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
