"""
Simple test script to verify the AI Course Companion system works end-to-end
Tests: RAG pipeline, vector database, and query system
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test 1: Check if environment variables are set"""
    print("\n" + "="*60)
    print("TEST 1: ENVIRONMENT VARIABLES")
    print("="*60)
    
    required_vars = ["OPENAI_API_KEY", "CANVAS_USERNAME", "CANVAS_PASSWORD"]
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if "KEY" in var or "PASSWORD" in var:
                print(f"✅ {var}: {'*' * 8} (hidden)")
            else:
                print(f"✅ {var}: {value[:10]}...")
        else:
            print(f"❌ {var}: NOT SET")
            missing.append(var)
    
    if missing:
        print(f"\n⚠️  Missing variables: {', '.join(missing)}")
        print("   Please create a .env file with these variables")
        return False
    
    print("\n✅ All environment variables are set!")
    return True


def test_mock_transcript():
    """Test 2: Check if mock transcript exists"""
    print("\n" + "="*60)
    print("TEST 2: MOCK TRANSCRIPT FILE")
    print("="*60)
    
    mock_file = Path("./mock_transcript.txt")
    
    if not mock_file.exists():
        print("❌ mock_transcript.txt not found")
        return False
    
    content = mock_file.read_text()
    print(f"✅ Found mock_transcript.txt ({len(content)} characters)")
    print(f"   Preview: {content[:100]}...")
    
    return True


def test_rag_pipeline():
    """Test 3: Test RAG pipeline with mock data"""
    print("\n" + "="*60)
    print("TEST 3: RAG PIPELINE")
    print("="*60)
    
    try:
        # Import RAG pipeline
        sys.path.append(str(Path(__file__).parent / "scripts"))
        from scripts.rag_pipeline import RAGPipeline
        
        print("   → Creating RAG pipeline...")
        pipeline = RAGPipeline()
        
        # Create a test transcript directory
        test_dir = Path("./transcripts/test_course_12345")
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy mock transcript to test directory
        mock_file = Path("./mock_transcript.txt")
        if mock_file.exists():
            test_transcript = test_dir / "test_lecture.txt"
            test_transcript.write_text(mock_file.read_text())
            print(f"   ✅ Created test transcript: {test_transcript}")
        else:
            print("   ⚠️  No mock transcript, creating sample...")
            test_transcript = test_dir / "test_lecture.txt"
            sample_content = """
            Introduction to Search Engines
            
            Today we'll discuss how search engines work. Search engines use crawlers to 
            discover web pages. These crawlers follow links from page to page, building 
            an index of the web.
            
            The indexing process involves parsing HTML, extracting text, and storing it 
            in an inverted index. An inverted index maps words to the documents that 
            contain them.
            
            Ranking algorithms like PageRank determine which pages to show first. PageRank 
            was developed by Larry Page and Sergey Brin at Stanford University. It measures 
            the importance of web pages based on the link structure of the web.
            
            Modern search engines also use machine learning to improve search quality. They 
            analyze user behavior, click patterns, and dwell time to understand which results 
            are most relevant.
            """
            test_transcript.write_text(sample_content)
            print(f"   ✅ Created sample transcript: {test_transcript}")
        
        # Process transcripts
        print("   → Processing transcripts into vector database...")
        result = pipeline.process_and_store_transcripts()
        
        print(f"   ✅ Processed {result.get('files_processed', 0)} files")
        print(f"   ✅ Created {result.get('chunks_created', 0)} chunks")
        
        # Test query
        print("\n   → Testing query...")
        test_query = "What is PageRank?"
        results = pipeline.query(
            course_id="test_course_12345",
            search_query=test_query,
            num_results=3
        )
        
        if results:
            print(f"   ✅ Query successful! Found {len(results)} relevant chunks")
            print(f"   Preview: {results[0][:100]}...")
            return True
        else:
            print("   ❌ No results found for query")
            return False
            
    except Exception as e:
        print(f"   ❌ RAG Pipeline Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_api_query():
    """Test 4: Test the main.py query functionality"""
    print("\n" + "="*60)
    print("TEST 4: API QUERY FUNCTION")
    print("="*60)
    
    try:
        # Import the API modules
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
        
        print("   → Testing OpenAI connection...")
        
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Simple test query
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Say 'Hello, the system is working!' if you can read this.")
        ]
        
        response = llm.invoke(messages)
        print(f"   ✅ OpenAI Response: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ API Query Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_scraper_files():
    """Test 5: Check scraper files and dependencies"""
    print("\n" + "="*60)
    print("TEST 5: SCRAPER FILES")
    print("="*60)
    
    scraper_files = [
        "./scripts/advanced_scraper.py",
        "./scripts/ultra_advanced_scraper.py",
        "./scripts/rag_pipeline.py"
    ]
    
    all_exist = True
    for file in scraper_files:
        if Path(file).exists():
            print(f"   ✅ Found: {file}")
        else:
            print(f"   ❌ Missing: {file}")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests"""
    print("\n" + "🚀"*30)
    print("AI COURSE COMPANION - SYSTEM TEST")
    print("🚀"*30)
    
    results = {
        "Environment": test_environment(),
        "Mock Transcript": test_mock_transcript(),
        "Scraper Files": test_scraper_files(),
    }
    
    # Only run these if basic setup is done
    if results["Environment"]:
        results["RAG Pipeline"] = test_rag_pipeline()
        results["API Query"] = test_api_query()
    else:
        print("\n⚠️  Skipping advanced tests - please set up environment first")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Your system is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nNEXT STEPS:")
        print("   1. Create a .env file (copy from env.example)")
        print("   2. Add your API keys and Canvas credentials")
        print("   3. Run: python test_system.py")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

