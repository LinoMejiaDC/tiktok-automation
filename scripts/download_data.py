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
from scripts.download_video import download_tiktok_video
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


load_dotenv()
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

#OUTPUT_DIR = "utils"

#timestamp = datetime.now().strftime("%Y%m%d%H%M")

base_dir = "/home/linoccm/08-tiktok-automation"

def save_to_file(content, filename, base_dir, relative_path= "data/raw"):
    """
    Save content to a file inside base_dir / relative_path / filename.
    
    Args:
        content (str): The content to write.
        filename (str): Name of the file (e.g. "output.txt").
        base_dir (str): The root path (e.g. "/home/linoccm/08-tiktok-automation").
        relative_path (str): Subfolder path (e.g. "/data/raw").
    """
    full_dir = os.path.join(base_dir, relative_path)
    os.makedirs(full_dir, exist_ok=True)

    full_path = os.path.join(full_dir, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ File saved to: {full_path}")


# def scrape_website(website):
#     print(f"Connecting to Scraping Browser for: {website}")
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
#         time.sleep(3)
#         html = driver.page_source
#         return html


# def scrape_website(website):
#     print(f"🌐 Scraping TikTok using logged-in session: {website}")

#     chrome_options = Options()
#     chrome_options.add_argument("start-maximized")
#     driver = webdriver.Chrome(options=chrome_options)

#     # Load cookies from file
#     cookies_path = os.path.join(base_dir, "utils", "cookies_cafe.txt")
#     driver.get("https://www.tiktok.com")  # Preload domain for cookies

#     with open(cookies_path, "r", encoding="utf-8") as f:
#         for line in f:
#             if not line.strip().startswith("#") and line.strip():
#                 parts = line.strip().split("\t")
#                 if len(parts) == 7:
#                     domain, flag, path, secure, expiry, name, value = parts
#                     cookie_dict = {
#                         "domain": domain,
#                         "name": name,
#                         "value": value,
#                         "path": path,
#                         "secure": secure.lower() == "true",
#                     }
#                     try:
#                         driver.add_cookie(cookie_dict)
#                     except Exception as e:
#                         print(f"⚠️ Cookie error: {name} → {e}")

#     # Now visit the page as logged-in user
#     driver.get(website)
#     time.sleep(10)

#     # Scroll for more content
#     for _ in range(3):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(4)

#     html = driver.page_source
#     driver.quit()
#     print("✅ Content scraped with cookies.")
#     return html


def scrape_website(website):
    print(f"🌐 Scraping TikTok using logged-in session: {website}")

    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    # Load cookies from file
    cookies_path = os.path.join(base_dir, "utils", "cookies_cafe.txt")
    driver.get("https://www.tiktok.com")  # Preload domain for cookies

    with open(cookies_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip().startswith("#") and line.strip():
                parts = line.strip().split("\t")
                if len(parts) == 7:
                    domain, flag, path, secure, expiry, name, value = parts
                    cookie_dict = {
                        "domain": domain,
                        "name": name,
                        "value": value,
                        "path": path,
                        "secure": secure.lower() == "true",
                    }
                    try:
                        driver.add_cookie(cookie_dict)
                    except Exception as e:
                        print(f"⚠️ Cookie error: {name} → {e}")

    # Now visit the page as logged-in user
    driver.get(website)
    time.sleep(10)

    # Scroll for more content
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    html = driver.page_source
    driver.quit()
    print("✅ Content scraped with cookies.")
    return html



def extract_video_data(driver, video_url, timestamp):
    print(f"Scraping video page: {video_url}")
    #global timestamp 
    driver.get(video_url)

    try:
        # Wait for like/comment elements to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="like-count"]'))
        )
    except:
        print("⚠️ Timeout waiting for video elements")
        pass

    time.sleep(2)  # Still give some buffer

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Debug: save HTML snapshot
    #save_to_file(driver.page_source, f"debug_{timestamp}.html")
    save_to_file(driver.page_source, f"debug_{timestamp}.html", base_dir, relative_path= "data/logs")

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

# def get_video_urls(username_url, timestamp):
#     html = scrape_website(username_url)
#     soup = BeautifulSoup(html, "html.parser")

#     # parsed soup
#     username = username_url.rstrip('/').split('@')[-1]
#     #global timestamp 

#     video_tags = soup.find_all("a", href=True)
#     video_urls = []
#     for tag in video_tags:
#         href = tag["href"]
#         if "/video/" in href:
#             video_url = urljoin("https://www.tiktok.com", href)
#             video_urls.append(video_url)
    
#     list_urls = list(set(video_urls))
#     #save
#     # save_to_file(html, f"{username}_html_{timestamp}.txt")
#     # save_to_file(str(soup), f"{username}_soup_{timestamp}.txt")
#     # save_to_file(str(list_urls), f"{username}_list_urls_{timestamp}.txt")
#     save_to_file(html, f"{username}_html_{timestamp}.txt", base_dir, relative_path= "data/text")
#     save_to_file(str(soup), f"{username}_soup_{timestamp}.txt", base_dir, relative_path= "data/text")
#     save_to_file(str(list_urls), f"{username}_urls_{timestamp}.txt", base_dir, relative_path= "data/text")

#     print(f"URL dowloaded : {list_urls}")

#     return list_urls, username


def get_video_urls(username_url, timestamp):
    html = scrape_website(username_url)
    soup = BeautifulSoup(html, "html.parser")
    username = username_url.rstrip('/').split('@')[-1]

    video_tags = soup.find_all("a", href=True)
    video_urls = []

    for tag in video_tags:
        href = tag["href"]
        if "/video/" in href:
            print("🎯 Found video href:", href)  # Debug print
            video_url = urljoin("https://www.tiktok.com", href)
            video_urls.append(video_url)

    list_urls = list(set(video_urls))
    save_to_file(html, f"{username}_html_{timestamp}.txt", base_dir, relative_path="data/text")
    save_to_file(str(soup), f"{username}_soup_{timestamp}.txt", base_dir, relative_path="data/text")
    save_to_file(str(list_urls), f"{username}_urls_{timestamp}.txt", base_dir, relative_path="data/text")

    print(f"URL downloaded: {list_urls}")
    return list_urls, username

# def build_username_data(username_url, timestamp):
#     sleep_between=10

#     #global timestamp

#     video_urls, username = get_video_urls(username_url,timestamp)
#     #video_urls = video_urls[:max_videos]  # Limit for testing

#     print("Starting full video scraping...")

#     user_data = {}

#     for video_url in video_urls:
#         for attempt in range(2):  # Retry up to 2 times
#             try:
#                 # Create a new browser session for each video
#                 sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
#                 with Remote(sbr_connection, options=ChromeOptions()) as driver:
#                     video_data = extract_video_data(driver, video_url,timestamp)
#                     user_data[video_url] = video_data
#                 break  # Exit retry loop on success
#             except Exception as e:
#                 print(f"Attempt {attempt+1} failed for {video_url}: {e}")
#                 time.sleep(5)  # Wait before retrying

#         time.sleep(sleep_between)  # Throttle between videos

#     username_data = {
#         username_url: user_data
#     }
    
#     #save_to_file(str(username_data), f"{username}_username_data_{timestamp}.txt")

#     save_to_file(str(username_data), f"{username}_{timestamp}.txt", base_dir, relative_path= "data/text")

#     return username_data



def build_username_data(username_url, timestamp):
    sleep_between = 10

    video_urls, username = get_video_urls(username_url, timestamp)

    print("Starting full video scraping...")

    user_data = {}

    video_urls = video_urls[:2]

    for video_url in video_urls:
        for attempt in range(2):  # Retry up to 2 times
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument("start-maximized")
                chrome_options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )

                driver = webdriver.Chrome(options=chrome_options)

                try:
                    video_data = extract_video_data(driver, video_url, timestamp)
                    user_data[video_url] = video_data
                    break  # success
                finally:
                    driver.quit()
            except Exception as e:
                print(f"Attempt {attempt+1} failed for {video_url}: {e}")
                time.sleep(5)

        time.sleep(sleep_between)

    username_data = {
        username_url: user_data
    }

    save_to_file(str(username_data), f"{username}_{timestamp}.txt", base_dir, relative_path="data/text")

    return username_data



