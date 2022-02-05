# NewRepoProtecto

## Challenge:
Please create a simple web service that listens for organization events to know when a repository has been created. When the repository is created please automate the protection of the main branch. Notify yourself with an @mention in an issue within the repository that outlines the protections that were added.

## Objectives:

- Flask enabled
- Webhook - New Repo Created

Endpoints:

- NewRepoCreated
  - Uses GitHub API to protect the main branch of a new repo
  - Notify yourself with an @mention in an issue within the repo 
    - Include the protections that were added


## How To Use

>
> **About Security:**
>
> This prototype will not use SSL encrypted communication to receive the webhook request from GitHub.  This potentially exposes sensitive info like your app ID .  
> In a production environment, your web server should be secured behind SSL.  If you're unfamiliar with SSL, a great place to start is with [Let's Encrypt](https://letsencrypt.org/getting-started/).






### Setup Environment

You will need:
- Python 3.8 or higher
- A [GitHub Personal Access Token](https://github.com/settings/tokens) that has access to your organization
- An environment exposed to the internet and able to receive webhook requests from GitHub
  - See [ngrok](https://ngrok.com/download) - Easily exposes your development environment ports to the internet so you can receive webhook requests.
- Setup Webhooks
  - GitHub provides a great tutorial on [creating webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks).

### Getting It Running
``` bash

$ export FLASK_APP=main

# replace the value below with your GitHub Private Token 
$ export NEWREPOPROTECTO_GITHUB_TOKEN=AAAAA....BBBBB

```


## References

- [GitHub: Creating Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)
- [GitHub API: Github Objects](https://pygithub.readthedocs.io/en/latest/github_objects.html)
- [GitHub REST API: Repos](https://docs.github.com/en/rest/reference/repos)
- [GitHub: Setting Personal Access Tokens](https://github.com/settings/tokens)
- [GitHub API and Python](https://martinheinz.dev/blog/25)