# """
# RepoManager — the orchestrator.

# It runs all 3 analysis agents, then feeds their output into
# the documentation agent to produce the final result.
# """

# from core.code_scanner import format_files_for_prompt
# from agents.repo_analyzer_agent import analyze_repo
# from agents.dependency_agent import analyze_dependencies
# from agents.architecture_agent import analyze_architecture
# from agents.documentation_agent import generate_documentation


# class RepoManager:

#     def run(self, file_data: list[dict]) -> str:
#         """
#         Takes scanned file data, runs all agents, returns final Markdown docs.
#         """

#         # Convert file list into one big readable text block for the AI
#         file_dump = format_files_for_prompt(file_data)

#         # --- Phase 1: Run the 3 analysis agents ---
#         repo_summary = analyze_repo(file_dump)
#         dependencies = analyze_dependencies(file_dump)
#         architecture = analyze_architecture(file_dump)

#         # --- Phase 2: Combine all results ---
#         combined = f"""
# ## Repo Summary
# {repo_summary}

# ## Dependencies
# {dependencies}

# ## Architecture
# {architecture}
# """

#         # --- Phase 3: Documentation agent synthesizes everything ---
#         final_docs = generate_documentation(combined)

#         return final_docs

"""
repo_manager.py — orchestrates the full pipeline

Flow:
  1. Split all files into chunks
  2. Summarize each chunk (handles massive repos)
  3. Combine all chunk summaries
  4. Run the 3 analysis agents on the combined summary
  5. Documentation agent writes the final docs
"""

from core.code_scanner import chunk_files, format_files_for_prompt
from agents.chunk_summarizer_agent import summarize_chunk
from agents.repo_analyzer_agent import analyze_repo
from agents.dependency_agent import analyze_dependencies
from agents.architecture_agent import analyze_architecture
from agents.documentation_agent import generate_documentation


class RepoManager:

    def run(self, file_data: list[dict]) -> str:

        total_files = len(file_data)
        print(f"[repo_manager] Starting pipeline for {total_files} files")

        # ── Step 1: Chunk the files ──
        chunks = chunk_files(file_data, chunk_size=15)

        # ── Step 2: Summarize each chunk ──
        # Small repos (≤15 files): just 1 chunk, no extra work
        # Large repos (100+ files): each chunk gets its own summary
        chunk_summaries = []

        for i, chunk in enumerate(chunks):
            file_dump = format_files_for_prompt(chunk)
            summary = summarize_chunk(file_dump, chunk_index=i, total_chunks=len(chunks))
            chunk_summaries.append(f"### Batch {i+1} of {len(chunks)}\n{summary}")

        # ── Step 3: Combine all chunk summaries into one text ──
        combined_file_context = f"""
This repository has {total_files} files split into {len(chunks)} batches.
Below are the summaries of each batch:

{"".join(chunk_summaries)}
""".strip()

        print(f"[repo_manager] All chunks summarized. Running analysis agents...")

        # ── Step 4: Run the 3 analysis agents on the combined summary ──
        repo_summary   = analyze_repo(combined_file_context)
        dependencies   = analyze_dependencies(combined_file_context)
        architecture   = analyze_architecture(combined_file_context)

        combined_analysis = f"""
## Repo Summary
{repo_summary}

## Dependencies
{dependencies}

## Architecture
{architecture}
""".strip()

        # ── Step 5: Documentation agent synthesizes everything ──
        print(f"[repo_manager] Generating final documentation...")
        final_docs = generate_documentation(combined_analysis)

        print(f"[repo_manager] Done.")
        return final_docs