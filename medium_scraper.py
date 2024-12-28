
import requests
from bs4 import BeautifulSoup

class MediumScraper:
    def __init__(self, scraperapi_key):
        self.base_url = "https://medium.com"
        self.scraperapi_url = "http://api.scraperapi.com"
        self.api_key = scraperapi_key

    def get_author_info(self, screen_name):
        # Construct ScraperAPI request URL with JavaScript rendering enabled
        url = f"{self.scraperapi_url}?api_key={self.api_key}&url={self.base_url}/{screen_name}&render=true"
        
        # Send request through ScraperAPI with headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://medium.com/",
            "Connection": "keep-alive",
        }
        
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: Unable to access Medium. Status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract author information
        author_name = soup.find("meta", property="og:title")
        author_bio = soup.find("meta", {"name": "description"})
        
        # Extract list of articles written by the author (titles of articles on their profile page)
        article_titles = [article.text for article in soup.find_all("h3")]
        
        return {
            "author_name": author_name["content"] if author_name else "Unknown",
            "author_bio": author_bio["content"] if author_bio else "No bio available",
            "article_titles": article_titles
        }

if __name__ == "__main__":
    scraperapi_key = input("Enter your ScraperAPI key: ")
    screen_name = input("Enter the Medium username (screen name): ")
    
    scraper = MediumScraper(scraperapi_key)
    
    print(f"Fetching profile information for {screen_name}...")
    author_info = scraper.get_author_info(screen_name)
    
    if author_info:
        print(f"\nAuthor: {author_info['author_name']}")
        print(f"Bio: {author_info['author_bio']}")
        print("\nArticles:")
        for title in author_info["article_titles"]:
            print(f"- {title}")
