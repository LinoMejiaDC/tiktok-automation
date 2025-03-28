
from scripts.download_video import build_username_data

# Run test
if __name__ == "__main__":
    username_url = "https://www.tiktok.com/@anitta"
    data = build_username_data(username_url)
    print("\nFinal Data:\n")
    from pprint import pprint
    pprint(data)
