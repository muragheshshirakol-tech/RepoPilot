import os
import uvicorn
from dotenv import load_dotenv  # <--- MOVED TO TOP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# LOAD ENV VARS FIRST!
load_dotenv()

# Now it's safe to import routes (which imports db)
from routes import router 

app = FastAPI(title="RepoPilot Backend", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)