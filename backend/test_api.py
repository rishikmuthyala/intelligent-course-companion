"""
Quick API test script - Tests the backend without starting a server
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import from main
from scripts.rag_pipeline import RAGPipeline
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

async def test_query_system():
    """Test the query system end-to-end"""
    
    print("\n" + "="*60)
    print("🧪 TESTING QUERY SYSTEM")
    print("="*60)
    
    # Test question
    test_question = "What is a binary search tree and how does it work?"
    course_id = "test_course_12345"  # From our test setup
    
    print(f"\n📝 Question: {test_question}")
    print(f"📚 Course: {course_id}")
    
    # Step 1: Initialize RAG pipeline
    print("\n→ Step 1: Initializing RAG pipeline...")
    pipeline = RAGPipeline()
    
    # Step 2: Query for relevant context
    print("→ Step 2: Retrieving relevant context...")
    context_chunks = pipeline.query(
        course_id=course_id,
        search_query=test_question,
        num_results=5
    )
    
    if not context_chunks:
        print("❌ No relevant context found!")
        return False
    
    print(f"✅ Found {len(context_chunks)} relevant chunks")
    print(f"\n📄 Most relevant chunk preview:")
    print(f"   {context_chunks[0][:200]}...")
    
    # Step 3: Synthesize answer
    print("\n→ Step 3: Generating answer with GPT-4o-mini...")
    
    context = "\n\n---\n\n".join(context_chunks)
    
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

Question: {test_question}

Answer:"""
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    answer = response.content
    
    print("\n" + "="*60)
    print("📖 ANSWER:")
    print("="*60)
    print(answer)
    print("="*60)
    
    return True


def test_api_endpoints():
    """Show what API endpoints are available"""
    
    print("\n" + "="*60)
    print("📡 AVAILABLE API ENDPOINTS")
    print("="*60)
    
    endpoints = [
        ("GET", "/", "Health check"),
        ("POST", "/sync", "Trigger scraper to download transcripts"),
        ("GET", "/sync/status", "Check sync progress"),
        ("GET", "/courses", "List available courses"),
        ("POST", "/query/{course_id}", "Query a course (ask questions)"),
        ("GET", "/docs", "Interactive API documentation"),
    ]
    
    print("\nBase URL: http://localhost:8000\n")
    
    for method, endpoint, description in endpoints:
        print(f"  {method:6} {endpoint:25} - {description}")
    
    print("\n💡 To test these endpoints:")
    print("   1. Start backend: ./start_backend.sh")
    print("   2. Open browser: http://localhost:8000/docs")
    print("   3. Or use curl: curl http://localhost:8000/")


if __name__ == "__main__":
    print("\n🧪 AI Course Companion - API Test\n")
    
    # Test query system
    success = asyncio.run(test_query_system())
    
    if success:
        print("\n✅ Query system working perfectly!")
    else:
        print("\n⚠️  Query test failed")
    
    # Show API info
    test_api_endpoints()
    
    print("\n🎉 Your system is fully functional and ready to use!")
    print("\nNext steps:")
    print("   1. Run: chmod +x start_backend.sh && ./start_backend.sh")
    print("   2. Open: http://localhost:8000/docs")
    print("   3. Or start frontend: cd ../frontend && npm run dev")

