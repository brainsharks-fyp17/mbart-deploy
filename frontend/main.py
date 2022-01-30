import gradio
import requests

backend_port = 8000
host = "0.0.0.0"
request_path = "generate"


def get_simplification(text, model):
    url = "http://" + host + ":" + str(backend_port) + "/" + request_path
    data = {"text": text, "model": model}
    response = requests.post(url, json=data).json()
    text = ""
    for line in response["simplification"]:
        text += line + "\n"
    return text


gradio.close_all()  # close already running instances
models = ["mBART", "mT5"]
text_input = gradio.inputs.Textbox(lines=10, placeholder="Type here", label="Complex Sentence")
model_selection = gradio.inputs.Dropdown(models, type="value", default="mT5", label=None)
output = gradio.outputs.Textbox(type="str", label="Simplified")
examples = [["example 1 text", "mT5"],
            ["example 2 text hvuf vfv fuuhv fvfikv evie vj friv rev"
             " vbnrib kr ibn bienrbrrdb  tghhhhhhhhhhhhhhhhhhhhhhhhhhh"
             "hhhhhrffffffffffffffffffffffffffd", "mBART"]]
iface = gradio.Interface(
    fn=get_simplification,
    title="Text Simplification",
    description="description above",
    article="Description <b>of the</b> project",
    inputs=[text_input, model_selection],
    outputs=output,
    theme="dark-huggingface",
    allow_flagging="never",
    allow_screenshot=False,
    css="custom.css",
    examples=examples
)
iface.launch(share=False, server_port=5000)

### todo handle queue
