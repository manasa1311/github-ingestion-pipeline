import json
import csv
import logging

def save_to_json(data: list[dict],filename:str)->None:
    try:
        with open(filename,"w") as f:
            json.dump(data,f,indent=4)
        logging.info(f"Saved {len(data)} records to {filename}")
    except Exception as e:
        logging.error(f"Failed to save JSON to {filename}: {e}")


def save_to_csv(data: list[dict],filename:str)-> None:
    if not data:
        logging.warning("no data to save to CSV")
        return
    fieldnames = ["name","full_name","html_url","stargazers_count","language","created_at"]
    try:
        with open(filename,"w",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames=fieldnames)
            writer.writeheader()
            for repo in data:
                row = {key:repo.get(key) for key in fieldnames}
                writer.writerow(row)
            logging.info(f"Saved {len(data)} records to {filename}")
    except Exception as e:
        logging.error(f"Failed to save CSV to {filename}:{e}")
