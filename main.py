
from scripts.download_data import build_username_data
from scripts.create_conten import load_description_from_file, paraphrase_text
from scripts.download_video import download_tiktok_video

from datetime import datetime
import time

base_dir = "/home/linoccm/08-tiktok-automation"

# Run test
if __name__ == "__main__":

    # 1- Scrapping data 
    #username_url = "https://www.tiktok.com/@choquei"
    username_url = "https://www.tiktok.com/@sbt"  
    username = username_url.rstrip('/').split('@')[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H")

    data = build_username_data(username_url, timestamp)
    print("\nFinal Data:\n")
    from pprint import pprint
    pprint(data)

    # 2 dowload video
    num_videos = 2    

    try:
        path_urls = base_dir + f"/data/text/{username}_list_urls_{timestamp}.txt"

        with open(path_urls, "r", encoding="utf-8") as file:
            video_urls = file.read()
            print(video_urls)
    except FileNotFoundError:
        print(f"The file at {path_urls} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    video_urls = video_urls[:num_videos]

    for video_url in video_urls:

        path_save_videos = base_dir + f"/videos/"
        download_tiktok_video(video_url, path_save_videos)


    #2 - create content

    # output_dir = os.path.join(base_dir, "data", "videos")

    # filepath = "/home/linoccm/08-tiktok-automation/data/text/choquei_username_data_202503301619.txt"
    # print("📥 Loading original TikTok description...")
    # original = load_description_from_file(filepath)
    # print("📄 Original:\n", original)

    # print("\n✨ Generating paraphrased version using GPT-4 Turbo...")
    # improved = paraphrase_text(original)

    # print("\n🔥 Paraphrased:\n", improved)


