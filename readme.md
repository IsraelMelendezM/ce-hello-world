## Getting started
To get the API running:

```bash
cd twilio_otp_api
e```

```bash
pip install -r requirements.txt
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
