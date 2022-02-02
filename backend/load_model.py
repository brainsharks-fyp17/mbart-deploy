from transformers import MT5ForConditionalGeneration, T5Tokenizer, MBartForConditionalGeneration, MBartTokenizer
import torch
from dotenv import load_dotenv
import logging.config
import os

load_dotenv()
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('frontend')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = None
tokenizer = None


class Args:
    model_path = ""
    top_p = os.getenv("TOP_P", "0.95")
    top_k = os.getenv("TOP_K", "50")
    do_sample = os.getenv("DO_SAMPLE", "0")
    temp = os.getenv("TEMP", "1")
    max_length = os.getenv("MAX_LENGTH", "700")
    num_beams = os.getenv("NUM_BEANS", "5")
    rep_pen = os.getenv("REP_PEN", "1.0")
    task = os.getenv("TASK", "com-sim")


def load_model():
    global tokenizer
    global model
    global device
    Args.model_path = "Rumesh/txt-smp-mbart"
    model = MBartForConditionalGeneration.from_pretrained(Args.model_path)
    model.to(device)
    tokenizer = MBartTokenizer.from_pretrained(Args.model_path)
    return model, tokenizer


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

        # input_ids = tokenizer(line, return_tensors="pt").input_ids
        # input_ids = input_ids.to(device)
        # output_ids = model.generate(input_ids=input_ids, do_sample=bool(Args.do_sample), temperature=float(Args.temp),
        #                             max_length=int(Args.max_length), top_k=int(Args.top_k), top_p=float(Args.top_p),
        #                             repetition_penalty=float(Args.rep_pen), num_beams=int(Args.num_beams))
        # out = tokenizer.decode(output_ids[0])

        # Remove pad and eos tokens.
        out = out.strip().replace('<pad>', '').replace('</s>', '').strip(" ")

        # Fix zero-width joiner issue.
        out = out.replace("\u0dca \u0dbb", "\u0dca\u200d\u0dbb").replace("\u0dca \u0dba", "\u0dca\u200d\u0dba")
        generated += out + "\n"
    return generated
