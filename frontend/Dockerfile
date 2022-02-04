FROM python:3.10.1-slim
# make sure the build context is '/frontend' dir
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app/
ENV PYTHONUNBUFFERED 1
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["main.py"]
