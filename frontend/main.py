import logging.config
import os

import gradio
from gradio.mix import Parallel
import requests
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
    return response["simplification"]


gradio.close_all()  # close already running instances
text_input = gradio.inputs.Textbox(lines=10, placeholder="Type here", label="Complex Sentence")
output = gradio.outputs.Textbox(type="str", label="Simplified")

iface1 = gradio.Interface.load("huggingface/Rumesh/mbart-si-simp")
Parallel(iface1).launch(share=False, server_port=5000, server_name="0.0.0.0")
