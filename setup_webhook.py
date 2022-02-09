"""
    Author: Steve Gongage (steve@gongage.com)
    Created: 2/4/2022
    Purpose:
        To be used for initial setup of your organization's webhooks.
        Create a webhook for a given organization that sends specific types events to a given webhook url.
        For now, this only creates a webhook for "repository" events.
    Usage:
        Update values in `config.py` for use in this script.  See README.md
"""
from config import Config
from github import Github
import pprint


config = Config()
print('-'*60)
print(f'Org Name:    {config.github_org_name}')
print(f'Webhook URL: {config.public_webhook_url_root}')
print('-'*60)

# Setup GitHub
github = Github(config.github_token)

# Load the target org
org = github.get_organization(config.github_org_name)
if not org:
    raise ValueError(f'Organization "{config.github_org_name}" could not be found')

# The webhook configuration payload - allow
webhook_config_repo_events = {
    "url": f"{config.public_webhook_url_root}{config.public_webhook_path_repo_events}",
    "secret": config.app_secret,
    "insecure_ssl": "1" if config.webhook_insecure_connections_allowed else "0",
    "content_type": "json",
    "accept": "application/vnd.github.v3+json",
}

results = org.create_hook("web", webhook_config_repo_events, ["repository"], active=True)
pprint.pprint(results)




