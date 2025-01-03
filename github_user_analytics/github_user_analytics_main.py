import requests
import time
import datetime
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import List, Dict, Tuple, Any, Optional
import sys

# Constants for GitHub API URLs and rate limiting
API_BASE_URL = "https://api.github.com"
USER_REPOS_URL = f"{API_BASE_URL}/users/{{username}}/repos"
LINK_HEADER = 'Link'
REL_NEXT = 'rel="next"'

# Constants for retry mechanism and exponential backoff
MAX_RETRIES = 5
INITIAL_RETRY_DELAY = 1  # initial delay in seconds
MAX_BACKOFF_TIME = 60  # max backoff time in seconds

# Configure logging
logging.basicConfig(level=logging.INFO)

class GithubUser:
    # Class-level cache for rate limit reset time
    cached_reset_time = 0

    def __init__(self, username: str):
        """
        Initializes a GithubUser object for interacting with GitHub API.

        :param username: GitHub username to fetch repositories and follow status for.
        """
        self.username = username
        self.url = USER_REPOS_URL.format(username=username)
        self.profile_url = f"https://github.com/{username}?tab="
        self.session = requests.Session()  # Use requests.Session to reuse connections

    def handle_rate_limit(self) -> None:
        """
        Manages rate limiting for API requests. 

        If the rate limit is exceeded:
        - Waits until the cached reset time if known.
        - Otherwise, updates the cached reset time using the rate limit endpoint.

        :raises Exception: If fetching rate limit information from the API fails.
        """
        WAIT_INTERVAL = 5 
        current_time = time.time()

        if current_time < GithubUser.cached_reset_time:
            # Check if remaining requests are still available
            rate_limit_info = self.session.get(f"{API_BASE_URL}/rate_limit").json()
            remaining = rate_limit_info.get('resources', {}).get('core', {}).get('remaining', 0)
            if remaining > 0:
                logging.info("Processing...")
                return

            # If no remaining requests, wait until the cached reset time
            wait_time = GithubUser.cached_reset_time - current_time

            # Convert cached_reset_time to a datetime object
            reset_time = datetime.datetime.fromtimestamp(GithubUser.cached_reset_time, tz=datetime.timezone.utc)

            logging.warning(f"Rate limit in effect. "
                            f"Reset time: {reset_time.strftime('%Y-%m-%d %H:%M:%S')} UTC."
                           )
           
            while wait_time > 0:
                    hours, remainder = divmod(wait_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    sys.stdout.write(f"\rWaiting: {int(hours)}h {int(minutes)}m {int(seconds)}s remaining.")
                    sys.stdout.flush()
                    time.sleep(WAIT_INTERVAL)
                    wait_time -= WAIT_INTERVAL

        else:
            # Update the reset time from the API
            rate_limit_info = self.session.get(f"{API_BASE_URL}/rate_limit").json()
            core_info = rate_limit_info.get('resources', {}).get('core', {})
            reset_time = core_info.get('reset', None)
            if reset_time:
                GithubUser.cached_reset_time = reset_time
            else:
                logging.error("Rate limit information missing 'reset' field.")


    def fetch_url(self, url: str) -> Optional[Tuple[Dict[str, Any], Dict[str, str]]]:
        """
        Fetches data from a specified URL, handling rate limits and retries.

        :param url: The URL to fetch data from.
        :return: A tuple containing the JSON response data and the response headers, or None if the request fails.
        :raises: None directly. Logs errors and handles retries if requests fail.
        """
        retries = 0
        while retries < MAX_RETRIES:
            try:
                # Centralized rate limit handling
                self.handle_rate_limit()

                # Make the request
                response = self.session.get(url)
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '').lower()
                    if 'application/json' not in content_type:
                        logging.error(f"Expected JSON, but got {response.headers.get('Content-Type')}")
                        return None
                    try:
                        return response.json(), response.headers  # Return both JSON data and headers
                    except ValueError as e:
                        logging.error(f"Error parsing JSON from {url}: {e}")
                        return None
                elif response.status_code == 404:
                    logging.error(f"User {self.username} not found.")
                    return None
                elif response.status_code == 403:  # Rate limit exceeded
                    self.handle_rate_limit()
                    continue
                else:
                    logging.error(f"Error fetching {url}: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed for {url}: {e}")
                retries += 1
                if retries >= MAX_RETRIES:
                    logging.error(f"Max retries reached for {url}. Giving up.")
                    return None
                backoff_time = min(INITIAL_RETRY_DELAY * (2 ** retries), MAX_BACKOFF_TIME)
                logging.warning(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
        return None

    def check_rate_limit(self) -> None:
        """
        Ensures compliance with the GitHub API rate limit by invoking the rate limit handler.

        :raises: None. However, this method may pause execution if the rate limit is exceeded.
        """
        self.handle_rate_limit()

    def wait_for_rate_limit_reset(self, reset_time: float) -> None:
        """
        Wait for the GitHub API rate limit to reset.

        :param reset_time: The timestamp when the rate limit will reset
        """
        wait_time = reset_time - time.time() + 1  # Wait until reset time
        logging.warning(f"Rate limit exceeded. Waiting for {wait_time:.0f} seconds.")
        time.sleep(wait_time)


    def extract_usernames(self, page_data: List[Dict[str, Any]]) -> List[str]:
        """
        Extracts usernames from a list of stargazers or followers data.

        :param page_data: List of dictionaries containing user data, each dictionary must have a 'login' key.
        :return: List of usernames extracted from the data
        """
        usernames = []
        for user in page_data:
            if 'login' in user:  # Ensure that 'login' key exists in user data
                usernames.append(user['login'])
            else:
                logging.warning("Missing 'login' key in stargazer data.")
        return usernames

  

    def handle_pagination(self, url: str, fetch_fn) -> List[Dict[str, Any]]:
        """
        Handles pagination for GitHub API responses. It fetches data from multiple pages if necessary.

        :param url: The initial URL to fetch
        :param fetch_fn: The function used to fetch data (e.g., fetch_url)
        :return: A list of data from all pages
        """
        all_data = []
        while url:
            page_data, response_headers = fetch_fn(url)  # Assume fetch_fn returns both data and headers
            if not page_data:
                break
            all_data.extend(page_data)

            # Check for pagination and get the next page URL from the 'Link' header
            next_url = self.extract_next_page_url_from_response(response_headers)
            url = next_url
        return all_data

    def extract_next_page_url_from_response(self, response_headers: dict) -> Optional[str]:
        """
        Extracts the next page URL from the 'Link' header, if it exists. This method
        assumes that the headers are passed from the previous response.

        :param response_headers: The headers from the API response
        :return: The next page URL if found, or None if no pagination is present.
        """
        if LINK_HEADER in response_headers:
            links = response_headers[LINK_HEADER]
            for link in links.split(','):
                if REL_NEXT in link:
                    next_page = link[link.find('<') + 1:link.find('>')]
                    return next_page
        return None

    def get_repositories(self) -> List[Dict[str, Any]]:
        """
        Retrieves all repositories of the GitHub user and their star counts.
        Returns an empty list if no repositories are found or an error occurs.

        :return: A list of dictionaries containing repository 'name' (str), 'stars' (int), and 'stargazers' (List[str])
        :rtype: List[Dict]
        """
        repos = self.fetch_url(self.url)[0]
        if not repos:
            return []

        repo_info = []

        with ThreadPoolExecutor() as executor:
            # Use executor to fetch stargazers concurrently for all repositories
            stargazer_futures = {repo['name']: executor.submit(self.get_stargazers, repo['stargazers_url']) for repo in repos}

            # Handle pagination and fetch repositories in batches
            all_repos = self.handle_pagination(self.url, self.fetch_url)

            for repo in all_repos:
                repo_name = repo['name']
                stars = repo['stargazers_count']
                try:
                    stargazers = stargazer_futures[repo_name].result()  # Get stargazers from the future
                except Exception as e:
                    logging.error(f"Error fetching stargazers for {repo_name}: {e}")
                    stargazers = []  # Default to an empty list if there's an error
                repo_info.append({
                    'name': repo_name,
                    'stars': stars,
                    'stargazers': stargazers
                })

        return repo_info

    def get_stargazers(self, url: str) -> List[str]:
        """
        Retrieves the list of stargazers for a given repository, paginated.

        :param url: The URL of the repository's stargazers API endpoint
        :return: A list of stargazer usernames
        """
        stargazers_page_data = self.handle_pagination(url, self.fetch_url)
        
        # Ensure the stargazers page data is in the expected format
        if not isinstance(stargazers_page_data, list):
            logging.error("Stargazer data is not in the expected list format.")
            return []
        
        return self.extract_usernames(stargazers_page_data)

    def get_users(self, user_type: str) -> set:
        """
        Scrapes the GitHub profile page to retrieve a list of followers or following.

        :param user_type: 'followers' or 'following' to specify which users to retrieve
        :return: A set of GitHub usernames
        """
        try:
            response = self.session.get(self.profile_url + user_type)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            return set(elem.text for elem in soup.find_all('span', {'class': 'Link--secondary'}))
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {user_type} for {self.username}: {e}")
            return set()
        except Exception as e:
            logging.error(f"Error parsing {user_type} for {self.username}: {e}")
            return set()

    def get_follow_status(self, followers: set, followings: set) -> Dict[str, set]:
        """
        Returns the follow status (users not following back and unique followers) as a dictionary.

        :param followers: A set of follower usernames
        :param followings: A set of following usernames
        :return: A dictionary with keys 'not_following_back' (set of strings) and 'unique_followers' (set of strings)
        """
        return {
            'not_following_back': followings - followers,
            'unique_followers': followers - followings
        }

    def check_follow_status(self) -> Dict[str, set]: 
        """
        Checks and compares the followers and following lists of the user to determine who is not following back.
        Uses ThreadPoolExecutor to fetch both lists concurrently.
        """
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Explicitly calling the method for 'followers' and 'following'
            followers_future = executor.submit(self.get_users, 'followers')
            followings_future = executor.submit(self.get_users, 'following')

            # Waiting for the results of the futures
            followers = followers_future.result()
            followings = followings_future.result()          

        follow_status = self.get_follow_status(followers, followings)
        
        return follow_status

    def print_follow_status(self, follow_status: Dict[str, set]) -> None:
        """
        Prints the follow status (users not following back and unique followers).

        :param follow_status: A dictionary containing 'not_following_back' and 'unique_followers' (sets of strings)
        """
        print("\nUsers not following back:", *follow_status['not_following_back'], sep='\n')
        print("\nFollowers the account doesn't follow:", *follow_status['unique_followers'], sep='\n')

    def print_repositories_info(self) -> None:
        """
        Prints detailed information about the user's repositories, including their names,
        star counts, and stargazers.
        """
        repos_info = self.get_repositories()
        if not repos_info:
            print("No repositories found or an error occurred.")
            return
        print("\n" + "-" * 40)
        for repo in repos_info:
            print(f"Repository: {repo['name']}")
            print(f"Stars: {repo['stars']}")
            print("Stargazers:", ', '.join(repo['stargazers']))
            print("-" * 40)

if __name__ == "__main__":
    """
    Main script to execute the process for checking a user's GitHub follow status.

    This script prompts the user for their GitHub username, initializes a
    GithubUser object with that username, and performs the following tasks:
    - Prints repository and stargazer information.
    - Checks the user's follow status.
    - Prints the follow status.

    :param username: GitHub username to fetch follow status and repository info for.
    """
    username: str = input("Enter your GitHub username: ")
    user = GithubUser(username)

    user.print_repositories_info()  # To print repository and stargazer info
    follow_status = user.check_follow_status()  # Get follow status data
    user.print_follow_status(follow_status) 
