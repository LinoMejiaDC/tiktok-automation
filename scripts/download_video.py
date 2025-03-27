
# from bs4 import BeautifulSoup
# from seleniumbase import Driver
# from urllib.parse import urljoin
# from datetime import datetime
# import time
# from selenium.webdriver import ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# from selenium.webdriver.remote.webdriver import WebDriver as Remote
# import os


# SBR_WEBDRIVER  =f'https://brd-customer-hl_a6de26b2-zone-scraping_browser1:dvvofz2u5jjd@brd.superproxy.io:9515'

# def get_timestamp():
#     return datetime.now().strftime("%Y%m%d%H")

# def save_to_file(content, filename):

#     OUTPUT_DIR = "utils"
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)
#     path = os.path.join(OUTPUT_DIR, filename)
#     with open(path, "w", encoding="utf-8") as f:
#         f.write(content)

# def scrape_website(website):

#     print("Connecting to Scraping Browser...")
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website)
#         print("Waiting captcha to solve...")
#         solve_res = driver.execute(
#             "executeCdpCommand",
#             {
#                 "cmd": "Captcha.waitForSolve",
#                 "params": {"detectTimeout": 10000},
#             },
#         )
#         print("Captcha solve status:", solve_res["value"]["status"])
#         print("Navigated! Scraping page content...")
#         time.sleep(3)  # Wait for videos to fully load
#         html = driver.page_source
#         return html


# def get_video_urls(username_url):
#     html = scrape_website(username_url)
#     soup = BeautifulSoup(html, "html.parser")
#     video_tags = soup.find_all("a", href=True)

#     video_urls = []
#     for tag in video_tags:
#         href = tag["href"]
#         if "/video/" in href:
#             video_url = urljoin("https://www.tiktok.com", href)
#             video_urls.append(video_url)
    
#     # Extract username from the URL (e.g., anitta)
#     username = username_url.rstrip('/').split('@')[-1]
#     timestamp = get_timestamp()
#     save_to_file(html, f"{username}_html_{timestamp}.txt")
#     save_to_file(str(soup), f"{username}_soup_{timestamp}.txt")

#     # Remove duplicates
#     return list(set(video_urls))


from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from urllib.parse import urljoin
from datetime import datetime
import time
import os

# Scraping Browser credentials
SBR_WEBDRIVER = f'https://brd-customer-hl_a6de26b2-zone-scraping_browser1:dvvofz2u5jjd@brd.superproxy.io:9515'

OUTPUT_DIR = "utils"

def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H")

def save_to_file(content, filename):
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
        time.sleep(3)
        html = driver.page_source
        return html

def extract_video_data(driver, video_url):
    print(f"Scraping video page: {video_url}")
    driver.get(video_url)
    time.sleep(5)  # Let it load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Description
    img_tag = soup.find("img", alt=True)
    description = img_tag["alt"] if img_tag else ""

    # Likes and comments count
    try:
        like_elem = soup.select_one('[data-e2e="like-count"]')
        comment_elem = soup.select_one('[data-e2e="comment-count"]')

        likes = int(like_elem.text.replace("K", "000").replace(".", "")) if like_elem else 0
        comments_count = int(comment_elem.text.replace("K", "000").replace(".", "")) if comment_elem else 0
    except Exception:
        likes, comments_count = 0, 0

    # TikTok does not expose save count directly
    saves = 0

    # Limited comment extraction
    comment_divs = soup.select('[data-e2e="comment-list"] p')
    comments = [c.text.strip() for c in comment_divs[:5]]

    info = {
        "description": description,
        "likes": likes,
        "comments_count": comments_count,
        "saves": saves,
        "comments": comments
        }
    
    save_to_file(info.txt)

    return info

def get_video_urls(username_url):
    html = scrape_website(username_url)
    soup = BeautifulSoup(html, "html.parser")

    # Save HTML and parsed soup
    username = username_url.rstrip('/').split('@')[-1]
    timestamp = get_timestamp()
    save_to_file(html, f"{username}_html_{timestamp}.txt")
    save_to_file(str(soup), f"{username}_soup_{timestamp}.txt")

    video_tags = soup.find_all("a", href=True)
    video_urls = []
    for tag in video_tags:
        href = tag["href"]
        if "/video/" in href:
            video_url = urljoin("https://www.tiktok.com", href)
            video_urls.append(video_url)

    return list(set(video_urls)), username

def build_username_data(username_url):
    html = scrape_website(username_url)
    video_urls, username = get_video_urls(username_url)

    # Connect again to extract data from each video
    print("Starting full video scraping...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        user_data = {}
        for video_url in video_urls:
            try:
                video_data = extract_video_data(driver, video_url)
                user_data[video_url] = video_data
            except Exception as e:
                print(f"Failed to scrape {video_url}: {e}")

    username_data = {
        username_url: user_data
    }

    return username_data

# Run test
if __name__ == "__main__":
    username_url = "https://www.tiktok.com/@anitta"
    data = build_username_data(username_url)
    print("\nFinal Data:\n")
    from pprint import pprint
    pprint(data)
