#!/bin/bash
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py &
if [ ! -d ".git" ]; then
  git init
  git remote add origin git@github.com:georgelevine/rockwell-chatbot.git
fi
git pull origin main --rebase
git add .
git commit -m "Final chatbot build with RAG and deployment"
git push -u origin main
