import logging
import os
from utilities import Constants, Utilities
import git

def get_latest_file_and_commit_sha(self, image_category_folder, image_name=None):
        
    images = {}
    #create the full path from present working directory and the image category folder
    image_category_folder = os.path.join(os.getcwd(), image_category_folder)
    #check if image_category_folder exists if not throw error
    if not os.path.exists(image_category_folder):
        self.logger.error(f"Provided image category folder '{image_category_folder}' does not exist.")
        return None
    # Initialize a Git repository object, traverse to find the git repo
    repo = git.Repo(search_parent_directories=True)
    self.logger.debug(f"Found git repo working directory: {repo.working_dir} and git directory: {repo.git_dir}")

    if(image_name == None):
        self.logger.info(f"Running the logic to identify all images in category folder: {image_category_folder}")
        for root, dirs, files in os.walk(image_category_folder):
            self.logger.debug(f"Details root {root},dirs {dirs}, files {files}")
            if root == image_category_folder:
                #skip to next when root folder is same as category folder
                continue

            if files:
                # Sort the git files by modification time and get the latest one
                git_files = sorted(repo.git.ls_files(root).splitlines(), key=lambda f: repo.git.log(f, n=1, format="%at"), reverse=True)
                latest_file = git_files[0] if git_files else None
                self.logger.info(f"latest file in git is '{latest_file}' in '{root}'")
                # Get the commit SHA of the latest file

                #latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(root, f))) 
                #self.logger.info(f"latest file is '{latest_file}' in '{root}'")

                # Get the commit SHA of the latest file
                commit_sha = repo.git.rev_parse(f":{latest_file}")

                self.logger.info(f"commit sha for file '{latest_file}' is {commit_sha}")
                # Store the latest file commit SHA for each image directory
                images[os.path.relpath(root,image_category_folder)] = (latest_file, commit_sha)
