from fastapi import FastAPI
from pydantic import BaseModel
from load_model import Args, load_model, generate

app = FastAPI()


class RequestBody(BaseModel):
    text: str


@app.post('/generate')
def generate_simp(body: RequestBody):
    text = body.text
    if Args.model_path == "":
        load_model()
    out = generate(text.split("\n"))
    return {"simplification": out}


@app.get('/health')
def health():
    return {}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", debug=True, reload=True)
