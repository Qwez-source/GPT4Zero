# GPT4Zero 🚀

🇷🇺 - Русский                                                                                                                                                                                                                               
🇺🇸 - [English](https://github.com/Qwez-source/GPT4Zero/blob/main/README.md)

![logo](https://i.ibb.co/3SQqx9v/photo-2024-08-31-12-14-53.jpg)

## 📚 Содержание
- [О библиотеке](#о-библиотеке)
- [Использование ChatGPT](#используем-chatgpt-)
  - [Параметры](#параметры)
- [Генерация изображений](#генерация-изображений-)
  - [Параметры генерации картинки](#параметры-функции-generate)
  - [Параметры сохранения картинки](#параметры-функции-save_image)
- [Использование через веб-запросы](#использование-через-веб-запросы-)
  - [Пример python кода](#отправка-веб-запросов-через-пайтон)
- [Используем webui](#используем-webui-)
- [Благодарности](#благодарности-)

## О библиотеке

GPT4Zero был создан как максимально упрощенная в использовании альтернатива GPT4Free

## Используем ChatGPT 🤖

Пример использования ChatGPT через GPT4Zero:

```python
from GPT4Zero import CmdGpt_lib

promt = """
привет,
мой дорогой ии
"""

print(CmdGpt_lib.ask(promt, bot_id=0))
# id - 0, 1, 2
```

### Параметры:
- **message**: Сообщение которые вы хотите отправить ChatGPT.
- **bot_id**: число (0, 1, 2) указывающее какую модель использовать:
  - `0`: GPT 3.5 [ 1 ]
  - `1`: GPT 3.5 [ 2 ]
  - `2`: Gemini 1-5 flash
 
> [!TIP]
>  Выберите подходящий `bot_id` в зависимости от модели, с которой хотите взаимодействовать. Каждая модель обладает разными возможностями и производительностью.

## Генерация изображений 🎨

Генерируем изображения через GPT4Zero:

```python
from GPT4Zero import CmdGenerate_lib

# Генерация изображения в формате base64
image_data = CmdGenerate_lib.generate("кот", 1024, 1024, "негативный запрос", "стиль") 
# стили - KANDINSKY, DEFAULT, UHD, ANIME. Посмотреть стили можно здесь: https://cdn.fusionbrain.ai/static/styles/key

# Расшифровка и сохранение
if image_data:
    CmdGenerate_lib.save_image(image_data, "name.png", "Путь") 
    # Если путь не указан, файл будет сохранен в текущем каталоге
```

### Параметры функции generate:
- **prompt**: Обьект генерации.
- **width**: ширина изображения в пикелях (максимально - 1024).
- **height**: длина изображения в пикелях (максимально - 1024).
- **negative_prompt**: Негативный промт, то чего не должно быть на картинке.
- **style**: Стиль изображения, есть:
  - `KANDINSKY`
  - `DEFAULT`
  - `UHD`
  - `ANIME`
> [!IMPORTANT]
> максимальные ширина и длина - 1024 пикселя.

### Параметры функции save_image:
- **image_data**: base64 строка изображения которую можно получить в `generate`.
- **filename**: имя сохраненного файла.
- **path**: место куда сохранится изображение, если путь не указан, файл будет сохранен в текущем каталоге.

## Используем телеграмм бота 💬
Был сделан код для телеграмм бота, на основе нашей библиотеки, его код можно найти в `teleGPT`.

> [!NOTE]
>  Измените токен бота.

## Использование через веб запросы ✉️

GPT4Zero также позволяет генерировать текст через обычные веб-запросы.

1. **Отправляем запрос:**
   - Используйте поле `?ask` для написания своего промта:
     ```
     https://inquisitive-grizzly-conkerberry.glitch.me/?ask=your_prompt
     ```
   - Замените `your_prompt` на ваш промт.

> [!NOTE]
> Вы можете получить скрипт сайта на этом репозитории.

2. **Выбор модель:**
   - Чтобы выбрать модель, используйте параметр `?model=gpt3_5` или `?model=gemini`:
     ```
     https://inquisitive-grizzly-conkerberry.glitch.me/?ask=your_prompt&model=model_name
     ```
   - Замените `model_name` на `gpt3_5` (по умолчанию) или `gemini`.

> [!TIP]
> Выберите подходящий `bot_id` в зависимости от модели, с которой хотите взаимодействовать. Каждая модель обладает разными возможностями и производительностью.

### Отправка веб запросов через пайтон:

```python
import requests

# Определяем запрос и модель
prompt = "Столица Франции?"
model = "gemini"  # или "gpt3_5" по умолчанию

# Формируем URL
url = f"https://inquisitive-grizzly-conkerberry.glitch.me/?ask={prompt}&model={model}"

# Отправляем запрос
response = requests.get(url)

# Выводим ответ модели
print(response.text)
```

## Используем WebUI 🌐
Можно запустить графический интерфейс (GUI) для GPT4Zero с помощью функции `runGUI()`.
```Python
from GPT4Zero import WebGpt

WebGpt.runGUI()
```
Этот код запустит интерфейс для более удобной работы с ChatGPT                                                                                                  
также вы можете просто перейти на сайт https://pitch-hilarious-hall.glitch.me/ и работать с chatGPT там.

> [!NOTE]
> Код webui можно получить на этом репозитории.

## Благодарности 🙌

- **Kandinsky** [Генерация картинок] - [fusionbrain.ai](https://fusionbrain.ai/)
- **GPT 3.5 [0 id]** - [toolbas.com](https://toolbaz.com/writer/chat-gpt-alternative)
- **GPT 3.5 [1 id]** - [seoschmiede.at](https://seoschmiede.at/en/aitools/chatgpt-tool/)
- **Gemini 1-5 flash [2 id]** - [toolbas.com](https://toolbaz.com/writer/chat-gpt-alternative)
