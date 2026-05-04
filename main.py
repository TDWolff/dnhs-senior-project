import logging
import os
from datetime import datetime
from flask import Flask, render_template, request

# --- Logging setup ---
os.makedirs("logs", exist_ok=True)

log_filename = os.path.join("logs", datetime.now().strftime("%Y-%m-%d") + ".log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(),
    ],
)

log = logging.getLogger(__name__)

# --- App ---
app = Flask(__name__)

@app.after_request
def log_request(response):
    log.info("%s %s %s — %d", request.method, request.path, request.remote_addr, response.status_code)
    return response

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

if __name__ == "__main__":
    log.info("Server starting on port 8090")
    app.run(host="0.0.0.0", port=8090)
