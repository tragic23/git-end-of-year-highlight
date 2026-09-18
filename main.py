import os
import asyncio
from git import Commit
import requests
import json
from gql import Client, gql 
from gql.transport.aiohttp import AIOHTTPTransport
from Info import Info
from datetime import datetime


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  


url = "https://api.github.com/graphql"


# Execute
async def main():

  git_token = os.getenv("GITHUB_TOKEN")
 
  info = Info( git_token)

  header = {"Authorization": f"Bearer {info.token}"}

  info = await get_all_commits(info, header)

  print(info)
  


# TODO write method to make a request with query
async def get_all_commits(info: Info, header: dict) -> Info:
    username = getattr(info, "username", None)

    async with Client(
        transport=AIOHTTPTransport(url, headers=header),
        execute_timeout=10,
    ) as session:
        query_obj = gql("""
          query User($login: String!, $from: DateTime, $to: DateTime, $first: Int) {
            user(login: $login) {
              contributionsCollection(from: $from, to: $to) {
                commitContributionsByRepository {
                  contributions(first: $first) {
                    totalCount
                  }
                  repository {
                    name
                  }
                }
                contributionCalendar {
                  totalContributions
                  weeks {
                    contributionDays {
                      contributionCount
                      date
                      weekday
                    }
                  }
                }
              }
            }
          }
        """)

        
            
        response = await session.execute(query_obj, variable_values={"login": username,"from": "20"
        "25-01-01T00:42:00Z", "to": "2025-12-31T23:59:00Z" })
        commit_data = response['user']['contributionsCollection']['contributionCalendar']['weeks']

        info = computeDataCommits(info, commit_data)

        # TODO print what commit_data looks like in a json file named getCommits.json
        try: 
          with open("getCommits.json", "w", encoding="utf-8") as f:
            json.dump(commit_data, f, indent=4)
        except Exception:
          pass     
    return info

def computeDataCommits(info: Info, commit_data: dict) -> Info:

  # Compute maxMonth, maxMonthCount, maxDate, maxDateCount, weekendCount
  maxMonth = ""
  maxMonthCount = 0
  maxDate = "Null"
  maxDateCount = 0
  totalCommitCount = 0
  weekendCount = 0
  workWeekendBoolean = False
  monthCnt = 1
  monthCommitCnt = 0

  for week in commit_data:
    for day in week["contributionDays"]:
      totalCommitCount += day["contributionCount"]

      # check max day count
      if day["contributionCount"] > maxDateCount:
           
        maxDateCount = day["contributionCount"]
        maxDate = day["date"]


      # count month commits
      parsed_date = datetime.strptime(day["date"], "%Y-%m-%d")
      if(parsed_date.month == monthCnt):
        monthCommitCnt += day["contributionCount"]
      else:
        if(monthCommitCnt> maxMonthCount):
          maxMonthCount = monthCommitCnt
          maxMonth = monthCnt

        monthCommitCnt = day["contributionCount"]
        monthCnt += 1

      # check set weekend boolean
      if(( day["weekday"] == 0 or day["weekday"] == 6) and day["contributionCount"] > 0):
        workWeekendBoolean = True
    # End Inner For loop

    # check weekend boolean and iterate count
    if (workWeekendBoolean == True):
      weekendCount += 1
      workWeekendBoolean = False
  # End outter For loop      
           

  info.setCommitData(maxMonth, maxMonthCount, maxDate, maxDateCount, totalCommitCount, weekendCount)
  return info
# End computeDataCommits method

    

if __name__ == "__main__":
  asyncio.run(main())