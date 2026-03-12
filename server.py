"""
server.py — FastAPI backend
Local:  python -m uvicorn server:app --reload
Cloud:  uvicorn server:app --host 0.0.0.0 --port $PORT
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from core.repo_loader import clone_repo
from core.code_scanner import scan_repo, chunk_files, format_files_for_prompt
from core.repo_manager import RepoManager
from agents.chat_agent import chat_with_repo
from agents.chunk_summarizer_agent import summarize_chunk

load_dotenv()

app = FastAPI(title="CodeSpotlight API")

# CORS — allow all origins so the frontend can call the API from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory state (per server instance)
repo_state = {
    "chat_context": None,
    "repo_name":    None,
}

SMALL_REPO_THRESHOLD = 15


# ── Request Models ──

class AnalyzeRequest(BaseModel):
    repo_url: str

class ChatRequest(BaseModel):
    question: str
    history:  list

class RestoreRequest(BaseModel):
    chat_context: str
    repo_name:    str


# ── Routes ──

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    """Railway uses this to check if the app is running."""
    return {"status": "ok", "app": "CodeSpotlight"}


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        repo_path = clone_repo(req.repo_url.strip())
        files     = scan_repo(repo_path)

        if not files:
            return {"error": "No readable source files found in this repo."}

        repo_name = req.repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        repo_state["repo_name"] = repo_name

        # Build chat context
        if len(files) <= SMALL_REPO_THRESHOLD:
            repo_state["chat_context"] = format_files_for_prompt(files)
        else:
            chunks    = chunk_files(files, chunk_size=15)
            summaries = []
            for i, chunk in enumerate(chunks):
                dump    = format_files_for_prompt(chunk)
                summary = summarize_chunk(dump, i, len(chunks))
                summaries.append(f"### Batch {i+1}\n{summary}")
            repo_state["chat_context"] = "\n\n".join(summaries)

        manager = RepoManager()
        result  = manager.run(files)

        return {
            "docs":         result,
            "repo_name":    repo_name,
            "file_count":   len(files),
            "chat_context": repo_state["chat_context"]
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/chat")
async def chat(req: ChatRequest):
    if not repo_state["chat_context"]:
        return {"error": "No repo analyzed yet. Please analyze a repo first."}
    try:
        answer = chat_with_repo(req.question, repo_state["chat_context"], req.history)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}


@app.post("/restore")
async def restore(req: RestoreRequest):
    try:
        repo_state["chat_context"] = req.chat_context
        repo_state["repo_name"]    = req.repo_name
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}
#------------------------------------------------------------------------------
# """
# server.py — FastAPI backend
# Run with: python -m uvicorn server:app --reload
# """

# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from core.repo_loader import clone_repo
# from core.code_scanner import scan_repo, chunk_files, format_files_for_prompt
# from core.repo_manager import RepoManager
# from agents.chat_agent import chat_with_repo
# from agents.chunk_summarizer_agent import summarize_chunk

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount("/static", StaticFiles(directory="static"), name="static")

# # In-memory state
# repo_state = {
#     "chat_context": None,
#     "repo_name":    None,
# }

# SMALL_REPO_THRESHOLD = 15


# class AnalyzeRequest(BaseModel):
#     repo_url: str

# class ChatRequest(BaseModel):
#     question: str
#     history:  list


# @app.get("/")
# def index():
#     return FileResponse("static/index.html")


# @app.post("/analyze")
# async def analyze(req: AnalyzeRequest):
#     try:
#         repo_path = clone_repo(req.repo_url.strip())
#         files     = scan_repo(repo_path)

#         if not files:
#             return {"error": "No readable source files found in this repo."}

#         repo_name = req.repo_url.rstrip("/").split("/")[-1].replace(".git", "")
#         repo_state["repo_name"] = repo_name

#         # Build chat context
#         if len(files) <= SMALL_REPO_THRESHOLD:
#             repo_state["chat_context"] = format_files_for_prompt(files)
#         else:
#             chunks    = chunk_files(files, chunk_size=15)
#             summaries = []
#             for i, chunk in enumerate(chunks):
#                 dump    = format_files_for_prompt(chunk)
#                 summary = summarize_chunk(dump, i, len(chunks))
#                 summaries.append(f"### Batch {i+1}\n{summary}")
#             repo_state["chat_context"] = "\n\n".join(summaries)

#         # Run the full agent pipeline
#         manager = RepoManager()
#         result  = manager.run(files)

#         return {"docs": result, "repo_name": repo_name, "file_count": len(files), "chat_context": repo_state["chat_context"]}

#     except Exception as e:
#         return {"error": str(e)}


# @app.post("/chat")
# async def chat(req: ChatRequest):
#     if not repo_state["chat_context"]:
#         return {"error": "No repo analyzed yet. Please analyze a repo first."}

#     try:
#         answer = chat_with_repo(req.question, repo_state["chat_context"], req.history)
#         return {"answer": answer}
#     except Exception as e:
#         return {"error": str(e)}




# class RestoreRequest(BaseModel):
#     chat_context: str
#     repo_name: str

# @app.post("/restore")
# async def restore(req: RestoreRequest):
#     """Restores a past session's context into server memory."""
#     try:
#         repo_state["chat_context"] = req.chat_context
#         repo_state["repo_name"]    = req.repo_name
#         return {"ok": True}
#     except Exception as e:
#         return {"error": str(e)}
#----------------------------------------------------------------------------------------------
# """
# server.py — FastAPI backend
# Run with: python -m uvicorn server:app --reload
# """

# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from core.repo_loader import clone_repo
# from core.code_scanner import scan_repo, chunk_files, format_files_for_prompt
# from core.repo_manager import RepoManager
# from agents.chat_agent import chat_with_repo
# from agents.chunk_summarizer_agent import summarize_chunk

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount("/static", StaticFiles(directory="static"), name="static")

# # In-memory state
# repo_state = {
#     "chat_context": None,   # what gets passed to chat (summaries or raw files)
#     "repo_name":    None,
# }

# SMALL_REPO_THRESHOLD = 15   # repos with ≤15 files use raw files for chat context


# class AnalyzeRequest(BaseModel):
#     repo_url: str

# class ChatRequest(BaseModel):
#     question: str
#     history:  list


# @app.get("/")
# def index():
#     return FileResponse("static/index.html")


# @app.post("/analyze")
# async def analyze(req: AnalyzeRequest):
#     try:
#         repo_path = clone_repo(req.repo_url.strip())
#         files     = scan_repo(repo_path)

#         if not files:
#             return {"error": "No readable source files found in this repo."}

#         repo_name = req.repo_url.rstrip("/").split("/")[-1].replace(".git", "")
#         repo_state["repo_name"] = repo_name

#         # Build chat context:
#         # Small repo  → raw file dump (richer detail for chat)
#         # Large repo  → chunk summaries (fits in context window)
#         if len(files) <= SMALL_REPO_THRESHOLD:
#             repo_state["chat_context"] = format_files_for_prompt(files)
#         else:
#             chunks   = chunk_files(files, chunk_size=15)
#             summaries = []
#             for i, chunk in enumerate(chunks):
#                 dump    = format_files_for_prompt(chunk)
#                 summary = summarize_chunk(dump, i, len(chunks))
#                 summaries.append(f"### Batch {i+1}\n{summary}")
#             repo_state["chat_context"] = "\n\n".join(summaries)

#         # Run the full agent pipeline
#         manager = RepoManager()
#         result  = manager.run(files)

#         return {"docs": result, "repo_name": repo_name, "file_count": len(files)}

#     except Exception as e:
#         return {"error": str(e)}


# @app.post("/chat")
# async def chat(req: ChatRequest):
#     if not repo_state["chat_context"]:
#         return {"error": "No repo analyzed yet. Please analyze a repo first."}

#     try:
#         answer = chat_with_repo(req.question, repo_state["chat_context"], req.history)
#         return {"answer": answer}
#     except Exception as e:
#         return {"error": str(e)}
    
#-----------------------------------------------------------------------------------------------
    
#     """
# server.py — FastAPI backend
# Run with: python -m uvicorn server:app --reload
# """

# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from core.repo_loader import clone_repo
# from core.code_scanner import scan_repo, chunk_files, format_files_for_prompt
# from core.repo_manager import RepoManager
# from agents.chat_agent import chat_with_repo
# from agents.chunk_summarizer_agent import summarize_chunk
# from agents.security_agent import scan_security

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount("/static", StaticFiles(directory="static"), name="static")

# # In-memory state
# repo_state = {
#     "chat_context": None,
#     "file_dump":    None,   # raw first-chunk dump for security scan
#     "repo_name":    None,
# }

# SMALL_REPO_THRESHOLD = 15


# class AnalyzeRequest(BaseModel):
#     repo_url: str

# class ChatRequest(BaseModel):
#     question: str
#     history:  list


# @app.get("/")
# def index():
#     return FileResponse("static/index.html")


# @app.post("/analyze")
# async def analyze(req: AnalyzeRequest):
#     try:
#         repo_path = clone_repo(req.repo_url.strip())
#         files     = scan_repo(repo_path)

#         if not files:
#             return {"error": "No readable source files found in this repo."}

#         repo_name = req.repo_url.rstrip("/").split("/")[-1].replace(".git", "")
#         repo_state["repo_name"] = repo_name

#         # Store raw file dump for security scanning (use first 30 files max)
#         security_files = files[:30]
#         repo_state["file_dump"] = format_files_for_prompt(security_files)

#         # Build chat context
#         if len(files) <= SMALL_REPO_THRESHOLD:
#             repo_state["chat_context"] = format_files_for_prompt(files)
#         else:
#             chunks    = chunk_files(files, chunk_size=15)
#             summaries = []
#             for i, chunk in enumerate(chunks):
#                 dump    = format_files_for_prompt(chunk)
#                 summary = summarize_chunk(dump, i, len(chunks))
#                 summaries.append(f"### Batch {i+1}\n{summary}")
#             repo_state["chat_context"] = "\n\n".join(summaries)

#         # Run the full agent pipeline
#         manager = RepoManager()
#         result  = manager.run(files)

#         return {"docs": result, "repo_name": repo_name, "file_count": len(files)}

#     except Exception as e:
#         return {"error": str(e)}


# @app.post("/chat")
# async def chat(req: ChatRequest):
#     if not repo_state["chat_context"]:
#         return {"error": "No repo analyzed yet. Please analyze a repo first."}

#     try:
#         answer = chat_with_repo(req.question, repo_state["chat_context"], req.history)
#         return {"answer": answer}
#     except Exception as e:
#         return {"error": str(e)}


# @app.post("/security")
# async def security():
#     if not repo_state["file_dump"]:
#         return {"error": "No repo analyzed yet. Please analyze a repo first."}

#     try:
#         result = scan_security(repo_state["file_dump"])
#         return result
#     except Exception as e:
#         return {"error": str(e)}