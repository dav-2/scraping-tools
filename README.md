# scraping-tools
A collection of lightweight web scraping tools focused on gathering and analyzing data from social media and online accounts. These scripts are designed to automate the extraction of useful insights, such as engagement metrics and connections (e.g., followers and follow-back statuses), offering an efficient way to track and manage your online presence. Perfect for self-monitoring, data collection, and experimentation with web scraping techniques.

### List of Tools:

1. **[Medium Scraper](#1-medium-scraper)**
   A script to scrape author information and article titles from Medium using the ScraperAPI service.
2. **[GitHub User Analytics Script](#2-github-user-analytics-script)**
   A script to fetch and analyze detailed information about a GitHub user's repositories, stargazers, and follow status.
3. **[Instagram Unfollowers Checker (Educational Tool)](#3-instagram-unfollowers-checker---educational-tool)** 
   A JavaScript tool that hypothetically identifies Instagram users who are not following you back by comparing your followers and following lists.


---

## 1. Medium Scraper

This Python script allows you to scrape author information and article titles from Medium using the ScraperAPI service. It fetches details about a Medium user's profile, including the author's name, bio, and a list of their articles. The script uses `requests` to send HTTP requests and `BeautifulSoup` to parse the HTML response.

### Features:

- **Fetch author information**: Retrieves the author's name and bio from their Medium profile.
- **List of articles**: Extracts the titles of articles written by the author.
- **ScraperAPI integration**: Uses ScraperAPI for rendering JavaScript and bypassing Medium's anti-scraping measures.

### Requirements:

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- ScraperAPI account and API key

### How to Use:

1. Install the required libraries:

    ```bash
    pip install requests beautifulsoup4
    ```

2. Run the script:

    ```bash
    python medium_scraper.py
    ```

3. Enter your ScraperAPI key and the Medium screen name of the author you'd like to scrape.

### Example Output:

Fetching profile information for john_doe...

Author: John Doe Bio: Tech enthusiast and writer on AI and programming.

Articles:

    How AI is Revolutionizing the Tech Industry
    5 Tips for Becoming a Better Programmer
    Understanding Machine Learning Algorithms



### Note:

- The script requires an active ScraperAPI key for fetching data.


### Disclaimer

This script is intended for educational and personal use only. By using this tool, you acknowledge that you are responsible for ensuring compliance with Medium's [Terms of Service](https://medium.com/policy/).

The author of this repository does not assume any liability for potential legal issues, account bans, or other consequences arising from the use of this script. It is your responsibility to review and adhere to Medium's terms and policies, particularly those related to scraping and automation.

Please use this tool responsibly and at your own risk.  

---

## 2. GitHub User Analytics Script

This Python script allows you to fetch and analyze detailed information about a GitHub user's repositories, stargazers, and follow status. It retrieves data such as repository names, star counts, stargazers, and the comparison of followers and following lists. The script uses the `requests` library to send HTTP requests and `BeautifulSoup` for parsing HTML responses.

### Features:

- **Fetch repositories**: Retrieves the list of repositories for a GitHub user, including the star count for each repository.
- **Retrieve stargazers**: Concurrently fetches the list of stargazers for each repository, handling paginated results.
- **Check follow status**: Compares the follower and following lists to identify users who are not following back and users that the account doesn't follow back.
- **GitHub API rate limit check**: Monitors the GitHub API rate limit and displays the remaining requests and reset time.

### Requirements:

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `concurrent.futures` module (built-in Python module)

### How to Use:

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

### Example Output:

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

### Note:

- The script checks the GitHub API rate limit before fetching data. If the rate limit is exceeded, it will show a warning along with the time when the limit will reset.
- The script uses concurrent requests to fetch stargazer data, making it efficient even for users with many repositories.

### Disclaimer:

This script is intended for educational and personal use only. By using this tool, you acknowledge that you are responsible for ensuring compliance with GitHub's [Terms of Service](https://docs.github.com/en/github/site-policy/github-terms-of-service).

The author of this repository does not assume any liability for potential legal issues, account bans, or other consequences arising from the use of this script. It is your responsibility to review and adhere to GitHub's terms and policies, particularly those related to scraping and automation.

Please use this tool responsibly and at your own risk.  

---

## 3. Instagram Unfollowers Checker - Educational Tool

This JavaScript code is **strictly intended for educational purposes only**, to learn JavaScript, DOM manipulation, and web scraping. It would hypothetically allow you to identify users who are not following you back on Instagram. The script automates the process of comparing your followers and the accounts you follow to determine "non-followers." It leverages JavaScript's DOM manipulation capabilities and asynchronous operations to interact with Instagram's web interface. **It is not meant to be used directly on Instagram’s website, and must never be run on Instagram or any other live platform.**

### Features

- **Automated Followers and Following Comparison (Hypothetically)**  
  - Fetches the list of users who follow you.  
  - Fetches the list of users you are following.  
  - Identifies accounts that you follow but are not following you back.  

- **Dynamic DOM Interaction (Hypothetically)**  
  - Waits for specific elements to appear in the DOM using utility functions.  
  - Handles Instagram's dynamically rendered content (e.g., infinite scrolling).  

- **De-duplication (Hypothetically)**  
  - Outputs a distinct list of non-followers.  

### Limitations

1. **Imperfect Results**:  
   The script's results may not have been perfectly accurate due to the complexity of Instagram's DOM.

2. **Multiple Runs**:  
   Running the script more than once in a short period may have caused failures due to Instagram's anti-bot measures.  

3. **Login Dependency**:  
   The script assumes you would be logged into Instagram on your browser. **Again, this script is not intended for use directly on Instagram’s platform, so refrain from attempting to use it there.**

### Requirements

- A modern web browser with developer tools.  
- Basic knowledge of how to run scripts in the browser console.  

### How it Would Be Used

1. **You Would Open Instagram**  
   - You would hypothetically log in to your Instagram account.  
   - Navigate to your profile page.  

2. **You Would Access Developer Tools**  
   - You would hypothetically press `Ctrl + Shift + I` (Linux/Windows) or `Cmd + Option + I` (Mac) to open the developer tools.  
   - Go to the **"Console"** tab.  

3. **You Would Run the Script**  
   - You would hypothetically copy the entire script into the console and press **Enter**.  

4. **You Would Wait for Results**  
   - The script would hypothetically fetch the lists of followers and following, compare them, and display the usernames of those not following you back.  

### Example Output

Users who are not following back:  
`['username1', 'username2', 'username3']`

### Disclaimer

This script is intended strictly for **educational use only**. By using this tool, you acknowledge the following:

- **Compliance**  
  You are solely responsible for ensuring compliance with Instagram's Terms of Service, Community Guidelines, and any applicable laws. **Do not use this script on Instagram or any other live platform.**

- **Assumption of Risk**  
  The author assumes no liability for account bans, legal issues, or any other consequences arising from the use of this script.

- **No Warranties**  
  The script is provided "as is" without guarantees of accuracy or functionality.

### Important Notes

- **Limitations**  
  Instagram’s dynamic DOM and anti-bot measures may have resulted in incomplete or inaccurate data, or caused the script to stop working.

- **Personal Responsibility**  
  By using this script, you agree that you are solely responsible for any consequences resulting from its use. The author will not provide support for bypassing Instagram’s security measures or any issues resulting from misuse. **This script must not be used on Instagram or any other live platform, and doing so may result in adverse consequences.**

- **Intended Purpose**  
  This script is a **learning tool** for understanding JavaScript, DOM manipulation, and asynchronous programming. It is not designed or endorsed for real-world use or violation of any platform policies, and you must avoid using it on Instagram or any other social platform.  

The author of this tool does not condone or endorse its misuse in any way, nor will the author provide assistance or accept responsibility for any consequences arising from such misuse.
