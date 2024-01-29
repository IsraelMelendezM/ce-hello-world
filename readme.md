## Getting started
To get the API running:

```bash
cd twilio_otp_api
```
Create a virtual environment with pip or conda:
### With pip
```bash
python3.10 -m venv .venv
```
Activate the virtual environment:
```bash
source .venv/bin/activate
```

### With Conda:
```bash
conda create -n venv python=3.9
```


```bash
pip3.10 install -r requirements.txt
```

### For development:
```bash
uvicorn --reload main:app
```

### For production:

```bash
gunicorn --worker-class uvicorn.workers.UvicornWorker  --bind 0.0.0.0:8080 main:app
```
The API is made for integration for the Watson Assistant.

CronJob scripts are made to run in the morning.

### For local usage:

Go to localhost:8000/docs#/ to see methods and use cases.
