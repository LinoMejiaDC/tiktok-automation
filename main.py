
from scripts.download_data import build_username_data
#from scripts.create_conten import load_description_from_file, paraphrase_text
from scripts.download_video import download_tiktok_video
from scripts.dir_url import url_filter
from scripts.create_conten import create_aicontent
from scripts.upload_video import upload_video

from datetime import datetime
import os
import ast

base_dir = "/home/linoccm/08-tiktok-automation"

# Run test
if __name__ == "__main__":

    # 1- Scrapping data 

    #username_url = "https://www.tiktok.com/@sbt"  
    #username_url = "https://www.tiktok.com/@jovempannews"  
    username_url = "https://www.tiktok.com/@choquei"
    #username_url = "https://www.tiktok.com/@portadosfundos"
    username = username_url.rstrip('/').split('@')[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H")

    data = build_username_data(username_url, timestamp)
    print("\nFinal Data:\n")
    from pprint import pprint
    pprint(data)

    # 2 download video 
    print(f"############ starting download video ############")

    file_path = os.path.join(base_dir, "data", "text",f"{username}_urls_{timestamp}.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            urls = ast.literal_eval(f.read())  # this parses the string list into a real list
    except Exception as e:
        print("❌ Failed to parse URLs:", e)
        urls = []  # fallback to empty list
    
    urls_filter = url_filter(urls, 1, 3)

    for url in urls_filter:

        path_save_videos = base_dir + f"/data/videos/"
        download_tiktok_video(url, path_save_videos)


    #3 - create content

    print(f"############ starting create content AI  ############")

    descriptionai = create_aicontent(data)

    #4 upload video 

    for url_video, description in descriptionai.items():
        VIDEO_PATH = base_dir + "/data/videos/" + f"{username}_{url_video}.mp4"
        upload_video(VIDEO_PATH, description)


