from agents import run_agent

SYSTEM_PROMPT = """
You are an expert software engineer analyzing a codebase.

Given a set of source files, your job is to:
1. Identify the programming languages used
2. Detect frameworks and major libraries
3. Describe what the project does in 2-3 sentences
4. List the key modules or folders and their purpose

Be concise and structured. Use bullet points where helpful.
"""

def analyze_repo(file_dump: str) -> str:
    print("[agent] Running Repo Analyzer...")
    return run_agent(SYSTEM_PROMPT, f"Here are the repository files:\n\n{file_dump}")
