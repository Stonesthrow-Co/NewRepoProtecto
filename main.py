import markdown
import json, os, pprint

import werkzeug.exceptions
from flask import Flask, request
from github import Github
import markdown.extensions.fenced_code




app = Flask(__name__)

# Environment variables that contain GitHub API keys.
env_vars = {
    "GITHUB_TOKEN": os.getenv('GITHUB_TOKEN')
}



# todo: remove this, just for debugging
pprint.pprint(env_vars)

# Setup GitHub Access
github = Github(env_vars['GITHUB_TOKEN'])

#
# for repo in github.get_user().get_repos():
#     print(repo.name)



@app.route("/")
def index():
    """
    Reads in the README.md file and returns it rendered as HTML.
    :return: [string] HTML rendering of the README.md file
    """
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string


@app.route("/webhook/repo", methods=['POST'])
def repo_create():
    """

    """
    response = {
        "error": False,
        "message": ""
    }

    # validate the payload
    payload = request.json

    if payload.get('action') == "created":
        if not payload.get('repository'):
            response = {
                "error": True,
                "message": f"Repo_Created payload missing 'repository' data.",
            }
            return json.dumps(response), 500

        else:
            error_message = protect_repo_branch(
                repo_name=payload.get('name'),
                branch_name=payload.get('default_branch'),
                repo_id=payload.get('id'),
            )

            if not error_message:
                response['message'] = "Repo protection turned on"
            else:
                response['error'] = True
                response['message'] = error_message

    else:
        response = {
            "error": True,
            "message": f"Unexpected webhook action sent: {payload.get('action', 'NO ACTION')}",
        }
        return json.dumps(response), 500


    status_code = 500 if response['error'] else 200
    return json.dumps(response), status_code


def protect_repo_branch(repo_name, branch_name, repo_id):
    """
    Given a github repo and branch, check for existence, then protect the branch, and post a message to a new issue.
    """
    repo = github.get_repo(repo_name)
    if not repo:
        return f"Could not find repo with name: {repo_name}"

    branch = repo.get_branch(branch_name)
    if not branch:
        return f"Could not find branch with name: {branch_name}"

    branch.edit_protection()


    return ""



@app.route("/repo_list")
def repo_list():
    """
    Returns a list of repos
    """
    repo_list = ""
    for repo in github.get_user().get_repos():
        repo_list += f"<li>{repo.name}</li>\n"

    response = f"""
        <h1>Your Organization's Repos</h1>    
        <ul>{repo_list}</ul>
    """


    return response
if __name__ == "__main__":
    app.run()
