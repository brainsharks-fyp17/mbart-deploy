FROM python:3.8
# make sure the build context is '/backend' dir
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN pip install -r requirements.txt -r requirements-local.txt
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN python cache_model.py
#ENTRYPOINT ["uvicorn"]
#CMD ["main:app","--port","8000","--log-level","debug"]
CMD ["python","main.py"]
