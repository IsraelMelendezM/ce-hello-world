FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

CMD ["gunicorn","--workers","2", "--worker-class","uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "main:app"]