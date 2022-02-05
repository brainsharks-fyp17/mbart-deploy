import traceback

from fastapi import FastAPI
from pydantic import BaseModel

from transformers import MBartTokenizer, MBartForConditionalGeneration
import torch
from dotenv import load_dotenv
import logging.config
import os
from timeit import default_timer as timer

load_dotenv()
app = FastAPI()
# The ML model takes a significant amount of time to generate results.
# whether the model is generating right now or not is stored in `is_busy`
is_busy = 0
logger = logging.getLogger("uvicorn.access")


class Args:
    model_path = os.getenv("MODEL_PATH", "Rumesh/mbart-si-simp")
    max_length = os.getenv("MAX_LENGTH", "700")
    num_beams = os.getenv("NUM_BEAMS", "5")
    task = os.getenv("TASK", "com-sim")


# Load the model globally
model = None
tokenizer = None
device = None


@app.on_event("startup")
def startup_event():
    global model
    global device
    global tokenizer
    print("Loading the model..............")
    start_timer = timer()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MBartForConditionalGeneration.from_pretrained(Args.model_path)
    model.to(device)
    tokenizer = MBartTokenizer.from_pretrained(Args.model_path)
    end_timer = timer()
    print("Loaded the model")
    print("Time taken to load the model: " + str(round(end_timer - start_timer, 4)) + " s")
    del start_timer
    del end_timer


def generate(source_sentences: list):
    global tokenizer
    global model
    global device
    generated = ""
    # if multiple sentences are in the input sentence, multiple outputs will be generated
    for line in source_sentences:
        # Attach task prefix.
        line = Args.task + ": " + line

        inputs = tokenizer(line, max_length=700, return_tensors="pt", padding=True).to(device)
        summary_ids = model.generate(inputs["input_ids"], num_beams=int(Args.num_beams),
                                     max_length=int(Args.max_length)).to(device)
        out = tokenizer.batch_decode(summary_ids, skip_special_tokens=True,
                                     clean_up_tokenization_spaces=False)

        # Remove pad and eos tokens.
        out = out[0]
        out = out.strip().replace('<pad>', '').replace('</s>', '').strip(" ")

        # Fix zero-width joiner issue.
        out = out.replace("\u0dca \u0dbb", "\u0dca\u200d\u0dbb").replace("\u0dca \u0dba", "\u0dca\u200d\u0dba")
        generated += out + "\n"
    return generated


class RequestBody(BaseModel):
    text: str


@app.post('/generate')
def generate_simp(body: RequestBody):
    try:
        start_timer = timer()
        text = body.text
        print("Received for /generate: " + str(text))
        global is_busy
        is_busy = 1
        input_sent = text.split("\n")
        print("Length of input: " + str(len(input_sent)))
        print("Input: " + str(input_sent))
        out = generate(input_sent)
        print("Output from /generate: " + str(out))
        is_busy = 0
        end_timer = timer()
        print("Time taken: " + str(round(end_timer - start_timer, 4)) + " s")
        return {"simplification": out}
    except Exception as e:
        is_busy = 0
        traceback.print_exc()
        return {"error": str(e)}, 500


@app.get('/health')
def health():
    return {}


@app.get('/busy')
def busy_status():
    return {"is_busy": is_busy}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", debug=True, reload=False, host="0.0.0.0")
