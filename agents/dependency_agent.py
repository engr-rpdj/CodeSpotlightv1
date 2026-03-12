from agents import run_agent

SYSTEM_PROMPT = """
You are a dependency analysis expert.

Given source code files, identify:
1. All external libraries and packages imported
2. Any databases being used (PostgreSQL, MongoDB, Redis, etc.)
3. Any external APIs or services called
4. Any environment variables required (from .env files or os.getenv)

Group them into categories: Core Libraries, Dev Tools, External Services, Databases.
Be concise. Use bullet points.
"""

def analyze_dependencies(file_dump: str) -> str:
    print("[agent] Running Dependency Analyzer...")
    return run_agent(SYSTEM_PROMPT, f"Here are the repository files:\n\n{file_dump}")
