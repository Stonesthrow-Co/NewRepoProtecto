"""
    Author: Steve Gongage (steve@gongage.com)
    Created: 2/4/2022
    Purpose: Create a webhook for a given organization that sends all repository events to a given webhook url
    Usage: see README.md
"""
from config import Config
from github import Github
import pprint
import requests


config = Config()
print('-'*60)
print(f'Org Name:    {config.github_org_name}')
print(f'Webhook URL: {config.public_webhook_url_root}')
print('-'*60)

# Setup GitHub
github = Github(config.github_token)

# Get our target org
org = github.get_organization(config.github_org_name)
if org:
    pprint.pprint(org)



webhook_config = {
    "url": f"{config.public_webhook_url_root}/webhook/repo",
    "secret": config.app_secret,
    "insecure_ssl": "1",
    "content_type": "json",
    "accept": "application/vnd.github.v3+json",
}
webhook_events = ["repository"]

results = org.create_hook("web", webhook_config, webhook_events, active=True)
pprint.pprint(results)

# for org in :
#     pprint.pprint(org)



