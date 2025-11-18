# Intelligent Course Companion - Backend

## Setup Instructions

### 1. Environment Setup

1. Copy the example environment file and fill in your credentials:
```bash
cp env.example .env
```

2. Edit `.env` and add your credentials:
- `CANVAS_USERNAME`: Your Canvas username
- `CANVAS_PASSWORD`: Your Canvas password  
- `OPENAI_API_KEY`: Your OpenAI API key

### 2. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Running the Application

```bash
# Start the FastAPI server
python main.py
```

The API will be available at `http://localhost:8000`

### 4. API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
/backend
├── main.py                 # FastAPI server with API endpoints
├── /scripts
│   ├── scraper.py          # Canvas/Echo360 transcript scraper
│   └── rag_pipeline.py     # RAG processing and vector storage
├── /transcripts            # Downloaded transcripts (auto-created)
├── /chroma_db             # ChromaDB vector storage (auto-created)
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create from env.example)
└── .gitignore            # Git ignore rules
```

## API Endpoints

- `GET /` - Health check
- `POST /sync` - Trigger transcript download and processing
- `POST /query/{course_id}` - Query a specific course with a question

## Development Notes

- The scraper uses Playwright for reliable JavaScript-heavy site automation
- RAG pipeline uses LangChain for document processing and OpenAI for embeddings
- ChromaDB provides local vector storage for the MVP
- All course data is isolated by course_id for proper data separation
