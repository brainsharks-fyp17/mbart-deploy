from transformers import MBartTokenizer, MBartForConditionalGeneration
import torch
from dotenv import load_dotenv
import logging.config
import os
from timeit import default_timer as timer

load_dotenv()
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('frontend')


class Args:
    model_path = "facebook/mbart-large-50"
    max_length = os.getenv("MAX_LENGTH", "700")
    num_beams = os.getenv("NUM_BEAMS", "5")
    task = os.getenv("TASK", "com-sim")


print("Loading the model..............")
start_timer = timer()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MBartForConditionalGeneration.from_pretrained(Args.model_path)
model.to(device)
tokenizer = MBartTokenizer.from_pretrained(Args.model_path)
end_timer = timer()
print("Loaded the model")
print("Time taken to load the model: " + str(round(end_timer - start_timer, 4))+" s")
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
