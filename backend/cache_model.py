import logging
import os

from dotenv import load_dotenv
from transformers import MBartForConditionalGeneration, MBartTokenizer

load_dotenv()
model_path = os.environ["MODEL_PATH"]
logger = logging.getLogger("uvicorn")
# This script downloads the model to the docker container.
# Should be executed when composing the image

logger.info("Caching the model inside the Docker image..............")
model = MBartForConditionalGeneration.from_pretrained(model_path)
tokenizer = MBartTokenizer.from_pretrained(model_path)
logger.info("Cached the model")
