import yt_dlp
import re

def download_tiktok_video(video_url, output_dir):

    print(f"download video: {video_url}")

    #get name video
    match = re.search(r'tiktok\.com/@([^/]+)/video/(\d+)', video_url)
    username = match.group(1)
    video_id = match.group(2)
    user_url = f"{username}_{video_id}"

    ydl_opts = {
        'outtmpl': f'{output_dir}/{user_url}.%(ext)s',
        'format': 'mp4',
        'cookiesfrombrowser': None,
        'cookiefile': '/home/linoccm/07_WebScrapping/AI-Web-Scraper/cookies.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"video: {user_url} download with sucess")

# # Example usage
# if __name__ == "__main__":
#     video_url = "https://www.tiktok.com/@anitta/video/7479569363813616951"
#     download_tiktok_video(video_url)

#teste 1
