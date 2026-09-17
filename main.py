import logging
from github_client import GitHubClient
from storage import save_to_json, save_to_csv
from config import load_config
from database import init_db, save_repos_to_db

logging.basicConfig(filename="pipeline.log",level=logging.INFO,format="%(asctime)s-%(levelname)s-%(message)s")

def process_users(client: GitHubClient,usernames:list[str])->dict:
    results={"success":[],"failure":[]}

    for username in usernames:
        logging.info(f"Processing user: {username}")
        repos = client.fetch_all_repos(username)
        if repos :
            results["success"].append(username)
            save_to_json(repos,f"{username}_repos.json")
            save_to_csv(repos,f"{username}_repos.csv")
            save_repos_to_db(username,repos)
        else:
            results["failure"].append(username)
            logging.warning(f"No data retrieved for {username}")
    return results

if __name__ == "__main__":
    config = load_config()
    init_db()
    client = GitHubClient(per_page=config["per_page"])
    results = process_users(client, config["usernames"])
    
    logging.info(f"Batch complete. Success:{len(results['success'])},Failed:{len(results['failure'])}")
    print(f"Succeeded: {results['success']}")
    print(f"Failed: {results['failure']}")