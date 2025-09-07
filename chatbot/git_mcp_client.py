import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("chatbot/logs/git_mcp_repos")
BASE_DIR.mkdir(exist_ok=True, parents=True)

def create_repo(repo_name):
    repo_path = BASE_DIR / repo_name
    if repo_path.exists():
        return f"El repositorio '{repo_name}' ya existe."
    
    repo_path.mkdir(parents=True)
    (repo_path / ".git").mkdir()
    
    commit_file = repo_path / "commits.log"
    commit_file.write_text("=== Historial de commits ===\n", encoding="utf-8")
    
    return f"Repositorio '{repo_name}' creado correctamente."

def create_file(repo_name, file_name, content=""):
    repo_path = BASE_DIR / repo_name
    if not repo_path.exists():
        return f"El repositorio '{repo_name}' no existe."
    
    file_path = repo_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return f"Archivo '{file_name}' creado en '{repo_name}'."

def commit(repo_name, message):
    repo_path = BASE_DIR / repo_name
    if not repo_path.exists():
        return f"El repositorio '{repo_name}' no existe."
    
    commit_file = repo_path / "commits.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(commit_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    
    return f"Commit realizado en '{repo_name}': {message}"

def list_repos():
    return [d.name for d in BASE_DIR.iterdir() if d.is_dir()]
