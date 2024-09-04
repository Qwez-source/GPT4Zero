from flask import Flask, request
import requests
import json
import re

app = Flask(__name__)

def ask_gpt3_5(question):
    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://seoschmiede.at",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    data = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            readable_text = response_json['choices'][0]['message']['content']
            return readable_text
        else:
            return "No choices found in response"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except ValueError:
        return "Error decoding JSON response"

def ask_transformerBB(question):
    url = "https://www.blackbox.ai/api/chat"
    data = {
        "messages": [
            {"id": "5rT7N42", "content": question + " answer the question in the language in which it was asked", "role": "user"}
        ],
        "id": "5rT7N42",
        "previewToken": None,
        "userId": None,
        "codeModelMode": True,
        "agentMode": {},
        "trendingAgentMode": {},
        "isMicMode": False,
        "maxTokens": 1024,
        "isChromeExt": False,
        "githubToken": None,
        "clickedAnswer2": False,
        "clickedAnswer3": False,
        "clickedForceWebSearch": False,
        "visitFromDelta": False,
        "mobileClient": False
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Origin": "https://www.blackbox.ai",
        "Referer": "https://www.blackbox.ai/"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        
        if response.status_code == 200:
            raw_response = response.content.decode('utf-8')
            cleaned_response = re.sub(r'^\$@\$\w+=.*\$', '', raw_response)
            return cleaned_response.strip()
        else:
            return f"Response error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

@app.route('/')
def home():
    ask = request.args.get('ask')
    model = request.args.get('model', 'gpt3_5')
    
    if ask:
        if model == 'transformerBB':
            answer = ask_transformerBB(ask)
        else:
            answer = ask_gpt3_5(ask)
        return f'<html><body><p>{answer}</p></body></html>'
    else:
        return '<html><body><p>Use the URL parameter ?ask to ask a question and ?model=gpt3_5 or ?model=transformerBB to select the model.</p></body></html>'

if __name__ == "__main__":
    app.run(debug=True)