import gradio


def say_hello(input1):
    return "Hello " + input1


gradio.close_all()
input_comp = gradio.inputs.Textbox(lines=10, placeholder="Type here", label="Complex Sentence")
output = gradio.outputs.Textbox(type="str", label="Simplified")
examples = [["example 1 text"],
            ["example 2 text hvuf vfv fuuhv fvfikv evie vj friv rev"
             " vbnrib kr ibn bienrbrrdb  tghhhhhhhhhhhhhhhhhhhhhhhhhhh"
             "hhhhhrffffffffffffffffffffffffffd"]]
iface = gradio.Interface(
    fn=say_hello,
    title="Text Simplification",
    description="description above",
    article="Description <b>of the</b> project",
    inputs=[input_comp],
    outputs=output,
    theme="dark-huggingface",
    allow_flagging="never",
    allow_screenshot=False,
    css="custom.css",
    examples=examples
)
iface.launch(share=False, server_port=5000)
