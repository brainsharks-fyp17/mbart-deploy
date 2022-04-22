import logging.config
import os

import gradio
from text import description, article, examples
from gradio.mix import Parallel
import requests
from dotenv import load_dotenv

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('frontend')
load_dotenv()

backend_port = os.environ['BACKEND_PORT']
backend_host = os.environ['BACKEND_HOST']
backend_port2 = os.environ['BACKEND_PORT2']
backend_host2 = os.environ['BACKEND_HOST2']
request_path = "generate"


def get_simplification(text):
    url = "http://" + backend_host + ":" + str(backend_port) + "/" + request_path
    data = {"text": text}
    response = requests.post(url, json=data).json()
    return response["simplification"]


def get_simplification2(text):
    url = "http://" + backend_host2 + ":" + str(backend_port2) + "/" + request_path
    data = {"text": text}
    response = requests.post(url, json=data).json()
    return response["simplification"]


def resp(text):
    return get_simplification(text), get_simplification2(text)


gradio.close_all()  # close already running instances
text_input = gradio.inputs.Textbox(lines=10, placeholder="Type here", label="Complex Sentence")
output = gradio.outputs.Textbox(type="str", label="Simp")
output2 = gradio.outputs.Textbox(type="str", label="Trans Simp")

iface = gradio.Interface(
    fn=resp,
    title="Text Simplification for Sinhala Language",
    description=description,
    article=article,
    inputs=[text_input],
    outputs=[output, output2],
    theme="dark-huggingface",
    allow_flagging="never",
    allow_screenshot=False,
    analytics_enabled=True,
    css="custom.css",
    examples=examples
)

iface.launch(share=False, server_port=5000, server_name="0.0.0.0")
