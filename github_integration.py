from github import Github
import os

g = Github(os.getenv("GITHUB_TOKEN"))

def get_repo_files(repo_name):
    repo = g.get_repo(repo_name)
    contents = repo.get_contents("")

    files = []

    for content in contents:
        if content.type == "file":
            try:
                files.append((content.name, content.decoded_content.decode()))
            except:
                pass

    return files
