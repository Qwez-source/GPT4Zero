import requests
import json
import cloudscraper
import re
from urllib.parse import quote_plus

def ask(question, bot_id=0):
    if bot_id == 1:
        return ask_gpt3_5(question)
    elif bot_id == 2:
        return ask_transformerBB(question)
    else:
        return ask_gpt3(question)

def ask_gpt3(question):
    url = "https://chatgptis.org/wp-admin/admin-ajax.php"
    data = {
        "_wpnonce": "e9dbd06b79",
        "post_id": "60",
        "url": "https://chatgptis.org",
        "action": "wpaicg_chat_shortcode_message",
        "message": question,
        "bot_id": "0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Origin": "https://chatgptis.org",
        "Referer": "https://chatgptis.org/",
        "Accept": "application/json",
        "Cookie": "cf_clearance=4ToK8EJNJnooNpaqGvrFrv6c7Ja018tjx4NAbrh_0ko-1724778248-1.2.1.1-V.eq7pqVUSGRqzCoqxHBGLoOX.qfsjtFugoAtUpseLWUgV9WS53NcFq_Pym.liAt8LUi9joBWPHdLm04b6iOjhQWLjnf6rDZjJ1xmRpW3iQ74svtS1v4YwsP8hGIB_gVH.vY4Psj62gtbPOcbpzlE6qDW.LfefB2drXLXMLbIvXXIM6KGRznT2xDEuEvng74ll.kVbmVVY2DoUHJac8_9uMTfPeT_71Nv3IhJgPDmkhitI_GCMkjoh8hfbqDe6jwh3Lj8dUYFXNaKuFBs8aMxekm7R2kB5bIYWZ2rgT32k8dsjSXX3nQT8egCxgm6NW.kW5WIK51FrLxKRHSCEtwYM3OCLjoG1zjZ2bTebL.cT.H04dzQqMxux43rb88k3A6Vot5eKF7nH4pJbQ9kmrBnFJCCl8flyhE.gwb6_v8W0sPYsn5Z6as5NfFMM94zwWm"
    }

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        try:
            json_response = response.json()
            if 'data' in json_response:
                return json_response['data']
            else:
                return " 'data' is missing "
        except ValueError:
            return "JSON error"
    else:
        return f"Response error: {response.status_code}"

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
