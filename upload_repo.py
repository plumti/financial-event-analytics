import os
import logging
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
REPO_NAME = "plumti/crew-ai-financial"
FOLDER_PATH = "/teamspace/studios/this_studio/trading-project-2024/"
TOKEN = os.getenv("GITHUB_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def file_content_different(local_file_path, github_file):
    """
    Function to check if the content of the local file is different from the GitHub file.
    """
    with open(local_file_path, 'rb') as file_data:
        local_content = file_data.read()
    github_content = github_file.decoded_content

    return local_content != github_content

def upload_file_if_different(file_path, repo, remote_path):
    """
    Function to upload a specific file to a GitHub repository if its content is different.
    """
    try:
        contents = repo.get_contents(remote_path)
        if file_content_different(file_path, contents):
            with open(file_path, 'rb') as file_data:
                content = file_data.read()
            repo.update_file(contents.path, f"Updating {remote_path}", content, contents.sha)
            logger.info(f"Updated file: {remote_path}")
        else:
            logger.info(f"No changes detected in the file: {remote_path}")
    except Exception as e:
        if "404" in str(e):
            try:
                with open(file_path, 'rb') as file_data:
                    content = file_data.read()
                repo.create_file(remote_path, f"Creating {remote_path}", content)
                logger.info(f"Created file: {remote_path}")
            except Exception as e:
                logger.error(f"Failed to upload file {remote_path}: {e}")
        else:
            logger.error(f"Error accessing file {remote_path} in the repository: {e}")

def upload_folder_to_github(local_folder, repo, remote_folder=""):
    """
    Function to upload all files in a folder to a GitHub repository.
    """
    for root, _, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_folder)
            remote_path = os.path.join(remote_folder, relative_path).replace("\\", "/")
            upload_file_if_different(local_path, repo, remote_path)

def main_update():
    """
    Main function to initialize GitHub connection and start uploading the folder.
    """
    if not TOKEN:
        logger.error("GitHub token is not set. Please set it in the .env file.")
        return

    g = Github(TOKEN)
    try:
        repo = g.get_repo(REPO_NAME)
    except Exception as e:
        logger.error(f"Failed to access repository {REPO_NAME}: {e}")
        return
  
    upload_folder_to_github(FOLDER_PATH, repo)
    logger.info("Folder upload process completed")

if __name__ == "__main__":
    main_update()
