FROM python:3.8 AS build-image
## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
## add and install requirements
COPY requirements.txt .
COPY requirements-local.txt .
RUN pip install -r requirements.txt -r requirements-local.txt

FROM python:3.8 AS runtime-image
## copy Python dependencies from build-image
COPY --from=build-image /opt/venv /opt/venv
## set working directory
WORKDIR /usr/src/app
## add app
COPY . /usr/src/app
## set environment variables
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000
RUN python cache_model.py
#ENTRYPOINT ["uvicorn"]
#CMD ["main:app","--port","8000","--log-level","debug"]
ENTRYPOINT ["python3"]
CMD ["main.py"]