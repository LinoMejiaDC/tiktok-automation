# import json
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# # Create OpenAI client
# client = OpenAI()

# # ✅ Load environment variables
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load environment variables first
load_dotenv()

# ✅ Create OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ✅ Step 1: Load original TikTok video description
def load_description_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
        try:
            data = eval(raw)  # Your file is a Python dict, not strict JSON
        except Exception as e:
            raise ValueError("Failed to parse file. Check format.") from e

        first_url_data = list(data.values())[0]  # get the video dictionary
        first_video_data = list(first_url_data.values())[0]  # get the first video details
        return first_video_data["description"]

# ✅ Step 2: Use GPT-4 Turbo to paraphrase

def paraphrase_text(original_text):
    prompt = f"""

Você é um criador de conteúdo viral no TikTok que mora no Brasil.

Melhore e reformule a legenda abaixo para torná-la mais impactante, envolvente e viral. Mantenha as hashtags e deixe-a pronta para o TikTok.

Original: {original_text}

Reformulada:
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content.strip()


# ✅ Step 3: Run the process
if __name__ == "__main__":
    filepath = "/home/linoccm/08-tiktok-automation/data/text/choquei_username_data_202503301619.txt"

    print("📥 Loading original TikTok description...")
    original = load_description_from_file(filepath)
    print("📄 Original:\n", original)

    print("\n✨ Generating paraphrased version using GPT-4 Turbo...")
    improved = paraphrase_text(original)

    print("\n🔥 Paraphrased:\n", improved)
