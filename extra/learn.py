'''
Make a GraphQL query to get info like number of commit, 
what day, commit messege, repos created, PRs 
Then print out the raw data to understand and be able to mutliate 
the date request to then print it into the # file name and # of commits, 
# of PRs, # of issues, # of reviews,

'''



import os
import argparse
import json
import asyncio
import requests
from gql import Client, gql 
from gql.transport.aiohttp import AIOHTTPTransport



GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  
USERNAME = os.getenv("USERNAME")

url = "https://api.github.com/graphql"
header = {"Authorization": f"Bearer {GITHUB_TOKEN}"}


my_query = gql("""
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
        commitContributionsByRepository(maxRepositories: 10) {  

          repository {
            nameWithOwner
          }
          contributions {
            totalCount
          }
        }
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {            
          
            contributionCount
            date
          }
        }
      }
    }
  }
}
""")
def get_contributions(username):
    transport = AIOHTTPTransport(url, headers=header)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute the query
    result = client.execute(my_query, variable_values={"username": username})
    return result   

def main():
    contributions = get_contributions(USERNAME)
    parser = argparse.ArgumentParser(description="Fetch GitHub contributions and write output to a file")
    parser.add_argument("--out", "-o", help="Output file to write results to", default="output.json")
    args = parser.parse_args()

    out_path = args.out
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(contributions, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to write output to {out_path}: {e}")
    else:
        print(f"Wrote contributions to {out_path}")

if __name__ == "__main__":
    main()
