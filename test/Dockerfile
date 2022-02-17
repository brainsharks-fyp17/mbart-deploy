FROM python:3.8
## add and install requirements
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python3"]
CMD ["main.py"]