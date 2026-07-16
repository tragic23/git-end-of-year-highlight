'''
This code was generated with gemini with this prompt 

how do i just write a query that gets list of all users repos?

***********************************
This was all for learning purposes.
***********************************

'''

import os
import requests

GITHUB_TOKEN = "ghp_"
USERNAME = "tragic23"

url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

#TODO Learn how to graphql
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

# TODO What is cursor doing here?
def get_all_repositories(username):
    repositories = []
    has_next_page = True
    cursor = None
    
    while has_next_page:
        variables = {"username": username, "cursor": cursor}

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        # Check for errors in the response
        if response.status_code != 200:
            raise Exception(f"Query failed: {response.status_code}\n{response.text}")
            
        data = response.json()
        repo_data = data['data']['user']['repositories']
        
        # Add current page of repos to our list
        repositories.extend(repo_data['nodes'])
        
        # Check if there are more repos to fetch
        has_next_page = repo_data['pageInfo']['hasNextPage']
        cursor = repo_data['pageInfo']['endCursor']
        
    return repositories

# Execute
all_repos = get_all_repositories(USERNAME)
print(f"Found {len(all_repos)} repositories:")
for repo in all_repos:
    privacy = "Private" if repo['isPrivate'] else "Public"
    print(f"- {repo['nameWithOwner']} ({privacy})")