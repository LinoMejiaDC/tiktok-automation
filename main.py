
from scripts.download_video import get_video_urls

if __name__ == "__main__":
    username_url = "https://www.tiktok.com/@anitta"  # You can change the username here
    urls = get_video_urls(username_url)
    print("Video URLs:")
    for url in urls:
        print(url)