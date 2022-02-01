import logging.config

from fastapi import FastAPI
from pydantic import BaseModel
from load_model import Args, load_model, generate
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('frontend')

app = FastAPI()
# The ML model takes a significant amount of time to generate results.
# whether the model is generating right now or not is stored in `is_busy`
is_busy = 0


class RequestBody(BaseModel):
    text: str


@app.post('/generate')
def generate_simp(body: RequestBody):
    try:
        text = body.text
        logger.debug("Received for /generate: "+str(text))
        if Args.model_path == "":
            load_model()
        global is_busy
        is_busy = 1
        out = generate(text.split("\n"))
        logger.debug("Output from /generate: "+str(out))
        is_busy = 0
        return {"simplification": out}
    except Exception as e:
        is_busy = 0
        return {"error": str(e)}, 500


@app.get('/health')
def health():
    return {}


@app.get('/busy')
def busy_status():
    return {"is_busy": is_busy}


if __name__ == "__main__":
    import uvicorn
    load_model()
    uvicorn.run("main:app", debug=True, reload=True)
