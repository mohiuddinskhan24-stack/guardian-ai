from github import Github
import os

# 🔐 Load token
g = Github(os.getenv("GITHUB_TOKEN"))

def get_repo_files(repo_name):
    repo = g.get_repo(repo_name)
    files = []

    def fetch(contents):
        for content in contents:
            if content.type == "dir":
                fetch(repo.get_contents(content.path))
            else:
                try:
                    files.append((content.path, content.decoded_content.decode()))
                except:
                    pass

    fetch(repo.get_contents(""))
    return files
