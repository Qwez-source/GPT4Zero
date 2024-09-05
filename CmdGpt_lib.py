import requests
import json
import re
import uuid

def ask(question, bot_id=0):
    if bot_id == 1:
        return ask_gpt3_5(question)
    elif bot_id == 2:
        return ask_transformerBB(question)
    else:
        return ask_gpt3_5_2(question)

def ask_gpt3_5_2(question):
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
        "model": "gpt-4o-mini",
        "session_id": session_id
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    response_text = response.text
    clean_text = re.sub(r'\[.*?\]', '', response_text).strip()
    
    return clean_text
    
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
    
    response = requests.post(url, headers=headers, data=data)
    
    response_text = response.text
    clean_text = re.sub(r'\[.*?\]', '', response_text).strip()
    
    return clean_text
