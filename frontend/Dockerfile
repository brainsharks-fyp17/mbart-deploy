FROM python:3.10.1-slim
# make sure the build context is '/backend' dir
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app/
RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app
USER user
ENV PYTHONUNBUFFERED 1
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["main.py"]
