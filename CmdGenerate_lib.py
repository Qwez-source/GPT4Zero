import json
import time
import requests
import os
import base64

class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        try:
            response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0]['id']
            else:
                raise ValueError("Model list is empty")
        except Exception as e:
            print(f"Ошибка при получении модели: {e}")
            return None

    def generate(self, prompt, width=1024, height=1024, negative="", style=""):
        model_id = self.get_model()
        if not model_id:
            print("Не удалось получить идентификатор модели")
            return None

        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": width,
            "height": height,
            "negativePromptUnclip": negative,
            "style": style,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model_id),
            'params': (None, json.dumps(params), 'application/json')
        }
        try:
            response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
            response.raise_for_status()
            data = response.json()
            uuid = data.get('uuid')
            if not uuid:
                raise ValueError("UUID not found in response")
            return self.check_generation(uuid)
        except Exception as e:
            print(f"Ошибка при генерации изображения: {e}")
            return None

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            try:
                response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
                response.raise_for_status()
                data = response.json()
                if data['status'] == 'DONE':
                    return data.get('images', [])
                elif data['status'] == 'FAILED':
                    print("Ошибка генерации изображения")
                    return None
            except Exception as e:
                print(f"Ошибка при проверке статуса генерации: {e}")

            attempts -= 1
            time.sleep(delay)
        print("Превышено время ожидания")
        return None

    def save_image(self, image_data, file_name, file_path=None):
        try:
            if file_path is None:
                file_path = os.getcwd()

            full_path = os.path.join(file_path, file_name)
            with open(full_path, 'wb') as file:
                file.write(base64.b64decode(image_data))

        except Exception as e:
            print(f"Ошибка при сохранении изображения: {e}")

def generate(prompt, width=1024, height=1024, negative="", style=""):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '582AC9DB39EC26657C8DC5363FA298CE', 'A1B55EB2DF8E9FC08268AB5A3871D093')
    images = api.generate(prompt, width, height, negative, style)
    if images:

        return images[0]
    return None

def save_image(image_data, file_name, file_path=None):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '582AC9DB39EC26657C8DC5363FA298CE', 'A1B55EB2DF8E9FC08268AB5A3871D093')
    api.save_image(image_data, file_name, file_path)
