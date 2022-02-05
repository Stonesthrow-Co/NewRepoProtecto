import os

class Config(object):

    public_webhook_url_root = "http://d81d-72-238-137-230.ngrok.io"


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
