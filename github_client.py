import requests
import logging
import os
from dotenv import load_dotenv



load_dotenv()

class GitHubClient:
    def __init__(self,token:str | None = None, per_page: int =5 )->None:
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {"authorization": f"token {self.token}"}
        self.base_url = "https://api.github.com"
        self.per_page = per_page
    def fetch_user(self, username:str)->dict | None:
        url = f"{self.base_url}/users/{username}"
        try:
            response = requests.get(url, headers=self.headers,timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logging.error(f"Request timed out for {username}")
            return None
        except requests.exceptions.ConnectionError:
            logging.error(f"Connection error occurred for {username}")
            return None
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred for {username}: {err}")
            return None
        except requests.exceptions.RequestException as err:
            logging.error(f"Error occurred for {username}: {err}")
            return None
    def fetch_repos(self, username:str, page:int=1)->list[dict] | None:
        url = f"{self.base_url}/users/{username}/repos"
        params = {"page": page, "per_page": 5}
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch repos page {page} for {username}:{e}")
            return None

    def fetch_all_repos(self, username:str)->list[dict]:
        all_repos=[]
        page=1
        while True:
            repos = self.fetch_repos(username, page=page)
            if not repos:
                break
            all_repos.extend(repos)
            logging.info(f"Fetched page {page} with {len(repos)} repos")
            page+=1
        return all_repos