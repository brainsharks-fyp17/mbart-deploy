import os
from dotenv import load_dotenv
import torch
from transformers import MBartForConditionalGeneration, MBartTokenizer

load_dotenv()
model_path = os.getenv("MODEL_PATH", "Rumesh/txt-smp-mbart")

print("Loading the model..............")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MBartForConditionalGeneration.from_pretrained(model_path)
model.to(device)
tokenizer = MBartTokenizer.from_pretrained(model_path)
print("Loaded the model")
