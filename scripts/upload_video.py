

### version typing caption  paste###

# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains

# def upload_video(VIDEO_PATH, CAPTION):
#     print("🚀 Launching browser...")
#     COOKIES_PATH = "/home/linoccm/08-tiktok-automation/utils/cookies_cafe.txt"

#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=chrome_options)

#     print("🔐 Loading TikTok and applying cookies...")
#     driver.get("https://www.tiktok.com/upload")

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

#     print("📝 Updating caption via simulated typing...")
#     try:
#         caption_area = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "public-DraftEditor-content")]'))
#         )

#         caption_area.click()
#         time.sleep(1)

#         # Clear any existing text
#         actions = ActionChains(driver)
#         actions.move_to_element(caption_area).click().key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
#         time.sleep(1)

#         # Simulate real typing
#         for char in CAPTION:
#             caption_area.send_keys(char)
#             time.sleep(0.03)

#         print("✅ Caption updated by simulated typing.")
#     except Exception as e:
#         print(f"❌ Could not update caption: {e}")
#         with open("debug_upload_caption.html", "w", encoding="utf-8") as f:
#             f.write(driver.page_source)
#         driver.quit()
#         return

#     print("📤 Publishing video...")
#     try:
#         post_button = WebDriverWait(driver, 50).until(
#             EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Post"]'))
#         )
#         driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
#         time.sleep(1)
#         driver.execute_script("arguments[0].click();", post_button)
#         print("✅ Video posted successfully!")
#     except Exception as e:
#         print(f"❌ Failed to click 'Post' button: {e}")
#         with open("debug_post_button.html", "w", encoding="utf-8") as f:
#             f.write(driver.page_source)

#     input("🔒 Press Enter to close browser...")
#     driver.quit()

# if __name__ == "__main__":
#     VIDEO_PATH = "/home/linoccm/08-tiktok-automation/data/videos/choquei_7386355699481185541.mp4"
#     CAPTION = "🚨 TRANSFORMAÇÃO ÉPICA: A Isabelle virou um GAVIÃO! Vejam isso! 🦅👀 #isabelle #parintins #bbb #famosos #fofoca #noticias"
#     upload_video(VIDEO_PATH, CAPTION)


### version copy and paste caption ###

import time
import os
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def upload_video(VIDEO_PATH, CAPTION):
    print("🚀 Launching browser...")
    COOKIES_PATH = "/home/linoccm/08-tiktok-automation/utils/cookies_cafe.txt"

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    print("🔐 Loading TikTok and applying cookies...")
    driver.get("https://www.tiktok.com/upload")

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

    print("⏳ Waiting for video processing (approx. 20s)...")
    time.sleep(20)

    print("📝 Updating caption with clipboard and clearing old text...")
    try:
        caption_area = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "public-DraftEditor-content")]'))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", caption_area)
        time.sleep(1)

        # Clear existing content
        actions = ActionChains(driver)
        actions.move_to_element(caption_area).click().key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        time.sleep(1)

        # Paste caption using clipboard
        pyperclip.copy(CAPTION)
        caption_area.send_keys(Keys.CONTROL, 'v')
        print("✅ Caption added.")
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
    VIDEO_PATH = "/home/linoccm/08-tiktok-automation/data/videos/choquei_7386284885658324229.mp4"
    CAPTION = "🚨 TRANSFORMAÇÃO ÉPICA: A Isabelle virou um GAVIÃO! Vejam isso!. A Isabelle virou um GAVIÃO! Vejam isso!. A Isabelle virou um GAVIÃO! Vejam isso! 🦅👀 #isabelle #parintins #bbb #famosos #fofoca #noticias"
    upload_video(VIDEO_PATH, CAPTION)
