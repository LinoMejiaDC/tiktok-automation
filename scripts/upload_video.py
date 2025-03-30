
# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # === Config ===
# VIDEO_PATH = "/home/linoccm/08-tiktok-automation/data/videos/choquei_7385049342018620677.mp4"
# CAPTION = "Giovanna causando na multidão! Os fãs não param: Giovanna gostosa"
# COOKIES_PATH = "/home/linoccm/08-tiktok-automation/utils/cookies.txt"

# def upload_video():
#     print("🚀 Launching browser...")

#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=chrome_options)

#     print("🔐 Loading TikTok and applying cookies...")
#     driver.get("https://www.tiktok.com/upload")

#     # Load cookies
#     with open(COOKIES_PATH, "r", encoding="utf-8") as f:
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

#     print("📤 Opening upload page...")
#     driver.get("https://www.tiktok.com/upload")
#     time.sleep(5)

#     print("📂 Uploading video...")
#     upload_input = WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
#     )
#     upload_input.send_keys(VIDEO_PATH)

#     print("⏳ Waiting for video processing (approx. 15s)...")
#     time.sleep(15)

#     print("📝 Updating caption via JavaScript...")
#     try:
#         caption_area = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "public-DraftEditor-content")]'))
#         )

#         driver.execute_script("arguments[0].scrollIntoView(true);", caption_area)
#         time.sleep(1)

#         # Inject caption using JavaScript
#         js_code = f"""
#             const editor = arguments[0];
#             const event = new Event('input', {{ bubbles: true }});
#             editor.innerText = `{CAPTION}`;
#             editor.dispatchEvent(event);
#         """
#         driver.execute_script(js_code, caption_area)

#         print("✅ Caption updated successfully.")
#     except Exception as e:
#         print(f"❌ Could not update caption: {e}")
#         with open("debug_upload_caption.html", "w", encoding="utf-8") as f:
#             f.write(driver.page_source)
#         driver.quit()
#         return

#     input("🔒 Press Enter after verifying everything to quit...")
#     driver.quit()

# if __name__ == "__main__":
#     upload_video()


import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Config ===
VIDEO_PATH = "/home/linoccm/08-tiktok-automation/data/videos/choquei_7385049342018620677.mp4"
CAPTION = "Giovanna causando na multidão! Os fãs não param: Giovanna gostosa"
COOKIES_PATH = "/home/linoccm/08-tiktok-automation/utils/cookies_cafe.txt"

def upload_video():
    print("🚀 Launching browser...")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    print("🔐 Loading TikTok and applying cookies...")
    driver.get("https://www.tiktok.com/upload")

    # Load cookies
    with open(COOKIES_PATH, "r", encoding="utf-8") as f:
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

    print("📤 Opening upload page...")
    driver.get("https://www.tiktok.com/upload")
    time.sleep(5)

    print("📂 Uploading video...")
    upload_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    upload_input.send_keys(VIDEO_PATH)

    print("⏳ Waiting for video processing (approx. 15s)...")
    time.sleep(15)

    print("📝 Updating caption via JavaScript...")
    try:
        caption_area = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "public-DraftEditor-content")]'))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", caption_area)
        time.sleep(1)

        js_code = f"""
            const editor = arguments[0];
            const event = new Event('input', {{ bubbles: true }});
            editor.innerText = `{CAPTION}`;
            editor.dispatchEvent(event);
        """
        driver.execute_script(js_code, caption_area)

        print("✅ Caption updated successfully.")
    except Exception as e:
        print(f"❌ Could not update caption: {e}")
        with open("debug_upload_caption.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.quit()
        return

    print("📤 Publishing video...")
    try:
        post_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Post"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", post_button)
        print("✅ Video posted successfully!")
    except Exception as e:
        print(f"❌ Failed to click 'Post' button: {e}")
        with open("debug_post_button.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    input("🔒 Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    upload_video()
