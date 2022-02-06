# ProtectoNewRepo
A simple web service that listens for organization events to know when a repository has been created. 
When the repository is created, the main branch is automatically protected. 
An issue is then created on the new repo with a mention of your github user that outlines the protections that were added.

>
> **A Note About Security:**
>
> This prototype will not use SSL encrypted communication to receive the webhook request from GitHub.   
> In a production environment, your web server should be secured behind SSL.  
> If you're unfamiliar with SSL, a great place to start is with [Let's Encrypt](https://letsencrypt.org/getting-started/).


## First Time Setup

*You will need the following to get started:*
- Python 3.8 or higher
- A [GitHub Personal Access Token](https://github.com/settings/tokens) that has access to your organization
- An environment exposed to the internet and able to receive webhook requests from GitHub
  - See [ngrok](https://ngrok.com/download) - Easily exposes your development environment ports to the internet so you can receive webhook requests.
 
### First Time Setup
After cloning this repo, run the following commands to get your code up and running

```bash

# create a virtual environment
$ python3 -m venv venv

# install requirements
$ pip3 install -r requirements.txt

# Set your environment variables
$ export PROTECTONEWREPO_GITHUB_TOKEN=my_github_token
$ export PROTECTONEWREPO_GITHUB_ORG_NAME=Stonesthrow-Co
$ export PROTECTONEWREPO_APP_SECRET=my_app_secret
$ export PROTECTONEWREPO_MENTION_USER_IN_ISSUE=my_github_user_name
$ export FLASK_APP=main

# Start Flask
$ flask run

# Optional (if using ngrok. Be sure to use the same port that Flask is listening on)
$ ngrok http 5000

```



## References and Further Info

- [GitHub: Creating Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)
- [GitHub API: Github Objects](https://pygithub.readthedocs.io/en/latest/github_objects.html)
- [GitHub REST API: Repos](https://docs.github.com/en/rest/reference/repos)
- [GitHub: Setting Personal Access Tokens](https://github.com/settings/tokens)
- [GitHub API and Python](https://martinheinz.dev/blog/25)