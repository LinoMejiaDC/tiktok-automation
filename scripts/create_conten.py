import os
from dotenv import load_dotenv
from openai import OpenAI
import ast

# ✅ Load environment variables first
load_dotenv()

# ✅ Create OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def paraphrase_text(original_text):


#     prompt = f"""

# Você é um criador de conteúdo viral no TikTok que mora no Brasil.

# Melhore e reformule a legenda abaixo para torná-la mais impactante, envolvente e viral. Mantenha as hashtags e deixe-a pronta para o TikTok.

#  legenda Original: {original_text}

# Reformulada:
# """

    prompt = f"""
    Você é um criador de conteúdo viral no TikTok que mora no Brasil.

    Reescreva APENAS a legenda abaixo de forma mais impactante, envolvente e viral. Mantenha as hashtags. NÃO explique, não adicione nada além da legenda reformulada.

    Legenda original:
    {original_text}

    Legenda reformulada:
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content.strip()

def create_aicontent(data):
   description_ai= {}

   for user_url, videos_dict in data.items():
    
    print(f"videos_dict >>> {videos_dict}")
    # Loop through the videos inside
    for video_url, video_info in videos_dict.items():
        video_id = video_url.split('/')[-1]
        description = video_info.get('description', '')
        print(f"🔢 Video ID: {video_id}")
        print(f"📝 Description: {description}")

        text_ai =  paraphrase_text(description)

        description_ai[video_id] = text_ai
        
        print(f"description_ai --->> {description_ai}")
    
    return description_ai
    
# ✅ Step 3: Run the process
if __name__ == "__main__":
    filepath = "/home/linoccm/08-tiktok-automation/data/text/choquei_2025040423.txt" 

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
        try:
            data = ast.literal_eval(raw)  # safely convert str to dict
        except Exception as e:
            raise ValueError("❌ Failed to parse file as dict. Check content.") from e
    
    create_aicontent(data)