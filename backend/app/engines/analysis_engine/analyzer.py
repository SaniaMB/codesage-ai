from pathlib import Path

class ProjectAnalyzer:
    def get_python_files(self, repository_path: Path):
        return list(repository_path.rglob("*.py"))