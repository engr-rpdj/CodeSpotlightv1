import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Primary: Groq
groq_client = OpenAI(
    api_key=GROQ_API_KEY if GROQ_API_KEY else "dummy",
    base_url="https://api.groq.com/openai/v1"
)

GROQ_MODEL = "llama-3.3-70b-versatile"  # For final docs (best quality)
GROQ_MODEL_FAST = "llama-3.1-8b-instant"   # For chunking (30x more tokens)


def run_agent(system_prompt: str, user_content: str) -> str:
    """Calls Groq only."""
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
#----------------------------------------------------------------------------
# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# # Primary: Groq
# groq_client = OpenAI(
#     api_key=GROQ_API_KEY if GROQ_API_KEY else "dummy",
#     base_url="https://api.groq.com/openai/v1"
# )

# GROQ_MODEL = "llama-3.3-70b-versatile"


# def run_agent(system_prompt: str, user_content: str) -> str:
#     """Calls Groq only."""
#     response = groq_client.chat.completions.create(
#         model=GROQ_MODEL,
#         max_tokens=2000,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user",   "content": user_content}
#         ]
#     )
#     print("[agents] Used: Groq")
#     return response.choices[0].message.content