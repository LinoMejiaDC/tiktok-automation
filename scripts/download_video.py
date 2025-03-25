
from bs4 import BeautifulSoup
from seleniumbase import Driver
from urllib.parse import urljoin
from datetime import datetime
import time
from selenium.webdriver import ChromeOptions
#from selenium.webdriver.remote.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver as Remote
import os


# Your Bright Data Scraping Browser credentials
# AUTH = 'brd-customer-hl_bce0f29e-zone-scraping_browser1:w91l3u6tzami'
# SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

SBR_WEBDRIVER  =f'https://brd-customer-hl_a6de26b2-zone-scraping_browser1:dvvofz2u5jjd@brd.superproxy.io:9515'

def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H")

def save_to_file(content, filename):

    OUTPUT_DIR = "utils"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def scrape_website(website):

    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        time.sleep(3)  # Wait for videos to fully load
        html = driver.page_source
        return html


def get_video_urls(username_url):
    html = scrape_website(username_url)
    soup = BeautifulSoup(html, "html.parser")
    video_tags = soup.find_all("a", href=True)

    video_urls = []
    for tag in video_tags:
        href = tag["href"]
        if "/video/" in href:
            video_url = urljoin("https://www.tiktok.com", href)
            video_urls.append(video_url)
    
    # Extract username from the URL (e.g., anitta)
    username = username_url.rstrip('/').split('@')[-1]
    timestamp = get_timestamp()
    save_to_file(html, f"{username}_html_{timestamp}.txt")
    save_to_file(str(soup), f"{username}_soup_{timestamp}.txt")

    # Remove duplicates
    return list(set(video_urls))

# Run test
# if __name__ == "__main__":
#     username_url = "https://www.tiktok.com/@anitta"  # You can change the username here
#     urls = get_video_urls(username_url)
#     print("Video URLs:")
#     for url in urls:
#         print(url)

