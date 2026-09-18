'''
This code was generated with gemini with this prompt 

how do i just write a query that gets list of all users repos?

***********************************
This was all for learning purposes.
***********************************

'''

import os
import asyncio
import requests
import json
from gql import Client, gql 
from gql.transport.aiohttp import AIOHTTPTransport


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  
USERNAME = os.getenv("USERNAME")

url = "https://api.github.com/graphql"
header = {"Authorization": f"Bearer {GITHUB_TOKEN}"}


async def get_all_repositories(username):
  repositories = []
  pages = []
  has_next_page = True
  cursor = None
    
  async with Client(
        transport=AIOHTTPTransport(url, headers=header),
        execute_timeout=10,
    ) as session:
        while has_next_page:
            query_obj = gql("""
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
            """)
            # TODO print this query output looks like in a json file named getRepo.json









            response = await session.execute(query_obj, variable_values={"username": username, "cursor": cursor})
            
            repo_data = response['user']['repositories']

            # Add current page of repos to our list
            repositories.extend(repo_data['nodes'])
            pages.append(response)

            # Check if there are more repos to fetch
            has_next_page = repo_data['pageInfo']['hasNextPage']
            cursor = repo_data['pageInfo']['endCursor']
            # TODO print what repositories looks like in a json file named getRepo2.json
            try:
              with open("getRepo2.json", "w") as f2:
                json.dump({"repositories": repositories}, f2, indent=2)
            except Exception:
              pass
        
  # Write the raw page responses and aggregated list to getRepo.json
  try:
    with open("getRepo.json", "w") as f:
      json.dump({"pages": pages, "repositories": repositories}, f, indent=2)
  except Exception:
    pass

  return repositories

# Execute
async def main():
    all_repos = await get_all_repositories(USERNAME)
    print(f"Found {len(all_repos)} repositories:")
    for repo in all_repos:
        privacy = "Private" if repo['isPrivate'] else "Public"
        print(f"- {repo['nameWithOwner']} ({privacy})")

if __name__ == "__main__":
    asyncio.run(main())