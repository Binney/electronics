import requests
import os
from dotenv import load_dotenv
load_dotenv()

print("Saying hi")

url = "https://discord.com/api/v10/channels/1212118169041379369/messages"
body = { "content": "It's very dark down here..." }
token = os.environ.get('BOT_TOKEN')

x = requests.post(url, json=body, headers={"Authorization": token})
print(x.text)
print("Done")
