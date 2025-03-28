from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from urllib.parse import urljoin
from datetime import datetime
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Scraping Browser credentials
SBR_WEBDRIVER = f'https://brd-customer-hl_55aa07be-zone-scraping_browser1:ymgi0mznl046@brd.superproxy.io:9515'

OUTPUT_DIR = "utils"

timestamp = datetime.now().strftime("%Y%m%d%H%M")


def save_to_file(content, filename):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def scrape_website(website):
    print(f"Connecting to Scraping Browser for: {website}")
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
        time.sleep(3)
        html = driver.page_source
        return html

def extract_video_data(driver, video_url):
    print(f"Scraping video page: {video_url}")
    global timestamp 
    driver.get(video_url)

    try:
        # Wait for like/comment elements to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="like-count"]'))
        )
    except:
        print("⚠️ Timeout waiting for video elements")
        pass

    time.sleep(2)  # Still give some buffer

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Debug: save HTML snapshot
    save_to_file(driver.page_source, f"debug_{timestamp}.html")

    # Description
    img_tag = soup.find("img", alt=True)
    description = img_tag["alt"] if img_tag else ""

    try:
        like_elem = soup.select_one('[data-e2e="like-count"]')
        comment_elem = soup.select_one('[data-e2e="comment-count"]')

        def parse_number(text):
            text = text.replace(",", "").strip()
            if 'K' in text:
                return int(float(text.replace("K", "")) * 1000)
            elif 'M' in text:
                return int(float(text.replace("M", "")) * 1_000_000)
            return int(text)

        likes = parse_number(like_elem.text) if like_elem else 0
        comments_count = parse_number(comment_elem.text) if comment_elem else 0
    except Exception as e:
        print("⚠️ Failed to parse like/comment numbers:", e)
        likes, comments_count = 0, 0

    saves = 0  # still not exposed

    comment_divs = soup.select('[data-e2e="comment-list"] p')
    comments = [c.text.strip() for c in comment_divs[:5]] if comment_divs else []

    return {
        "description": description,
        "likes": likes,
        "comments_count": comments_count,
        "saves": saves,
        "comments": comments
    }

def get_video_urls(username_url):
    html = scrape_website(username_url)
    soup = BeautifulSoup(html, "html.parser")

    # parsed soup
    username = username_url.rstrip('/').split('@')[-1]
    global timestamp 

    video_tags = soup.find_all("a", href=True)
    video_urls = []
    for tag in video_tags:
        href = tag["href"]
        if "/video/" in href:
            video_url = urljoin("https://www.tiktok.com", href)
            video_urls.append(video_url)
    
    list_urls = list(set(video_urls))
    #save
    save_to_file(html, f"{username}_html_{timestamp}.txt")
    save_to_file(str(soup), f"{username}_soup_{timestamp}.txt")
    save_to_file(str(list_urls), f"{username}_list_urls_{timestamp}.txt")

    return list_urls, username

def build_username_data(username_url, max_videos=2, sleep_between=10):

    global timestamp

    video_urls, username = get_video_urls(username_url)
    video_urls = video_urls[:max_videos]  # Limit for testing

    print("Starting full video scraping...")

    user_data = {}

    for video_url in video_urls:
        for attempt in range(2):  # Retry up to 2 times
            try:
                # Create a new browser session for each video
                sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
                with Remote(sbr_connection, options=ChromeOptions()) as driver:
                    video_data = extract_video_data(driver, video_url)
                    user_data[video_url] = video_data
                break  # Exit retry loop on success
            except Exception as e:
                print(f"Attempt {attempt+1} failed for {video_url}: {e}")
                time.sleep(5)  # Wait before retrying

        time.sleep(sleep_between)  # Throttle between videos

    username_data = {
        username_url: user_data
    }

    
    save_to_file(str(username_data), f"{username}_username_data_{timestamp}.txt")

    return username_data


