import logging.config
import os

import gradio
import requests
from text import description, article, examples
from dotenv import load_dotenv

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('frontend')
load_dotenv()

backend_port = os.environ['BACKEND_PORT']
backend_host = os.environ['BACKEND_HOST']
request_path = "generate"


def get_simplification(text):
    url = "http://" + backend_host + ":" + str(backend_port) + "/" + request_path
    data = {"text": text}
    response = requests.post(url, json=data).json()
    text = ""
    for line in response["simplification"]:
        text += line + "\n"
    return text


gradio.close_all()  # close already running instances
text_input = gradio.inputs.Textbox(lines=10, placeholder="Type here", label="Complex Sentence")
output = gradio.outputs.Textbox(type="str", label="Simplified")

iface = gradio.Interface(
    fn=get_simplification,
    title="Text Simplification for Sinhala Language",
    description=description,
    article=article,
    inputs=[text_input],
    outputs=output,
    theme="dark-huggingface",
    allow_flagging="never",
    allow_screenshot=False,
    analytics_enabled=True,
    css="custom.css",
    examples=examples
)
iface.launch(share=False, server_port=5000, server_name="0.0.0.0")

### todo handle queue
