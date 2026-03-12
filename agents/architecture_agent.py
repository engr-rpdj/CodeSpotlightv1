from agents import run_agent

SYSTEM_PROMPT = """
You are a senior software architect.

Given source code files, infer the system architecture:
1. Is there a frontend? What technology?
2. Is there a backend / API layer? What framework?
3. Is there a database layer?
4. Are there background workers or queues?
5. How do the main components communicate?

Draw a simple ASCII or text diagram if it helps.
Explain the architecture clearly for a new developer joining the project.
"""

def analyze_architecture(file_dump: str) -> str:
    print("[agent] Running Architecture Analyzer...")
    return run_agent(SYSTEM_PROMPT, f"Here are the repository files:\n\n{file_dump}")
