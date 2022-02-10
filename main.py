"""
    Author: Steve Gongage (steve@gongage.com)
    Created: 2/4/2022
    Purpose:
        Main flask application.  See README.md for more info
    Usage:

"""
import markdown
import hmac
import hashlib

from flask import Flask, request, jsonify, abort
from github import Github, GithubException
from github.GithubException import UnknownObjectException
import markdown.extensions.fenced_code
from config import Config

config = Config()

app = Flask(__name__)

# Setup GitHub Access
github = Github(config.github_token)

# Route: Index
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

# Route: webhook/repo
@app.route("/webhook/repo", methods=['POST'])
def repo_create():
    """
    Webhook endpoint for 'repository' events
    Valid Actions: ["created"]
    """

    # Make sure the incoming request comes from a 'repository' event
    if request.headers.get('X-GitHub-Event') == 'ping':
        # A ping event is ok.  That's just GitHub checking if this endpoint is valid.
        return jsonify({
            "error": False,
            "message": f"Pong"
        }), 200

    elif request.headers.get('X-GitHub-Event') != 'repository':
        # Unexpected github event calling this webhook
        return jsonify({
            "error": True,
            "message": f"Webhook Error: Invalid event '{request.headers.get('X-GitHub-Event')}'",
        }), 500

    # Validate the signature of the webhook to make sure we're receiving a legitimate webhook request
    error_message = validate_signature(request)
    if error_message:
        # Error validating the signature
        return jsonify({
            "error": True,
            "message": f"Webhook Error: {error_message}",
        }), 500

    # get the JSON payload from the request
    payload = request.json

    # Handle the payload based on the "action"
    if payload.get('action') == "created":
        # For "created" actions on the "repo" event

        if not payload.get('repository'):
            # Not provided with repository data in the payload
            return jsonify({
                "error": True,
                "message": f"Repo_Created payload missing 'repository' data.",
            }), 500

        else:
            # Perform actions on the repo
            repo = payload.get('repository', {})


            try:
                error_message = protect_repo_branch(
                    repo_name=repo.get('full_name'),
                    branch_name=repo.get('default_branch'),
                )
            except UnknownObjectException as ex:
                # GitHub returned an UnknownObjectException which likely means we could not edit the default branch

                # Todo: return to this and create a better solution
                # This is a temporary hack that needs a better solution
                # Sometimes the repo payload includes a default branch name for a branch that doesn't actually exist.
                # This seems to be particularly true at the start of a new repo, which is when this script runs.
                # Potential fix: reading in a list of existing branches and if the default isn't in there,
                # falling back to a better repo.
                if repo.get('default_branch') != 'main':
                    try:
                        error_message = f"UnknownObjectException occurred when protecting default repo branch '{repo.get('default_branch')}'.  Retrying with 'main' branch in case the default branch doesn't exist"
                        print(error_message, "\n", ex)
                        error_message = protect_repo_branch(
                            repo_name=repo.get('full_name'),
                            branch_name='main',
                        )

                    except Exception as ex:
                        error_message = "Unknown Error occurred when protecting fallback default repo branch 'main'"
                        print(error_message, "\n", ex)
                else:
                    error_message = f"UnknownObjectException occurred when protecting default repo branch '{repo.get('default_branch')}'."
                    print(error_message, "\n", ex)


            except Exception as ex:
                error_message = f"Unexpected error occurred when protecting fallback default repo branch '{repo.get('default_branch')}'"
                print(error_message, "\n", ex)

            if not error_message:
                # Completed successfully
                return jsonify({
                    "error": False,
                    "message": "Repo protection turned on"
                }), 200

            else:
                # Error during the protection process
                return jsonify({
                    "error": True,
                    "message": error_message
                }), 500

    else:
        # Error - unexpected webhook action
        return jsonify({
            "error": True,
            "message": f"Unexpected webhook action sent: {payload.get('action', 'NO ACTION FOUND')}",
        }), 500


def validate_signature(request):
    """
    Compare the signature received by a web hook request against our stored app secret.
    This is how we protect our endpoint and make sure we're only handling valid signatures.
    In production, expand upon this and provide logging for observability layer.
    """

    if 'X-Hub-Signature-256' not in request.headers:
        # missing a vital header
        return "Invalid signature - not provided"

    # get the body of the webhook request
    payload = request.data

    # get the signature from the webhook request header
    signature = request.headers['X-Hub-Signature-256']

    # encode our known secret to a byte array
    secret = config.app_secret.encode()

    # hmac generator - hash that payload using our local secret and sha256
    hmac_generator = hmac.new(secret, payload, hashlib.sha256)

    # add expected prefix and hex digest
    local_digest = "sha256=" + hmac_generator.hexdigest()
    # use secure comparison to see if what we receive matches what is expected
    if not hmac.compare_digest(local_digest, signature):
        return "Invalid signature - no match"
    else:
        return ""


def protect_repo_branch(repo_name, branch_name):
    """
    Given a github repo and branch, check for existence, then protect the branch, and post a message to a new issue.
    """
    print(f"""
        repo_name: {repo_name}
        branch_name: {branch_name}    
    """)

    # Validate repo exists
    repo = github.get_repo(repo_name)
    if not repo:
        return f"Could not find repo with name: {repo_name}"
    print(f"Repo found: {repo_name}")

    # Validate branch exists
    branch = repo.get_branch(branch_name)
    if not branch:
        return f"Could not find branch with name: {branch_name}"
    print(f"Branch found: {branch.name}")

    # Get the protection configuration from config
    protection = config.protection_default

    # Update the branch's protection
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

    # Now that the branch is protected, we need to create an Issue and mention the user

    # Easy to read list of branch protections for the issue body
    config_list = ""
    for key in protection.keys():
        config_list += f'{key}: {protection[key]}\n'

    # Add a little context to the top
    body = f"The following branch protection options were set by _{config.app_name}_:\n```{config_list}```"
    if config.mention_user_in_issue:
        # if a user needs to be mentioned, include them at the end.
        body += f"\n@{config.mention_user_in_issue}"

    # Create the issue in this repo
    repo.create_issue(
        title="Branch protection has been set",
        body=body
    )

    # Return with no error message = success!
    return ""


@app.route("/repo_list")
def repo_list():
    """
    Returns a list of repos for the configured org if you hit the endpoint.
    This is available for convenience and can safely be removed if needed
    """
    response_body = ""
    for repo in github.get_user().get_repos():
        response_body += f"<li>{repo.name}</li>\n"

    response = f"""
        <h1>Repos for GitHub Org: {config.github_org_name}</h1>    
        <ul>
            {response_body}
        </ul>
        <p><a href="https://github.com/Stonesthrow-Co/NewRepoProtecto">Protecto New Repo</a></p>
    """
    return response


if __name__ == "__main__":
    app.run()
