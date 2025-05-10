import os
import sys
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from writing.routers import grammar_check_router, level_analysis_router, writing_feedback_router,\
                            user_router, auth_router, chat_memory_router, vocabulary_support_router,\
                            agent_router, extract_office_file_router, extract_html_file_router,\
                            extract_table_file_router, document_qa_router

from writing.dependencies import initialize_storage_context
from writing.config.llm import gemini
from writing.config.setting import embed_model, setting

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = gemini
    app.state.embed_model = embed_model()
    setting(llm = app.state.llm, embed_model = app.state.embed_model)
    app.state.storage_context = initialize_storage_context("StudyEnglishData", "Grammar")
    yield
    # Clean up resources
    app.state.storage_context = None
    app.state.llm = None 
    app.state.embed_model = None
    

app = FastAPI(lifespan=lifespan)

# Allow CORS for frontend running on a different por
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


#Add routers
app.include_router(grammar_check_router)
app.include_router(level_analysis_router)
app.include_router(writing_feedback_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(chat_memory_router)
app.include_router(vocabulary_support_router)
app.include_router(agent_router)
app.include_router(extract_office_file_router)
app.include_router(extract_html_file_router)
app.include_router(extract_table_file_router)
app.include_router(document_qa_router)

@app.get("/")
async def root():
    return "Hello Hung"


host = "127.0.0.1"
port = 8000
if __name__ == "__main__":
    uvicorn.run("writing.main:app", host=host, port=port, reload=True)
