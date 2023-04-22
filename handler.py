import sys
sys.path.insert(0, 'vendor')

import openai
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

PREFIX = '*'
openai.api_key = os.environ.get('API_KEY')

def receive(event, context):
    message = json.loads(event['body'])

    bot_id = message['bot_id']
    response = process(message)
    if response:
        send(response, bot_id)

    return {
        'statusCode': 200,
        'body': 'ok'
    }


def process(message):
    # Prevent self-reply
    if message['sender_type'] == 'bot':
        return None
    
    if message['text'].startswith(PREFIX):
        prompt = message['text'][len(PREFIX):].strip()
        response = openai.Image.create(prompt=prompt, n=1, size="256x256")
        reply = response["data"][0]["url"]
        return reply        



def send(text, bot_id):
    url = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)