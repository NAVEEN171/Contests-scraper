from playwright.sync_api import sync_playwright
import json


from format_dates import convert_to_utc_formatted,convert_starts_in_to_datetime
from scrapers.leetcode_scraper import scrape_leetcode_contests
from scrapers.codeforces_scraper import scrape_codeforces_contests
from scrapers.codechef_scraper import scrape_codechef_contests
from utils.db_connection import get_db
from upload_data_to_db.upload import upload_contests_from_json
from upload_data_to_db.update import update_contests_from_json
from upload_data_to_db.process_upload import upload_processing_logs

from automate_youtube_links.automate_links import update_endtimes_and_get_eligible



def run_scrapers():
    platforms = [
        {"name": "codechef", "url": "https://www.codechef.com/contests", "function": scrape_codechef_contests},
        {"name": "codeforces", "url": "https://codeforces.com/contests", "function": scrape_codeforces_contests},
        {"name": "leetcode", "url": "https://leetcode.com/contest/", "function": scrape_leetcode_contests}
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        for platform in platforms:
            print(f"\n=== Scraping {platform['name']} ===")
            try:
                page = browser.new_page()
                page.goto(platform['url'])
                
                platform['function'](page)
                
                page.close()
                print(f"Completed scraping {platform['name']}")
            except Exception as e:
                print(f"Error scraping {platform['name']}: {str(e)}")
        
        browser.close()
    
    print("\nAll scraping completed!")

if __name__ == "__main__":
    db = get_db()
    print(f"Connected to database: {db.name}")
    run_scrapers()
    upload_contests_from_json()
    update_contests_from_json()
    update_endtimes_and_get_eligible()
    update_contests_from_json()
    upload_processing_logs()




