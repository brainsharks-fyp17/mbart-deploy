import logging.config
import traceback

from fastapi import FastAPI
from pydantic import BaseModel
from load_model import generate
from timeit import default_timer as timer

# logging.config.fileConfig('logging.conf')
# logger = logging.getLogger('frontend')

app = FastAPI()
# The ML model takes a significant amount of time to generate results.
# whether the model is generating right now or not is stored in `is_busy`
is_busy = 0
logger = logging.getLogger("uvicorn.access")


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


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
        print("Time taken: " + str(round(end_timer - start_timer, 4))+" s")
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

    uvicorn.run("main:app", debug=True, reload=True)
