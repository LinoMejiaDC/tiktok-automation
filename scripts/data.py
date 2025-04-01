from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrape_website(website):
    print(f"🌐 Scraping TikTok using local browser: {website}")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Optional: Use an undetected driver (recommended if TikTok blocks you)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(website)
        time.sleep(5)  # Wait for page to fully render
        html = driver.page_source
        print("✅ Page content retrieved successfully.")
    except Exception as e:
        print(f"❌ Failed to load page: {e}")
        html = ""
    finally:
        driver.quit()

    return print(html)

if __name__ == "__main__":
    scrape_website("https://www.tiktok.com/@sbt")