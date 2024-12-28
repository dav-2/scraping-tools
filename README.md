# small-tools
A collection of small, useful tools and scripts designed to automate tasks, solve everyday problems, or experiment with new ideas. These lightweight projects are quick to build and perfect for personal use or as learning resources.

### List of Tools:

1. **[Medium Scraper](#1-medium-scraper)**
   A script to scrape author information and article titles from Medium using the ScraperAPI service.
2. **[GitHub User Analytics Script](#2-github-user-analytics-script)**
   A script to fetch and analyze detailed information about a GitHub user's repositories, stargazers, and follow status.


---

### 1. Medium Scraper

This Python script allows you to scrape author information and article titles from Medium using the ScraperAPI service. It fetches details about a Medium user's profile, including the author's name, bio, and a list of their articles. The script uses `requests` to send HTTP requests and `BeautifulSoup` to parse the HTML response.

#### Features:

- **Fetch author information**: Retrieves the author's name and bio from their Medium profile.
- **List of articles**: Extracts the titles of articles written by the author.
- **ScraperAPI integration**: Uses ScraperAPI for rendering JavaScript and bypassing Medium's anti-scraping measures.

#### Requirements:

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- ScraperAPI account and API key

#### How to Use:

1. Install the required libraries:

    ```bash
    pip install requests beautifulsoup4
    ```

2. Run the script:

    ```bash
    python medium_scraper.py
    ```

3. Enter your ScraperAPI key and the Medium screen name of the author you'd like to scrape.

#### Example Output:

Fetching profile information for john_doe...

Author: John Doe Bio: Tech enthusiast and writer on AI and programming.

Articles:

    How AI is Revolutionizing the Tech Industry
    5 Tips for Becoming a Better Programmer
    Understanding Machine Learning Algorithms



#### Note:

- The script requires an active ScraperAPI key for fetching data.


#### Disclaimer

This script is intended for educational and personal use only. By using this tool, you acknowledge that you are responsible for ensuring compliance with Medium's [Terms of Service](https://medium.com/policy/).

The author of this repository does not assume any liability for potential legal issues, account bans, or other consequences arising from the use of this script. It is your responsibility to review and adhere to Medium's terms and policies, particularly those related to scraping and automation.

Please use this tool responsibly and at your own risk.



### 2. GitHub User Analytics Script

This Python script allows you to fetch and analyze detailed information about a GitHub user's repositories, stargazers, and follow status. It retrieves data such as repository names, star counts, stargazers, and the comparison of followers and following lists. The script uses the `requests` library to send HTTP requests and `BeautifulSoup` for parsing HTML responses.

#### Features:

- **Fetch repositories**: Retrieves the list of repositories for a GitHub user, including the star count for each repository.
- **Retrieve stargazers**: Concurrently fetches the list of stargazers for each repository, handling paginated results.
- **Check follow status**: Compares the follower and following lists to identify users who are not following back and users that the account doesn't follow back.
- **GitHub API rate limit check**: Monitors the GitHub API rate limit and displays the remaining requests and reset time.

#### Requirements:

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `concurrent.futures` module (built-in Python module)

#### How to Use:

1. Install the required libraries:

    ```bash
    pip install requests beautifulsoup4
    ```

2. Run the script:

    ```bash
    python github_user_analytics.py
    ```

3. Enter the GitHub username when prompted. The script will then display:
   - A list of repositories with their star counts and stargazer information.
   - A comparison of followers and followings to show who is not following back and who the account is not following back.

#### Example Output:

```bash
Enter your GitHub username: dav-2
```

The script will output details such as:

- **Repositories**: 
  - Repository: repo_name
  - Stars: 3
  - Stargazers: user1, user2, user3
  
- **Follow Status**:
  - Users not following back: user4, user5
  - Followers the account doesn't follow: user6, user7

#### Note:

- The script checks the GitHub API rate limit before fetching data. If the rate limit is exceeded, it will show a warning along with the time when the limit will reset.
- The script uses concurrent requests to fetch stargazer data, making it efficient even for users with many repositories.

#### Disclaimer:

This script is intended for educational and personal use only. By using this tool, you acknowledge that you are responsible for ensuring compliance with GitHub's [Terms of Service](https://docs.github.com/en/github/site-policy/github-terms-of-service).

The author of this repository does not assume any liability for potential legal issues, account bans, or other consequences arising from the use of this script. It is your responsibility to review and adhere to GitHub's terms and policies, particularly those related to scraping and automation.

Please use this tool responsibly and at your own risk.
