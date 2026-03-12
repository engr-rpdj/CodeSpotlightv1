<div align="center">

# CodeSpotlight

### Understand any codebase, in seconds.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Railway-7c6af7?style=for-the-badge&logo=railway)](https://codespotlightv1-production.up.railway.app)
[![GitHub](https://img.shields.io/badge/GitHub-engr--rpdj-black?style=for-the-badge&logo=github)](https://github.com/engr-rpdj)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)

**CodeSpotlight** is an autonomous multi-agent AI system that analyzes any public GitHub repository and instantly generates architecture documentation, dependency maps, and an interactive chat assistant — so developers can understand any codebase in seconds instead of days.

[Try it Live](https://codespotlightv1-production.up.railway.app) · [How it works](#how-it-works) · [Run locally](https://github.com/engr-rpdj/CodeSpotlightv1)

</div>

---

## Features

| Feature | Description |
|---|---|
|  **Auto Documentation** | Generates architecture overview, module breakdown, and developer notes |
|  **Repo Chat** | Ask anything about the codebase — powered by LLaMA 3.3 70B |
|  **Smart Chunking** | Handles massive repos (100+ files) by processing in intelligent batches |
|  **Session History** | All past sessions saved locally — resume any conversation instantly |
|  **Export to Markdown** | Download generated docs as a `.md` file |
|  **Fast & Free** | Powered by Groq's free API — no OpenAI costs |

---

## Demo

> Paste any public GitHub URL → get instant documentation + chat

```
https://github.com/pallets/flask        → analyzed in ~20 seconds
https://github.com/tiangolo/fastapi     → analyzed in ~25 seconds
https://github.com/django/django        → analyzed in ~3 minutes (500+ files)
```

---

## How It Works

CodeSpotlight uses a **multi-agent pipeline** where each AI agent has a specialized role:

```
GitHub URL
    │
    ▼
┌─────────────────┐
│   Repo Loader   │  Clones the repository via GitPython
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Code Scanner   │  Scans all files, prioritizes key files,
│                 │  splits into chunks of 15 files each
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│           Chunk Summarizer              │
│  Summarizes each batch of files using   │
│  llama-3.1-8b-instant (fast & efficient)│
└────────────────┬────────────────────────┘
                 │
                 ▼
    ┌────────────┴─────────────┐────────────────────────┐
    │                          │                        │
    ▼                          ▼                        ▼
┌──────────┐          ┌──────────────┐         ┌──────────────────┐
│  Repo    │          │  Dependency  │         │  Architecture    │
│ Analyzer │          │    Agent     │         │     Agent        │
│  Agent   │          │              │         │                  │
└────┬─────┘          └──────┬───────┘         └────────┬─────────┘
     │                       │                          │
     └───────────────────────┴──────────────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Documentation Agent │
                  │  Synthesizes all     │
                  │  results into final  │
                  │  Markdown docs       │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     Chat Agent       │
                  │  Multi-turn Q&A      │
                  │  about the codebase  │
                  └──────────────────────┘
```

### Agents

| Agent | Model | Role |
|---|---|---|
| Chunk Summarizer | `llama-3.1-8b-instant` | Fast batch summarization |
| Repo Analyzer | `llama-3.3-70b-versatile` | Language, framework, purpose detection |
| Dependency Agent | `llama-3.3-70b-versatile` | Libraries, APIs, databases |
| Architecture Agent | `llama-3.3-70b-versatile` | System design inference |
| Documentation Agent | `llama-3.3-70b-versatile` | Final doc synthesis |
| Chat Agent | `llama-3.3-70b-versatile` | Interactive Q&A |

---

## Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com) — REST API framework
- [GitPython](https://gitpython.readthedocs.io) — Repository cloning
- [Groq API](https://console.groq.com) — LLM inference (free tier)
- [OpenAI SDK](https://github.com/openai/openai-python) — API client (Groq-compatible)

**Frontend**
- Vanilla HTML/CSS/JavaScript — no framework needed
- [Marked.js](https://marked.js.org) — Markdown rendering
- localStorage — session persistence

**Infrastructure**
- [Railway](https://railway.app) — Cloud deployment
- [GitHub Actions](https://github.com/features/actions) — CI/CD pipeline

---

## Run Locally

### Prerequisites
- Python 3.11+
- [Groq API key](https://console.groq.com) (free)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/engr-rpdj/CodeSpotlightv1.git
cd CodeSpotlightv1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your Groq API key

# 4. Run the server
python -m uvicorn server:app --reload

# 5. Open in browser
# http://localhost:8080
```

### Environment Variables

```env
GROQ_API_KEY=gsk_your_key_here
```

Get your free key at [console.groq.com](https://console.groq.com)

---

## Project Structure

```
CodeSpotlightv1/
├── server.py                     # FastAPI backend + API routes
├── static/
│   └── index.html                # Full frontend (single file)
├── core/
│   ├── repo_loader.py            # GitHub repo cloning
│   ├── code_scanner.py           # File scanning + chunking
│   └── repo_manager.py           # Agent orchestration pipeline
├── agents/
│   ├── __init__.py               # Groq client + shared helpers
│   ├── repo_analyzer_agent.py    # Language/framework detection
│   ├── dependency_agent.py       # Dependency analysis
│   ├── architecture_agent.py     # Architecture inference
│   ├── documentation_agent.py    # Doc generation
│   ├── chunk_summarizer_agent.py # Batch file summarization
│   └── chat_agent.py             # Interactive chat
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD
├── railway.json                  # Railway deployment config
├── Procfile                      # Process definition
└── requirements.txt
```

---

## Roadmap

**Completed**
- Multi-agent pipeline
- Smart chunking for large repos
- Repo chat (multi-turn)
- Session history
- Export to Markdown
- Deploy to Railway
 
**Coming Soon**
- Clerk authentication (multi-user)
- AWS S3 + DynamoDB (persistent storage)
- Amazon Bedrock integration (Claude 4 / AWS Nova)
- Terraform + GitHub Actions (full CI/CD)
- Bedrock AgentCore (enterprise multi-agent)
---

## Author

**Regine Precious De Joya**
| Aspiring AI Engineer | Former (Analyst II ERP Package Applications) @ DXC Technology

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/reginepreciousdejoya/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/engr-rpdj)

---

<div align="center">
Built by Engr. Regine Precious de Joya · Powered by Groq + LLaMA 3.3
</div>