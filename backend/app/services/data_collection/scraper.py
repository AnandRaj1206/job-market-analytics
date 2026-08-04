"""
Lightweight scraper example. Point this at a job board that permits
scraping in its robots.txt / ToS, and adjust selectors accordingly.
Respect rate limits and robots.txt.
"""
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (job-market-research-bot)"}

def scrape_job_board(search_url: str, max_pages: int = 3, delay: float = 1.5):
    jobs = []
    for page in range(max_pages):
        resp = requests.get(f"{search_url}&page={page}", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")

        for card in soup.select(".job-card"):
            jobs.append({
                "title": card.select_one(".job-title").get_text(strip=True) if card.select_one(".job-title") else None,
                "company": card.select_one(".company-name").get_text(strip=True) if card.select_one(".company-name") else None,
                "location": card.select_one(".job-location").get_text(strip=True) if card.select_one(".job-location") else None,
                "description": card.select_one(".job-snippet").get_text(strip=True) if card.select_one(".job-snippet") else "",
                "source": "scraper",
            })
        time.sleep(delay)
    return jobs
