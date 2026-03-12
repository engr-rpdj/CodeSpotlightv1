import os
from git import Repo

def clone_repo(repo_url: str, base_dir="repos") -> str:
    """
    Clones a GitHub repo into the repos/ folder.
    If the repo was already cloned before, it just returns the path (no re-clone).
    """
    os.makedirs(base_dir, exist_ok=True)

    # Extract repo name from URL, e.g. "https://github.com/user/my-repo" → "my-repo"
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(base_dir, repo_name)

    if os.path.exists(repo_path):
        print(f"[repo_loader] Repo already exists at: {repo_path}")
        return repo_path

    print(f"[repo_loader] Cloning {repo_url} → {repo_path}")
    Repo.clone_from(repo_url, repo_path)
    print(f"[repo_loader] Done.")
    return repo_path
