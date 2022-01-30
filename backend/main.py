from transformers import MT5ForConditionalGeneration, T5Tokenizer
import torch

device = None
model = None
tokenizer = None


class args:
    model_path = ""
    topp = 0.95
    topk = 50
    do_sample = False
    temp = 1
    max_length = 700
    num_beams = 5
    rep_pen = 1.0
    task = "com-sim"


def load_model(model_name="mT5"):
    global model
    global device
    global tokenizer
    args.model_path = "models/" + model_name
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MT5ForConditionalGeneration.from_pretrained(args.model_path)
    model.to(device)
    tokenizer = T5Tokenizer.from_pretrained(args.model_path)


def generate(source_sentences: list):
    global tokenizer
    global model
    global device
    reply = ""
    for line in source_sentences:
        # Attach task prefix.
        line = args.task + ": " + line

        input_ids = tokenizer(line, return_tensors="pt").input_ids
        input_ids = input_ids.to(device)
        output_ids = model.generate(input_ids=input_ids, do_sample=args.do_sample, temperature=args.temp,
                                    max_length=args.max_length, top_k=args.topk, top_p=args.topp,
                                    repetition_penalty=args.rep_pen, num_beams=args.num_beams)
        out = tokenizer.decode(output_ids[0])

        # Remove pad and eos tokens.
        out = out.strip().replace('<pad>', '').replace('</s>', '').strip(" ")

        # Fix zero-width joiner issue.
        out = out.replace("\u0dca \u0dbb", "\u0dca\u200d\u0dbb").replace("\u0dca \u0dba", "\u0dca\u200d\u0dba")
        reply += out + "\n"
    return reply



