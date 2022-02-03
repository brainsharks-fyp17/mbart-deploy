FROM python:3.8
# make sure the build context is '/backend' dir
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN pip install -r requirements.txt -r requirements-local.txt
RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app
USER user
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
ENTRYPOINT ["uvicorn"]
CMD ["main:app","--port","8000","--workers","1","--log-level","debug","--limit-concurrency","3"]