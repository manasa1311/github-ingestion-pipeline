import json
import logging

def load_config(filename: str="config.json")-> dict:
    try:
        with open(filename,"r") as f:
            config = json.load(f)
        logging.info(f"Loaded Config from {filename}")
        return config
    except FileNotFoundError:
        logging.error(f"Config file {filename} not found")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {filename}: {e}")
        raise