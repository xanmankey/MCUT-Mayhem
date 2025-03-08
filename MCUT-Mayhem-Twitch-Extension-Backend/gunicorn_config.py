import os
from dotenv import load_dotenv

load_dotenv()

workers = int(os.environ.get("GUNICORN_PROCESSES", "1"))
worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
threads = int(os.environ.get("GUNICORN_THREADS", "1"))

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = os.environ.get("FLASK_PORT", "8000")
bind = os.environ.get("GUNICORN_BIND", "{}:{}").format(FLASK_HOST, FLASK_PORT)

forwarded_allow_ips = "*"

secure_scheme_headers = {"X-Forwarded-Proto": "https"}
# For print statements
capture_output = True
