"""
GitHub Wrapped
==============
Generates an end-of-year highlight reel of a user's GitHub activity:

- Total commits, PRs, issues, and reviews
- Number of repositories contributed to
- Busiest month of the year
- Single-day contribution peak
- Top repositories by commit count

Requires a GitHub personal access token with read access to contribution data.


==============
Cluade code
ONLY LEARNING PURPOSE
==============
"""

import os
from collections import defaultdict
from datetime import datetime
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")   # Or paste your token string here directly
USERNAME = os.getenv("USERNAME")          # Replace with your GitHub username
YEAR = 2026                               # The year you want to highlight

GRAPHQL_URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Fetches total commits, PRs, issues, repository breakdowns, and daily calendar data
GRAPHQL_QUERY = """
query($username: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $username) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions

      # Top repositories by commit count
      commitContributionsByRepository(maxRepositories: 10) {
        repository {
          nameWithOwner
        }
        contributions {
          totalCount
        }
      }

      # Calendar data used to calculate busiest months / days
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
"""


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_github_data(username: str, year: int) -> dict:
    """Query the GitHub GraphQL API for a user's contribution data in a given year."""

    variables = {
        "username": username,
        "from": f"{year}-01-01T00:00:00Z",
        "to": f"{year}-12-31T23:59:59Z",
    }

    response = requests.post(
        GRAPHQL_URL,
        json={"query": GRAPHQL_QUERY, "variables": variables},
        headers=HEADERS,
    )

    if response.status_code != 200:
        raise Exception(
            f"Query failed with status code {response.status_code}: {response.text}"
        )

    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    print(data)
    return data["data"]["user"]["contributionsCollection"]


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------

def get_monthly_breakdown(weeks: list) -> tuple[dict, int, str]:
    """
    Walk the contribution calendar and return:
      - a dict of {month_name: total_contributions}
      - the highest single-day contribution count
      - a human-readable label for that best day
    """

    monthly_contributions = defaultdict(int)
    max_single_day_commits = 0
    best_day_label = ""

    for week in weeks:
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            date = datetime.strptime(day["date"], "%Y-%m-%d")

            monthly_contributions[date.strftime("%B")] += count

            if count > max_single_day_commits:
                max_single_day_commits = count
                best_day_label = date.strftime("%A, %B %d")

    return monthly_contributions, max_single_day_commits, best_day_label


def get_busiest_month(monthly_contributions: dict) -> tuple[str, int]:
    """Return the (month_name, count) with the most contributions, or a fallback if empty."""

    if not monthly_contributions:
        return "None", 0

    return max(monthly_contributions.items(), key=lambda item: item[1])


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_wrapped_summary(data: dict, username: str, year: int) -> None:
    """Print a formatted 'Wrapped'-style summary of the user's GitHub activity."""

    # --- Headline stats -----------------------------------------------
    total_commits = data["totalCommitContributions"]
    total_prs = data["totalPullRequestContributions"]
    total_issues = data["totalIssueContributions"]
    total_reviews = data["totalPullRequestReviewContributions"]

    repos = data["commitContributionsByRepository"]
    unique_repos_count = len(repos)

    # --- Time-based analysis --------------------------------------------
    weeks = data["contributionCalendar"]["weeks"]
    #print(weeks)
    monthly_contributions, max_single_day_commits, best_day_label = get_monthly_breakdown(weeks)
    busiest_month, busiest_month_count = get_busiest_month(monthly_contributions)

    # --- Print report ------------------------------------------------
    divider = "=" * 50
    sub_divider = "-" * 50

    print(divider)
    print(f"✨  {username.upper()}'S GITHUB WRAPPED {year} ✨")
    print(divider)

    print(f"📝 Total Commits:             {total_commits}")
    print(f"🔀 Pull Requests Opened:      {total_prs}")
    print(f"🐞 Issues Raised:             {total_issues}")
    print(f"👀 Pull Requests Reviewed:    {total_reviews}")
    print(f"📦 Unique Repos Contributed:  {unique_repos_count}")
    print(sub_divider)

    print(f"📅 Busiest Month:             {busiest_month} ({busiest_month_count} contributions)")
    if max_single_day_commits > 0:
        print(f"🏆 Single Day Peak:           {max_single_day_commits} contributions on {best_day_label}!")
    print(sub_divider)

    print("🔥 TOP REPOSITORIES BY COMMITS:")
    if repos:
        for i, repo_data in enumerate(repos[:3], start=1):  # Top 3
            repo_name = repo_data["repository"]["nameWithOwner"]
            commits = repo_data["contributions"]["totalCount"]
            print(f"  {i}. {repo_name} ({commits} commits)")
    else:
        print("  No public commit data found for this period.")

    print(divider)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not GITHUB_TOKEN:
        raise ValueError(
            "Please set your GITHUB_TOKEN environment variable, or paste it directly in the script."
        )

    try:
        print(f"Fetching GitHub data for {USERNAME}...")
        raw_data = fetch_github_data(USERNAME, YEAR)
        print_wrapped_summary(raw_data, USERNAME, YEAR)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()