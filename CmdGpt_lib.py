import requests
import json
import re

def ask(question, bot_id=0):
    if bot_id == 1:
        return ask_gpt3_5(question)
    elif bot_id == 2:
        return ask_transformerBB(question)
    else:
        return ask_gpt3_5_2(question)

def ask_gpt3_5_2(question):
    url = "https://ai-chats.org/chat/send2/"
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
        "Origin": "https://ai-chats.org",
        "Referer": "https://ai-chats.org/chat/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    
    data = {
        "messagesHistory": [{"id": "683d7cc3-592f-4b3a-9648-1779c2d2c264", "from": "you", "content": question}],
        "type": "chat"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        response_text = response.text
        # Извлекаем только текст из data
        parsed_text = ''.join(
            line.split(': ')[1]
            for line in response_text.splitlines()
            if line.startswith('data: ') and line.split(': ')[1].strip()
        )
        return parsed_text

    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except ValueError:
        return "Error decoding response"

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
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        raw_response = response.content.decode('utf-8')
        cleaned_response = re.sub(r'^\$@\$\w+=.*\$', '', raw_response)
        return cleaned_response.strip()
    else:
        return f"Response error: {response.status_code}"
