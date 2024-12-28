# small-tools
A collection of small, useful tools and scripts designed to automate tasks, solve everyday problems, or experiment with new ideas. These lightweight projects are quick to build and perfect for personal use or as learning resources.

### List of Tools:

1. **[Medium Scraper](#1-medium-scraper)**
   A script to scrape author information and article titles from Medium using the ScraperAPI service.

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
