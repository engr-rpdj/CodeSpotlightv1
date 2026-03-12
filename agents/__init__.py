# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1"
# )

# def run_agent(system_prompt: str, user_content: str) -> str:
#     """Shared helper — sends a prompt to GPT-4o-mini and returns the text response."""
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         max_tokens=2000,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_content}
#         ]
#     )
#     return response.choices[0].message.content
#--------------------------------------------------------
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Primary: Groq (fast, free)
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Fallback: Google Gemini (free, 1500 req/day)
# Gemini supports the OpenAI-compatible SDK too
gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

GROQ_MODEL   = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-2.0-flash"


def run_agent(system_prompt: str, user_content: str) -> str:
    """
    Tries Groq first. If rate limited (429), falls back to Gemini automatically.
    """
    # ── Try Groq first ──
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
        # Check if it's a rate limit error
        if "429" in str(e) or "rate_limit" in str(e).lower() or "rate limit" in str(e).lower():
            print("[agents] Groq rate limited — falling back to Gemini...")
        else:
            print(f"[agents] Groq error: {e} — falling back to Gemini...")

    # ── Fallback: Gemini ──
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