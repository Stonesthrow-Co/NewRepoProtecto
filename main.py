import markdown
import hmac
import hashlib
import json
import os
import pprint

from flask import Flask, request, jsonify
from github import Github
import markdown.extensions.fenced_code
from config import Config

config = Config()

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
    error_message = validate_signature(request, config.app_secret)

    if error_message:
        response = {
            "error": True,
            "message": f"Webhook Error: {error_message}",
        }
        return jsonify(response), 500



    # validate the payload
    payload = request.json

    if payload.get('action') == "created":
        # For "created" actions on the "repo" event
        if not payload.get('repository'):
            # Not provided with a repository name in the payload
            response = {
                "error": True,
                "message": f"Repo_Created payload missing 'repository' data.",
            }
            return jsonify(response), 500

        else:
            # Perform actions on the repo
            json.dumps(payload, indent=2)
            repo = payload.get('repository', {})
            error_message = protect_repo_branch(
                repo_name=repo.get('full_name'),
                branch_name=repo.get('default_branch'),
                repo_id=repo.get('id'),
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
        return jsonify(response), 500


    status_code = 500 if response['error'] else 200
    return jsonify(response), status_code

def validate_signature(request, secret):

    sig_header = request.headers.get('X-Hub-Signature')
    if not sig_header:
        return "Invalid signature"

    sig_type, sig_received = sig_header.split('=')
    if sig_type != 'sha1':
        return "Invalid signature"

    sig_local = hmac.new(
        config.app_secret.encode('utf-8'),
        digestmod=hashlib.sha1,
        msg=request.body.encode('utf-8'),
    ).hexdigest()

    if not hmac.compare_digest(sig_local, sig_received):
        return "Invalid signature - no match"
    else:
        return ""



    # Get the signature from the payload
    signature_header = payload['headers']['X-Hub-Signature']
    sha_name, github_signature = signature_header.split('=')
    if sha_name != 'sha256':
        print('ERROR: X-Hub-Signature in payload headers was not sha256=****')
        return False

    # Create our own signature
    body = payload['body']
    local_signature = hmac.new(secret.encode('utf-8'), msg=body.encode('utf-8'), digestmod=hashlib.sha1)

    # See if they match
    return hmac.compare_digest(local_signature.hexdigest(), github_signature)

def protect_repo_branch(repo_name, branch_name, repo_id):
    """
    Given a github repo and branch, check for existence, then protect the branch, and post a message to a new issue.
    """
    print(f"""
        repo_name: {repo_name}
        branch_name: {branch_name}    
    """)
    repo = github.get_repo(repo_name)
    if not repo:
        return f"Could not find repo with name: {repo_name}"

    branch = repo.get_branch(branch_name)
    if not branch:
        return f"Could not find branch with name: {branch_name}"


    protection = config.protection_default
    branch.edit_protection(
        strict=protection['required_status_checks_strict'],
        contexts=protection['required_status_checks_contexts'],
        enforce_admins=protection['enforce_admins'],
        dismiss_stale_reviews=protection['dismiss_stale_reviews'],
        require_code_owner_reviews=protection['require_code_owner_reviews'],
        required_approving_review_count=protection['required_approving_review_count'],
        user_push_restrictions=protection['push_restrictions_users'],
        team_push_restrictions=protection['push_restrictions_team'],
        dismissal_users=protection['dismissal_restrictions_users'],
        dismissal_teams=protection['dismissal_restrictions_teams'],
    )

    # Mention User in issue

    body = ""
    for key in protection.keys():
        body += f'{key}: {protection[key]}\n'

    body = f"The following branch protection options were set by {config.app_name}:\n```{body}```\n@{config.mention_user_in_issue}"

    repo.create_issue(
        title="Branch protection has been set",
        body=body
    )



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
