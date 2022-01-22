from fastapi import FastAPI
from pydantic import BaseModel
from generate import generate, args, load_model

app = FastAPI()


class SimplificationBody(BaseModel):
    text: str
    model: str


@app.get('/')
async def get_root():
    return {}


@app.post('/generate')
async def generate_simp(body: SimplificationBody):
    model = body.model
    text = body.text
    if model not in args.model_path:
        load_model(model_name=model)
    out = generate(text.split("\n"))
    return {"simplification": out}
