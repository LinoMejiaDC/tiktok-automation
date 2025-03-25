# tiktok-automation

CONFIGURATION FOR CREATE PROJECT DIRECTORY + GITHUB CI/CD

🧱 STEP 1: Set Up the Project Structure
bash
Copiar
Editar
mkdir tiktok-automation
cd tiktok-automation

# Create subfolders
mkdir -p scripts utils data/raw data/processed data/logs .github/workflows config

# Create files
touch README.md requirements.txt main.py
touch scripts/download_video.py scripts/modify_video.py scripts/upload_video.py
touch utils/tiktok_api.py utils/video_utils.py utils/logger.py
touch config/config.yaml
🐍 STEP 2: Set Up Python Virtual Environment
bash
Copiar
Editar
# Install venv if not already installed
sudo apt-get install python3-venv -y

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
Now you're inside the virtual environment — you'll see (venv) in your terminal.

📦 STEP 3: Install Required Python Packages
Edit the requirements.txt file and add the libraries you'll use, for example:

txt
Copiar
Editar
requests
moviepy
opencv-python
Then install the dependencies:

bash
Copiar
Editar
pip install -r requirements.txt
🔐 STEP 4: Create a .gitignore File
bash
Copiar
Editar
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.log" >> .gitignore
echo ".env" >> .gitignore
echo "data/*" >> .gitignore
echo "!data/.gitkeep" >> .gitignore
echo "utils/" >> .gitignore
This keeps your repo clean and avoids pushing unnecessary files.

🧪 STEP 5: Add a Sample main.py
python
Copiar
Editar
# main.py
from scripts.download_video import download
from scripts.modify_video import modify
from scripts.upload_video import upload

if __name__ == "__main__":
    video_path = download()
    edited_path = modify(video_path)
    upload(edited_path)
Just make sure each script (download_video.py, etc.) defines the correct function.

🧑‍💻 STEP 6: Initialize Git & Push to GitHub
bash
Copiar
Editar
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/tiktok-automation.git
git push -u origin main
⚙️ STEP 7: Add GitHub Actions Workflow
Create the file .github/workflows/main.yml with the following content:

yaml
Copiar
Editar
name: TikTok Automation

on:
  push:
    branches:
      - main

jobs:
  run-tiktok-pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run pipeline
        run: python main.py
🚀 STEP 8: Push Again to Trigger GitHub Action
bash
Copiar
Editar
git add .github/workflows/main.yml
git commit -m "Add GitHub Actions pipeline"
git push



codes
python ./scripts/download_video.py

https://www.tiktok.com/@anitta/video/7469556423991561478
https://www.tiktok.com/@anitta/video/7481739673937710391
https://www.tiktok.com/@anitta/video/7481436341419494711
https://www.tiktok.com/@anitta/video/7473131029063028023
https://www.tiktok.com/@anitta/video/7461030892694195462
https://www.tiktok.com/@anitta/video/7468462221845155077
https://www.tiktok.com/@anitta/video/7479193490572709125
https://www.tiktok.com/@anitta/video/7466940299655367942
https://www.tiktok.com/@anitta/video/7468693887406607621
https://www.tiktok.com/@anitta/video/7473886446093487366
https://www.tiktok.com/@anitta/video/7480577356000726327
https://www.tiktok.com/@anitta/video/7466586721719733510
https://www.tiktok.com/@anitta/video/7469222285862325559
https://www.tiktok.com/@anitta/video/7464366079406656774
https://www.tiktok.com/@anitta/video/7469228896479612165
https://www.tiktok.com/@anitta/video/7068312859222052101
https://www.tiktok.com/@anitta/video/7481448823936519429
https://www.tiktok.com/@anitta/video/7466431293551561990
https://www.tiktok.com/@anitta/video/7478026846240607543
https://www.tiktok.com/@anitta/video/7481033502855531782
https://www.tiktok.com/@anitta/video/7461998573312363782
https://www.tiktok.com/@anitta/video/7458858557908339974
https://www.tiktok.com/@anitta/video/7479569363813616951
https://www.tiktok.com/@anitta/video/7471012447156030726
https://www.tiktok.com/@anitta/video/7477566784640437509
https://www.tiktok.com/@anitta/video/7471793440737774903
https://www.tiktok.com/@anitta/video/7464744792858152197
https://www.tiktok.com/@anitta/video/7465008143559298309
https://www.tiktok.com/@anitta/video/7469586834285137158
https://www.tiktok.com/@anitta/video/7462397708456725765
https://www.tiktok.com/@anitta/video/7474643421475491127
https://www.tiktok.com/@anitta/video/7478818921022377221
https://www.tiktok.com/@anitta/video/7467670264965254406
https://www.tiktok.com/@anitta/video/7466182708717276421
https://www.tiktok.com/@anitta/video/7461783860594969861
https://www.tiktok.com/@anitta/video/7476086305257016631