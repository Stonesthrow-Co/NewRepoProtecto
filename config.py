import os

class Config(object):
    app_name = "NewRepoProtecto"

    # The name of the user to mention in the issue created.  Change this as needed to fit your configuration.
    mention_user_in_issue = os.getenv('NEWREPOPROTECTO_MENTION_USER_IN_ISSUE', "therealsteveg")

    # The public root URL that GitHub Webhook expects to reach your service at
    public_webhook_url_root = "http://d81d-72-238-137-230.ngrok.io"

    # default protection - Update these settings to change your default protection
    protection_default = {
        "required_status_checks_strict": True,          # Require branches to be up to date before merging.
        "required_status_checks_contexts": ["checks"],  # The list of status checks to require in order to merge into this branch.
        "enforce_admins": False,                        # Enforce all configured restrictions for administrators. Set to true to enforce required status checks for repository administrators. Set to null to disable.
        "dismiss_stale_reviews": False,                 # Set to true if you want to automatically dismiss approving reviews when someone pushes a new commit.
        "require_code_owner_reviews": False,            # Blocks merging pull requests until code owners review them.
        "required_approving_review_count": 1,           # Specify the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.
        "push_restrictions_users": [],                # Restrict who can push to the protected branch. User, app, and team restrictions are only available for organization-owned repositories. Set to null to disable.
        "push_restrictions_team": [],                 # Restrict who can push to the protected branch. User, app, and team restrictions are only available for organization-owned repositories. Set to null to disable.
        "dismissal_restrictions_users": [],           # Users who can dismiss
        "dismissal_restrictions_teams": [],           # Teams who can dismiss
    }

    github_org_name = os.getenv('NEWREPOPROTECTO_GITHUB_ORG_NAME')
    if not github_org_name:
        raise ValueError("This application requires the environment variable 'NEWREPOPROTECTO_GITHUB_ORG_NAME' be set.")

    # GITHUB_TOKEN - Unique token
    github_token = os.getenv('NEWREPOPROTECTO_GITHUB_TOKEN')
    if not github_token:
        raise ValueError("This application requires the environment variable 'NEWREPOPROTECTO_GITHUB_TOKEN' be set.")

    # APP_SECRET - This unique code is registered with your GitHub webhook and is used to confirm that the request sent to this application is from an expected source
    app_secret = os.getenv('NEWREPOPROTECTO_APP_SECRET')
    if not app_secret:
        raise ValueError("This application requires the environment variable 'NEWREPOPROTECTO_APP_SECRET' be set.")
