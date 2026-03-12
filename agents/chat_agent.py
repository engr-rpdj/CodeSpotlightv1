from agents import groq_client, gemini_client, GROQ_MODEL, GEMINI_MODEL

def chat_with_repo(question: str, file_dump: str, history: list) -> str:
    """
    Answers questions about the codebase.
    Tries Groq first, falls back to Gemini if rate limited.
    """
    SYSTEM_PROMPT = """
You are an expert software engineer and code reviewer.

You have been given context about a GitHub repository.
Answer the user's questions clearly and specifically.

Rules:
- Reference actual file names when relevant
- Use code blocks when showing code examples
- If something isn't covered in the context, say so honestly
- Keep answers helpful and to the point
"""
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + f"\n\n## Repository Context\n\n{file_dump}"
        }
    ]

    for human_msg, ai_msg in history:
        messages.append({"role": "user",      "content": human_msg})
        messages.append({"role": "assistant", "content": ai_msg})

    messages.append({"role": "user", "content": question})

    # Try Groq first
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=1000,
            messages=messages
        )
        print("[chat_agent] Used: Groq")
        return response.choices[0].message.content
    except Exception as e:
        if "429" in str(e) or "rate_limit" in str(e).lower():
            print("[chat_agent] Groq rate limited — falling back to Gemini...")
        else:
            print(f"[chat_agent] Groq error: {e} — trying Gemini...")

    # Fallback: Gemini
    response = gemini_client.chat.completions.create(
        model=GEMINI_MODEL,
        max_tokens=1000,
        messages=messages
    )
    print("[chat_agent] Used: Gemini (fallback)")
    return response.choices[0].message.content
#-=----------------------------------------------------------------------------
# from agents import client

# def chat_with_repo(question: str, file_dump: str, history: list) -> str:
#     """
#     Answers questions about the codebase using Groq (free & fast).
#     """

#     SYSTEM_PROMPT = """
# You are an expert software engineer and code reviewer.

# You have been given context about a GitHub repository.
# Answer the user's questions clearly and specifically.

# Rules:
# - Reference actual file names when relevant
# - Use code blocks when showing code examples
# - If something isn't covered in the context, say so honestly
# - Keep answers helpful and to the point
# """

#     messages = [
#         {
#             "role": "system",
#             "content": SYSTEM_PROMPT + f"\n\n## Repository Context\n\n{file_dump}"
#         }
#     ]

#     for human_msg, ai_msg in history:
#         messages.append({"role": "user",      "content": human_msg})
#         messages.append({"role": "assistant", "content": ai_msg})

#     messages.append({"role": "user", "content": question})

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         max_tokens=1000,
#         messages=messages
#     )

#     return response.choices[0].message.content