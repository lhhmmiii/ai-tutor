import os
import sys

import uvicorn
from fastapi import FastAPI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from writing.routers import grammar_check_router, level_analysis_router, writing_feedback_router,\
                            user_router, auth_router, chat_memory_router, vocabulary_support_router


app = FastAPI()



#Add routers
app.include_router(grammar_check_router)
app.include_router(level_analysis_router)
app.include_router(writing_feedback_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(chat_memory_router)
app.include_router(vocabulary_support_router)

@app.get("/")
async def root():
    return "Hello Hung"


host = "127.0.0.1"
port = 8000
if __name__ == "__main__":
    uvicorn.run("writing.main:app", host=host, port=port, reload=True)
