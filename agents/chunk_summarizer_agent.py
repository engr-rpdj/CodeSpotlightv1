# from agents import client

# SYSTEM_PROMPT = """
# You are an expert software engineer doing a quick scan of source files.

# You will receive a batch of files from a larger repository.
# Your job is to write a CONCISE summary of what you see in this batch:

# - What do these files do?
# - Any important classes, functions, or patterns?
# - Any libraries or frameworks used?
# - Any config, routes, models, or schemas?

# Keep it short — 150 words max. 
# This summary will be combined with summaries of other file batches.
# """

# def summarize_chunk(file_dump: str, chunk_index: int, total_chunks: int) -> str:
#     """
#     Summarizes a single chunk of files.
#     chunk_index and total_chunks are just for logging.
#     """
#     print(f"[chunk_summarizer] Summarizing chunk {chunk_index + 1}/{total_chunks}...")

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         max_tokens=400,
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": f"Here are the files in this batch:\n\n{file_dump}"}
#         ]
#     )
#     return response.choices[0].message.content
#---------------------------------------------------
from agents import groq_client, gemini_client, GROQ_MODEL, GEMINI_MODEL

SYSTEM_PROMPT = """
You are an expert software engineer doing a quick scan of source files.

You will receive a batch of files from a larger repository.
Your job is to write a CONCISE summary of what you see in this batch:

- What do these files do?
- Any important classes, functions, or patterns?
- Any libraries or frameworks used?
- Any config, routes, models, or schemas?

Keep it short — 150 words max.
This summary will be combined with summaries of other file batches.
"""

def summarize_chunk(file_dump: str, chunk_index: int, total_chunks: int) -> str:
    """
    Summarizes a single chunk of files.
    Tries Groq first, falls back to Gemini if rate limited.
    """
    print(f"[chunk_summarizer] Summarizing chunk {chunk_index + 1}/{total_chunks}...")

    # Try Groq first
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=400,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Here are the files in this batch:\n\n{file_dump}"}
            ]
        )
        print(f"[chunk_summarizer] Chunk {chunk_index + 1} — Used: Groq")
        return response.choices[0].message.content
    except Exception as e:
        if "429" in str(e) or "rate_limit" in str(e).lower():
            print(f"[chunk_summarizer] Groq rate limited on chunk {chunk_index + 1} — falling back to Gemini...")
        else:
            print(f"[chunk_summarizer] Groq error: {e} — trying Gemini...")

    # Fallback: Gemini
    response = gemini_client.chat.completions.create(
        model=GEMINI_MODEL,
        max_tokens=400,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Here are the files in this batch:\n\n{file_dump}"}
        ]
    )
    print(f"[chunk_summarizer] Chunk {chunk_index + 1} — Used: Gemini (fallback)")
    return response.choices[0].message.content