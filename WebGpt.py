from flask import Flask, request, render_template, jsonify
import requests
import json
import re
import uuid

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

def ask_gemini(question):
    session_id = str(uuid.uuid4())

    url = "https://data.toolbaz.com/writer.php"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "host": "data.toolbaz.com",
        "origin": "https://toolbaz.com",
        "referer": "https://toolbaz.com/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    data = {
        "text": question,
        "model": "gemini-1.5-flash",
        "session_id": session_id 
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        response_text = response.text

        clean_text = re.sub(r'\[.*?\]', '', response_text).strip()

        return clean_text
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question', '')
    model = request.form.get('model', 'gpt3.5')
    
    if model == 'gemeni':
        answer = ask_gemini(question)
    else:
        answer = ask_gpt3_5(question)
    
    return jsonify({'answer': answer})

def runGUI():
    app.run(debug=True)

if __name__ == '__main__':
    runGUI()

