import json
import logging.config
import os
import random
import traceback
from datetime import timedelta
from timeit import default_timer as timer

import prometheus_client
import redis
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from starlette_exporter import PrometheusMiddleware, handle_metrics
from prometheus_client import Histogram, CollectorRegistry

from torch import device as torch_device
from torch.cuda import is_available as is_cuda_available
from transformers import MBartTokenizer, MBartForConditionalGeneration

load_dotenv()
app = FastAPI()
logger = logging.getLogger("uvicorn")
redis_client = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))

app.add_middleware(PrometheusMiddleware,
                   app_name="backend",
                   prefix="backend",
                   filter_unhandled_paths=False,
                   )
app.add_route("/metrics", handle_metrics)
cache_expire_in_seconds = 3600


# todo add custom metric to measure SARI, BLEU
# todo handle high memory consumption at starting time ~5GB vs 2GB

class Args:
    model_path = os.environ["MODEL_PATH"]
    max_length = os.environ["MAX_LENGTH"]
    num_beams = os.environ["NUM_BEAMS"]
    task = os.environ["TASK"]


# Load the model globally
model = None
tokenizer = None
device = None


@app.on_event("startup")
def startup_event():
    global model
    global device
    global tokenizer
    logger.info("Loading the model........")
    start_timer = timer()
    # device = torch_device('cuda' if is_cuda_available() else 'cpu')
    # model = MBartForConditionalGeneration.from_pretrained(Args.model_path)
    # model.to(device)
    # tokenizer = MBartTokenizer.from_pretrained(Args.model_path)
    end_timer = timer()
    logger.info("Loaded the model")
    logger.info("Time taken to load the model: " + str(round(end_timer - start_timer, 4)) + " s")
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
        out = out.replace("sim", "").strip()
        generated += out + "\n"
    return generated


class RequestBody(BaseModel):
    text: str


@app.post('/generate')
def generate_simp(body: RequestBody):
    try:
        start_timer = timer()
        text = body.text
        logger.info("Received for /generate: " + str(text))
        try:
            redis_result = redis_client.get(f':{text}')
            if redis_result:
                logger.info(f'search result from redis:{redis_result}')
                cached_result = json.loads(redis_result)
                return cached_result
        except Exception as e:
            traceback.print_exc()
            logger.error("Redis connection error")

        input_sent = text.split("\n")
        logger.info("Length of input: " + str(len(input_sent)))
        logger.info("Input: " + str(input_sent).strip())
        out = generate(input_sent)

        try:
            redis_client.set(f':{text}', json.dumps({"simplification": str(out)}))
            redis_client.expire(f':{text}', timedelta(seconds=cache_expire_in_seconds))
        except Exception as e:
            logger.error("Redis setting cache error")
            pass

        logger.info("Output from /generate: " + str(out).strip())
        end_timer = timer()
        logger.info("Time taken: " + str(round(end_timer - start_timer, 4)) + " s")
        return {"simplification": out}
    except Exception as e:

        traceback.print_exc()
        return {"error": str(e)}, 500


@app.get('/health')
def health():
    return {}


# @app.get('/busy')
# def busy_status():
#     return {"is_busy": is_busy}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", info=False, reload=False, host="0.0.0.0")
