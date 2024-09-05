import logging
import requests
import re
import json
import time
import base64
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = 'TELEGRAM_BOT_TOKEN'

class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, width, height, negative, style, images=1):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "negativePromptUnclip": negative,
            "style": style,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "**Gp4Zero showcase**\n\n"
        "Commands\n"
        "- /generate <текст> — image generating.\n"
        "- <regular message> - text generating\n\n"
        "GitHub: https://github.com/Qwez-source/GPT4Zero"
    )
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    generating_message = await update.message.reply_text("Generating...")
    response = requests.get(f'https://inquisitive-grizzly-conkerberry.glitch.me/?ask={user_message}')
    contents = response.text
    clean_text = re.sub(r'<.*?>', '', contents)
    await generating_message.edit_text(clean_text, parse_mode=ParseMode.MARKDOWN)

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = ' '.join(context.args)
    if not user_message:
        await update.message.reply_text("Please provide text to generate image.")
        return
    generating_message = await update.message.reply_text("Generating image...")
    prompt = user_message
    width, height = 1024, 1024
    negative = " "
    style = " "
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '582AC9DB39EC26657C8DC5363FA298CE', 'A1B55EB2DF8E9FC08268AB5A3871D093')
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id, width, height, negative, style)
    images = api.check_generation(uuid)

    for base64_image in images:
        image_data = base64.b64decode(base64_image)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_data)

    await update.message.reply_text("Success")
    await generating_message.delete()

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('generate', generate_image))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
