# 🤖 AI Codebase Analyzer

An autonomous multi-agent system that analyzes any GitHub repository and generates developer documentation automatically.

## What it does

Paste a GitHub repo URL → get back:
- Project overview & purpose
- Tech stack & frameworks detected
- System architecture diagram
- Dependency map
- How-to-run instructions
- Developer notes

## How it works

```
GitHub URL
    ↓
repo_loader.py     → clones the repo
code_scanner.py    → extracts source files
    ↓
Repo Analyzer Agent    → detects languages, frameworks, purpose
Dependency Agent       → finds libraries, APIs, databases
Architecture Agent     → infers system design
    ↓
Documentation Agent    → synthesizes everything into Markdown
    ↓
Gradio UI              → displays the result
```

## Setup

### 1. Clone this project
```bash
git clone <this-repo>
cd codebase-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
```bash
cp .env.example .env
# Open .env and paste your Anthropic API key
```

### 4. Run
```bash
python app.py
```

Then open http://localhost:7860 in your browser.

## Project Structure

```
codebase-agent/
├── app.py                    # Gradio UI + entry point
├── core/
│   ├── repo_loader.py        # Clones GitHub repos
│   ├── code_scanner.py       # Scans and reads source files
│   └── repo_manager.py       # Orchestrates all agents
├── agents/
│   ├── __init__.py           # Shared Claude API client
│   ├── repo_analyzer_agent.py
│   ├── dependency_agent.py
│   ├── architecture_agent.py
│   └── documentation_agent.py
├── repos/                    # Cloned repos go here (auto-created)
├── requirements.txt
└── .env.example
```

## Requirements

- Python 3.10+
- Anthropic API key (get one at console.anthropic.com)
