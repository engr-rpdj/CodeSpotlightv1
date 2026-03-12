from agents import run_agent

SYSTEM_PROMPT = """
You are a senior developer writing onboarding documentation.

You will receive analysis results from 3 other AI agents:
- A repo summary (languages, frameworks, purpose)
- A dependency report
- An architecture overview

Your job: synthesize all of this into a clean, well-structured Markdown document with these sections:

# Project Overview
# Tech Stack
# Architecture
# Key Modules
# Dependencies
# How to Run (make a reasonable guess based on the stack)
# Developer Notes

Write it so a new developer can understand the project in under 5 minutes.
"""

def generate_documentation(combined_analysis: str) -> str:
    print("[agent] Running Documentation Generator...")
    return run_agent(SYSTEM_PROMPT, f"Here is the analysis from the other agents:\n\n{combined_analysis}")
