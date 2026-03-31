from github import Github
import os

g = Github(os.getenv("GITHUB_TOKEN"))

def get_repo_files(repo_name):
    repo = g.get_repo(repo_name)

    files = []

    def get_all_files(contents):
        for content in contents:
            if content.type == "dir":
                get_all_files(repo.get_contents(content.path))
            elif content.type == "file":
                try:
                    files.append((content.name, content.decoded_content.decode()))
                except:
                    pass

    contents = repo.get_contents("")
    get_all_files(contents)

    return files
