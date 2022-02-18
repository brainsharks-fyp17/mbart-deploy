import os
import random
import time
import traceback
from timeit import default_timer as timer

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from starlette_exporter import PrometheusMiddleware, handle_metrics

load_dotenv()
app = FastAPI()

app.add_middleware(PrometheusMiddleware,
                   app_name="backend",
                   prefix="backend",
                   filter_unhandled_paths=False,
                   )
app.add_route("/metrics", handle_metrics)
cache_expire_in_seconds = 3600


class Args:
    model_path = os.environ["MODEL_PATH"]
    max_length = os.environ["MAX_LENGTH"]
    num_beams = os.environ["NUM_BEAMS"]
    task = os.environ["TASK"]


@app.on_event("startup")
def startup_event():
    print("Loading the model..............")
    start_timer = timer()
    time.sleep(random.randint(1, 10))
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
        time.sleep(random.randint(1, 10))
        pass
    return generated


class RequestBody(BaseModel):
    text: str


@app.post('/generate')
def generate_simp(body: RequestBody):
    try:
        start_timer = timer()
        text = body.text
        print("Received for /generate: " + str(text))
        try:
            pass
            if True:
                print(f'search result from redis:')

                return "cached_result"
        except Exception as e:
            traceback.print_exc()
            print("Redis connection error")

        input_sent = text.split("\n")
        print("Length of input: " + str(len(input_sent)))
        print("Input: " + str(input_sent).strip())
        out = generate(input_sent)

        try:
            pass
        except Exception as e:
            print("Redis setting cache error")
            pass

        print("Output from /generate: " + str(out).strip())
        end_timer = timer()
        print("Time taken: " + str(round(end_timer - start_timer, 4)) + " s")
        return {"simplification": out}
    except Exception as e:

        traceback.print_exc()
        return {"error": str(e)}, 500


@app.get('/health')
def health():
    print("Health endpoint")
    return {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", debug=False, reload=False, host="0.0.0.0")
