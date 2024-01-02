FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

# CMD ["python", "main.py"]
# --reload
CMD [ "uvicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--port", "80" ]