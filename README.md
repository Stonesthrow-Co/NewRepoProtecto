# ProtectoNewRepo

## What Is ProtectoNewRepo? 
A simple web service that listens for organization events to know when a repository has been created. 
When the repository is created, the main branch is automatically protected. 
An issue is then created on the new repo with a mention of your github user that outlines the protections that were added.

>
> **A Note About Security:**
>
> The steps below will not use SSL encrypted communication to receive the webhook request from GitHub.   
> In a production environment, your web server should be secured behind SSL.  
> If you're unfamiliar with SSL, a great place to start is with [Let's Encrypt](https://letsencrypt.org/getting-started/).


### Prerequisites
*You will need the following to get started:*
- Python 3.8 or higher
- A [GitHub Personal Access Token](https://github.com/settings/tokens) that has access to your organization
- An environment exposed to the internet and able to receive webhook requests from GitHub
  - See [ngrok](https://ngrok.com/download) - Easily exposes your development environment ports to the internet so you can receive webhook requests.
 
### First Time Setup
After cloning this repo, run the following commands to get this up and running:

#### Prepare Environment
```bash

# create a virtual environment
$ python3 -m venv venv
# activate the virtual environment
$ source venv/bin/activate

# Optional: update pip version if using an older version
$ pip3 install -U pip
$ pip3 install -U setuptools

# install requirements
$ pip3 install -r requirements.txt

# Set your environment variables (replace the values below with your own)
$ export PROTECTONEWREPO_GITHUB_TOKEN=your_github_token
$ export PROTECTONEWREPO_GITHUB_ORG_NAME=your_github_org_name
$ export PROTECTONEWREPO_APP_SECRET=your_app_secret
$ export PROTECTONEWREPO_MENTION_USER_IN_ISSUE=your_github_user_name
$ export PROTECTONEWREPO_WEBHOOK_URL_ROOT=http://yourwebhookurl
$ export FLASK_APP=main

# Setup your organization's webook
$ python3 setup_webhook.py

# Start Flask
$ flask run

# Optional (if using ngrok. Be sure to use the same port that Flask is listening on)
# Run this in another bash shell on the same machine
$ ngrok http 5000

```




## References and Further Info

- [GitHub: Creating Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)
- [GitHub API: Github Objects](https://pygithub.readthedocs.io/en/latest/github_objects.html)
- [GitHub REST API: Repos](https://docs.github.com/en/rest/reference/repos)
- [GitHub: Setting Personal Access Tokens](https://github.com/settings/tokens)
- [GitHub API and Python](https://martinheinz.dev/blog/25)