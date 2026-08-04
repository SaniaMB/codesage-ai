from git import Repo
from pathlib import Path
import shutil

class ProjectScanner:
    def __init__(self):
        self.repositories_dir = Path("repositories")
        self.repositories_dir.mkdir(exist_ok=True)

    def clone_repository(self, repository_url: str):
        repository_name = repository_url.rstrip("/").split("/")[-1]
        destination = self.repositories_dir / repository_name

        if destination.exists():
            shutil.rmtree(destination)

        Repo.clone_from(repository_url, destination)

        return destination