import psycopg2
import logging
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )
def init_db()->None:
    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS repos (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            name TEXT,
            full_name TEXT,
            html_url TEXT,
            stargazers_count INTEGER,
            language TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Database Initialized")
def save_repos_to_db(username:str,repos:list[dict])->None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for repo in repos:
            cursor.execute("""
                INSERT INTO repos (username, name, full_name, html_url, stargazers_count, language, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                username,
                repo.get("name"),
                repo.get("full_name"),
                repo.get("html_url"),
                repo.get("stargazers_count"),
                repo.get("language"),
                repo.get("created_at"),
            ))
            conn.commit()
            logging.info(f"Saved {len(repos)} repos for {username} to database")
    except psycopg2.Error as e:
        logging.error(f"Database error while saving {username} : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()    