from flask import Flask, request, render_template, jsonify
import requests
import json

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question', '')
    answer = ask_gpt3_5(question)
    return jsonify({'answer': answer})

def runGUI():
    app.run(debug=True)

if __name__ == '__main__':
    runGUI()