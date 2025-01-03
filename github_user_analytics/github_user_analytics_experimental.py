
import requests 
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

class GithubUser:
    def __init__(self, username):
        """
        Initializes a GithubUser object.
        
        :param username: GitHub username
        """
        self.username = username
        self.url = f"https://api.github.com/users/{username}/repos"
        self.profile_url = f"https://github.com/{username}?tab="

    def fetch_url(self, url):
        """
        Helper method to send a GET request to a URL and handle errors.

        :param url: The URL to request
        :return: JSON response if successful, None if an error occurs
        """
        try:
            response = requests.get(url)
            # Check if the response contains JSON
            if 'application/json' not in response.headers.get('Content-Type', ''):
                logging.error(f"Expected JSON, but got {response.headers.get('Content-Type')}")
                return None
            if response.status_code != 200:
                logging.error(f"Error fetching {url}: {response.status_code}")
                return None
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return None
 
    def check_rate_limit(self):
        """
        Check GitHub's API rate limit status and log the remaining requests and reset time.
        """
        rate_limit_url = 'https://api.github.com/rate_limit'
        rate_limit_info = self.fetch_url(rate_limit_url)
        if rate_limit_info:
            remaining = rate_limit_info['resources']['core']['remaining']
            reset_time_unix = rate_limit_info['resources']['core']['reset']
            reset_time = datetime.fromtimestamp(reset_time_unix, tz=timezone.utc)
            reset_delta = reset_time - datetime.now(tz=timezone.utc)

            hours, remainder = divmod(reset_delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            logging.info(f"Remaining requests: {remaining}")
            logging.info(f"Reset time: {reset_time} UTC ({hours} hours, {minutes} minutes, and {seconds} seconds from now)\n")
            
            return remaining, reset_time_unix, hours, minutes, seconds
        return 0, None

    def get_repositories(self):
        """
        Retrieves all repositories of the GitHub user and their star counts.
        
        :return: A list of dictionaries containing repository names, star counts, and stargazers
        """
        repos = self.fetch_url(self.url)
        if not repos:
            return []
        
        repo_info = []
        
        with ThreadPoolExecutor() as executor:
            # Use executor to fetch stargazers concurrently for all repositories
            stargazer_futures = {repo['name']: executor.submit(self.get_stargazers, repo['stargazers_url']) for repo in repos}
            
            for repo in repos:
                repo_name = repo['name']
                stars = repo['stargazers_count']
                stargazers = stargazer_futures[repo_name].result()  # Get stargazers from the future
                repo_info.append({
                    'name': repo_name,
                    'stars': stars,
                    'stargazers': stargazers
                })
        
        return repo_info

    def get_stargazers(self, url):
        """
        Retrieves the list of stargazers for a given repository, paginated.

        :param url: The URL of the repository's stargazers API endpoint
        :return: A list of stargazer usernames
        """
        stargazers = []
        while url:
            stargazer_page = self.fetch_url(url)
            if not stargazer_page:
                break
            stargazers.extend([user['login'] for user in stargazer_page])
            
            # Check for pagination and get the next page URL from the 'Link' header
            if 'Link' in requests.head(url).headers:
                links = requests.head(url).headers['Link']
                next_page = None
                for link in links.split(','):
                    if 'rel="next"' in link:
                        next_page = link[link.find('<') + 1:link.find('>')]
                url = next_page
            else:
                break
        
        return stargazers

    def get_users(self, user_type):
        """
        Scrapes the GitHub profile page to retrieve a list of followers or following.
        
        :param user_type: 'followers' or 'following' to specify which users to retrieve
        :return: A set of GitHub usernames
        """
        try:
            response = requests.get(self.profile_url + user_type)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            return set(elem.text for elem in soup.find_all('span', {'class': 'Link--secondary'}))
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {user_type} for {self.username}: {e}")
            return set()
        except Exception as e:
            logging.error(f"Error parsing {user_type} for {self.username}: {e}")
            return set()

    def print_follow_status(self, followers, followings):
        """
        Prints the follow status (users not following back and followers the account doesn't follow).
        
        :param followers: A set of follower usernames
        :param followings: A set of following usernames
        """
        print("\nUsers not following back:", *(followings - followers), "\nFollowers the account doesn't follow:", *(followers - followings), sep='\n')

    def check_follow_status(self):
        """
        Checks and compares the followers and following lists of the user to determine who is not following back.
        Uses ThreadPoolExecutor to fetch both lists concurrently.
        """
        with ThreadPoolExecutor(max_workers=2) as executor:
            followers, followings = executor.map(self.get_users, ['followers', 'following'])
        
        self.print_follow_status(followers, followings)

    def print_repositories_info(self):
        """
        Prints detailed information about the user's repositories, including their names,
        star counts, and stargazers.
        """
        repos_info = self.get_repositories()
        if not repos_info:
            print("No repositories found or an error occurred.")
            return
        else: 
            print("-" * 40)
            for repo in repos_info:
                print(f"Repository: {repo['name']}")
                print(f"Stars: {repo['stars']}")
                print("Stargazers:", ', '.join(repo['stargazers']))
                print("-" * 40)

if __name__ == "__main__":
    username = input("\nEnter your GitHub username: ")
    user = GithubUser(username)
    
    # Check rate limit before proceeding
    remaining, reset_time, hours, minutes, seconds = user.check_rate_limit()
    if remaining == 0:
        logging.warning(f"Rate limit exceeded. Try again in {hours} hours, {minutes} minutes, and {seconds} seconds.")
    
    user.print_repositories_info()  # To print repository and stargazer info
    user.check_follow_status()  # To check follow status
