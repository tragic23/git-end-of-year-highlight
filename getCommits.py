'''
after generate code to get list of repos, 
this code will grab a user commit history 
It will use the GitHub GraphQL API to fetch commit history for a given user across their repositories.

'''

import os
import requests
GITHUB_TOKEN = "ghp_"
USERNAME = "tragic23"

url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

query = """
query($username: String!, $cursor: String) {
  user(login: $username) {
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        nameWithOwner
        isPrivate
      }
    }
  }
}
"""

