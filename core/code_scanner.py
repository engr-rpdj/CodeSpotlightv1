# import os

# ALLOWED_EXTENSIONS = [
#     ".py", ".js", ".ts", ".tsx", ".jsx",
#     ".java", ".go", ".rs", ".cpp", ".c",
#     ".md", ".yml", ".yaml", ".toml", ".json"
# ]

# SKIP_DIRS = {
#     ".git", "node_modules", "__pycache__", ".venv",
#     "venv", "dist", "build", ".idea", ".vscode"
# }

# # Tuned for speed: smaller files, fewer files
# MAX_FILE_CHARS = 1500
# MAX_FILES = 20

# # These files are always included first — most useful for understanding a project
# PRIORITY_FILES = {
#     "main.py", "app.py", "index.py", "server.py",
#     "index.js", "index.ts", "main.js", "server.js",
#     "package.json", "requirements.txt", "pyproject.toml",
#     "docker-compose.yml", "Dockerfile", "README.md"
# }


# def scan_repo(repo_path: str) -> list[dict]:
#     """
#     Walks the repo and returns up to MAX_FILES files.
#     Priority files (README, main, package.json, etc.) are always included first.
#     """
#     priority = []
#     others = []

#     for root, dirs, files in os.walk(repo_path):
#         dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

#         for file in files:
#             ext = os.path.splitext(file)[1]
#             if ext not in ALLOWED_EXTENSIONS:
#                 continue

#             full_path = os.path.join(root, file)
#             relative_path = os.path.relpath(full_path, repo_path)

#             try:
#                 with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
#                     content = f.read(MAX_FILE_CHARS)
#             except Exception as e:
#                 print(f"[code_scanner] Could not read {relative_path}: {e}")
#                 continue

#             entry = {"path": relative_path, "extension": ext, "content": content}

#             if file in PRIORITY_FILES:
#                 priority.append(entry)
#             else:
#                 others.append(entry)

#     # Priority files first, then fill up to MAX_FILES
#     file_data = (priority + others)[:MAX_FILES]

#     print(f"[code_scanner] Sending {len(file_data)}/{len(priority)+len(others)} files to agents")
#     return file_data


# def format_files_for_prompt(file_data: list[dict]) -> str:
#     """Formats file list into a readable text block for AI prompts."""
#     parts = []
#     for f in file_data:
#         parts.append(f"### File: {f['path']}\n```{f['extension'][1:]}\n{f['content']}\n```")
#     return "\n\n".join(parts)

import os

ALLOWED_EXTENSIONS = [
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".go", ".rs", ".cpp", ".c",
    ".md", ".yml", ".yaml", ".toml", ".json"
]

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv",
    "venv", "dist", "build", ".idea", ".vscode"
}

MAX_FILE_CHARS = 2000  # characters per file

# Priority files always go into the FIRST chunk
PRIORITY_FILES = {
    "main.py", "app.py", "index.py", "server.py",
    "index.js", "index.ts", "main.js", "server.js",
    "package.json", "requirements.txt", "pyproject.toml",
    "docker-compose.yml", "Dockerfile", "README.md"
}


def scan_repo(repo_path: str) -> list[dict]:
    """
    Scans ALL valid files in the repo — no file limit anymore.
    Returns a flat list of file dicts.
    """
    priority = []
    others = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext not in ALLOWED_EXTENSIONS:
                continue

            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, repo_path)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(MAX_FILE_CHARS)
            except Exception as e:
                print(f"[code_scanner] Skipping {relative_path}: {e}")
                continue

            entry = {
                "path": relative_path,
                "extension": ext,
                "content": content
            }

            if file in PRIORITY_FILES:
                priority.append(entry)
            else:
                others.append(entry)

    # Priority files first, then the rest — NO cap on total
    file_data = priority + others
    print(f"[code_scanner] Found {len(file_data)} files total ({len(priority)} priority)")
    return file_data


def chunk_files(file_data: list[dict], chunk_size: int = 15) -> list[list[dict]]:
    """
    Splits the flat file list into chunks of chunk_size.
    Example: 47 files → [[15 files], [15 files], [15 files], [2 files]]
    """
    chunks = []
    for i in range(0, len(file_data), chunk_size):
        chunks.append(file_data[i:i + chunk_size])
    print(f"[code_scanner] Split into {len(chunks)} chunks of ~{chunk_size} files each")
    return chunks


def format_files_for_prompt(file_data: list[dict]) -> str:
    """
    Converts a list of file dicts into a readable text block for AI prompts.
    """
    parts = []
    for f in file_data:
        parts.append(f"### File: {f['path']}\n```{f['extension'][1:]}\n{f['content']}\n```")
    return "\n\n".join(parts)