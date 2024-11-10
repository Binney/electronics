echo "Starting answerphone, let's go"
cd /home/dreamcat/electronics/answerphone
sudo .venv/bin/python answerphone.py & > logs/log_${date}.txt 2>&1
