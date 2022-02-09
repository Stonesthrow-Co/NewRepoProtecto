"""
    Author: Steve Gongage (steve@gongage.com)
    Created: 2/4/2022
    Purpose:
        Config File for ProtectoNewRepo

    Usage:
        Please update the values below as needed for your configuration.
        Some values are expected to be pulled from environment variables.  Because these are sensitive secrets,
        it's best to keep these values outside of clear text in your repo.
        This config could be updated easily to pull these values from AWS Secrets Manager
        or an external secrets source as well.

"""
import os

class Config(object):
    # Name of this app
    app_name = "ProtectoNewRepo"

    # Webhook Allows insecure connections? (changing this requires re-running
    webhook_insecure_connections_allowed = True

    # The endpoint path for webhook repo events
    public_webhook_path_repo_events = "/webhook/repo"


    # default protection - Update these settings to change your default protection
    protection_default = {
        "required_status_checks_strict": True,          # Require branches to be up to date before merging.
        "required_status_checks_contexts": ["checks"],  # The list of status checks to require in order to merge into this branch.
        "enforce_admins": False,                        # Enforce all configured restrictions for administrators. Set to true to enforce required status checks for repository administrators. Set to null to disable.
        "dismiss_stale_reviews": False,                 # Set to true if you want to automatically dismiss approving reviews when someone pushes a new commit.
        "require_code_owner_reviews": False,            # Blocks merging pull requests until code owners review them.
        "required_approving_review_count": 1,           # Specify the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.
        "push_restrictions_users": [],                  # Restrict who can push to the protected branch. User, app, and team restrictions are only available for organization-owned repositories. Set to null to disable.
        "push_restrictions_team": [],                   # Restrict who can push to the protected branch. User, app, and team restrictions are only available for organization-owned repositories. Set to null to disable.
        "dismissal_restrictions_users": [],             # Users who can dismiss
        "dismissal_restrictions_teams": [],             # Teams who can dismiss
    }
    # The public root URL that GitHub Webhook expects to reach your service at.
    # If using ngrok it will look something like this: http://d81d-72-238-137-230.ngrok.io
    public_webhook_url_root = os.getenv('PROTECTONEWREPO_WEBHOOK_URL_ROOT')
    if not public_webhook_url_root:
        raise ValueError("This application requires the environment variable 'PROTECTONEWREPO_WEBHOOK_URL_ROOT' be set.")


    # GITHUB_ORG_NAME - [REQUIRED] Name of the organization
    github_org_name = os.getenv('PROTECTONEWREPO_GITHUB_ORG_NAME')
    if not github_org_name:
        raise ValueError("This application requires the environment variable 'PROTECTONEWREPO_GITHUB_ORG_NAME' be set.")

    # GITHUB_TOKEN - [REQUIRED] Unique token from GitHub
    github_token = os.getenv('PROTECTONEWREPO_GITHUB_TOKEN')
    if not github_token:
        raise ValueError("This application requires the environment variable 'PROTECTONEWREPO_GITHUB_TOKEN' be set.")

    # APP_SECRET - [REQUIRED] This unique code is registered with your GitHub webhook and is used to confirm that the request sent to this application is from an expected source
    app_secret = os.getenv('PROTECTONEWREPO_APP_SECRET')
    if not app_secret:
        raise ValueError("This application requires the environment variable 'PROTECTONEWREPO_APP_SECRET' be set.")

    # User Name - The name of the user to mention in the issue created.  Change this as needed to fit your configuration.
    # If you don't want to mention a user, do not set this environment variable
    mention_user_in_issue = os.getenv('PROTECTONEWREPO_MENTION_USER_IN_ISSUE')
