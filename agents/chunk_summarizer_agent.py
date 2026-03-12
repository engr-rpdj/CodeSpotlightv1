from agents import groq_client, GROQ_MODEL_FAST

SYSTEM_PROMPT = """
You are an expert software engineer doing a quick scan of source files.
Write a CONCISE summary of what you see — 150 words max.
Cover: what files do, important classes/functions, libraries used.
"""

def summarize_chunk(file_dump: str, chunk_index: int, total_chunks: int) -> str:
    """Uses the fast 8B model — 30x more tokens available vs 70B."""
    print(f"[chunk_summarizer] Summarizing chunk {chunk_index + 1}/{total_chunks} (fast model)...")
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL_FAST,  # llama-3.1-8b-instant
        max_tokens=300,         # keep summaries short
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Files in this batch:\n\n{file_dump}"}
        ]
    )
    return response.choices[0].message.content
#-----------------------------------------------------------
# from agents import groq_client, GROQ_MODEL

# SYSTEM_PROMPT = """
# You are an expert software engineer doing a quick scan of source files.
# Write a CONCISE summary of what you see — 150 words max.
# Cover: what files do, important classes/functions, libraries used.
# """

# def summarize_chunk(file_dump: str, chunk_index: int, total_chunks: int) -> str:
#     print(f"[chunk_summarizer] Summarizing chunk {chunk_index + 1}/{total_chunks}...")
#     response = groq_client.chat.completions.create(
#         model=GROQ_MODEL,
#         max_tokens=400,
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user",   "content": f"Files in this batch:\n\n{file_dump}"}
#         ]
#     )
#     return response.choices[0].message.content