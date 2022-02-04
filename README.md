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

