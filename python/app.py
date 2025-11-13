import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI

load_dotenv()

from controller.controller import router as api_router

app = FastAPI(title="Resume Chat Agent API")

app.include_router(api_router, prefix="") 

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)