import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Primary: Groq
groq_client = OpenAI(
    api_key=GROQ_API_KEY if GROQ_API_KEY else "dummy",
    base_url="https://api.groq.com/openai/v1"
)

# Fallback: Gemini
gemini_client = OpenAI(
    api_key=GEMINI_API_KEY if GEMINI_API_KEY else "dummy",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

GROQ_MODEL   = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-2.0-flash"


def run_agent(system_prompt: str, user_content: str) -> str:
    """Tries Groq first, falls back to Gemini on rate limit."""

    # Try Groq first
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=2000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_content}
            ]
        )
        print("[agents] Used: Groq")
        return response.choices[0].message.content

    except Exception as e:
        if "429" in str(e) or "rate_limit" in str(e).lower():
            print("[agents] Groq rate limited — falling back to Gemini...")
        else:
            print(f"[agents] Groq error: {e} — falling back to Gemini...")

    # Fallback: Gemini
    try:
        response = gemini_client.chat.completions.create(
            model=GEMINI_MODEL,
            max_tokens=2000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_content}
            ]
        )
        print("[agents] Used: Gemini (fallback)")
        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Both Groq and Gemini failed. Last error: {e}")