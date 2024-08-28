# CmdGpt
## About
The most simplified analogue of gpt4free
## Using ChatGPT
```python
import CmdGpt_lib
print(CmdGpt_lib.ask("hello", bot_id=0))
# id - 0, 1, 2
```
## Using Image Generation
```python
from CmdGenerate_lib import generate, save_image

# generating image in base64 string
image_data = generate("cat", 1024, 1024, "negative promt", "style") #styles - KANDINSKY, DEFAULT, UHD, ANIME. You can see styles on https://cdn.fusionbrain.ai/static/styles/key
# decrypt
if image_data:
    save_image(image_data, "name.png", "Path") # If you do not specify a saving path, the file will be saved in the same directory
```

## Credits
```
Kandinsky [image generator] - https://fusionbrain.ai/
ChatGPT [0 id] - https://chatgptis.org/
ChatGPT [1 id] - https://chatgptfree.ai/
ChatGPT [2 id] - https://www.blackbox.ai/
