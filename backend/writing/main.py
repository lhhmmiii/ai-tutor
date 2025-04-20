import os
import sys

import uvicorn
from fastapi import FastAPI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


app = FastAPI()



#Add routers

@app.get("/")
async def root():
    return "Hello Hung"


host = "127.0.0.1"
port = 8000
if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
