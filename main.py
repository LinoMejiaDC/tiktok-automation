
from scripts.download_data import build_username_data
from scripts.create_conten import load_description_from_file, paraphrase_text
from scripts.download_video import download_tiktok_video
from scripts.dir_url import url_filter

from datetime import datetime
import os
import ast

base_dir = "/home/linoccm/08-tiktok-automation"

# Run test
if __name__ == "__main__":

    # 1- Scrapping data 
    username_url = "https://www.tiktok.com/@sbt"  
    #username_url = "https://www.tiktok.com/@jovempannews"  
    #username_url = "https://www.tiktok.com/@choquei"


    username = username_url.rstrip('/').split('@')[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H")

    data = build_username_data(username_url, timestamp)
    print("\nFinal Data:\n")
    from pprint import pprint
    pprint(data)

    # 2 dowload video
    # num_videos = 2    

    # try:
    #     path_urls = base_dir + f"/data/text/{username}_urls_{timestamp}.txt"

    #     with open(path_urls, "r", encoding="utf-8") as file:
    #         video_urls = file.read()
    #         print(video_urls)
    # except FileNotFoundError:
    #     print(f"ERROR The file at {path_urls} was not found.")

    # video_urls = video_urls[:num_videos]

    print(f"############ starting download video ############")


    file_path = os.path.join(base_dir, "data", "text",f"{username}_urls_{timestamp}.txt")

    # try: 
    #     with open(file_path, "r", encoding="utf-8") as f:
    #         urls = f.read()

    # except Exception as e:
    #     print("❌ Failed to parse URLs:", e)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            urls = ast.literal_eval(f.read())  # this parses the string list into a real list
    except Exception as e:
        print("❌ Failed to parse URLs:", e)
        urls = []  # fallback to empty list


    print(f"file_path  --- {file_path }")
    
    urls_filter = url_filter(urls)

    print(f"file_path  --- {file_path }")
    
    print(f"urls_filter --- {urls_filter}")

    for url in urls_filter:

        path_save_videos = base_dir + f"/data/videos/"
        download_tiktok_video(url, path_save_videos)


    #2 - create content

    # output_dir = os.path.join(base_dir, "data", "videos")

    # filepath = "/home/linoccm/08-tiktok-automation/data/text/choquei_username_data_202503301619.txt"
    # print("📥 Loading original TikTok description...")
    # original = load_description_from_file(filepath)
    # print("📄 Original:\n", original)

    # print("\n✨ Generating paraphrased version using GPT-4 Turbo...")
    # improved = paraphrase_text(original)

    # print("\n🔥 Paraphrased:\n", improved)


