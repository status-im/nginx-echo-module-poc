import logging
import os
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    format='%(asctime)s [%(levelname)s] %(message)s',  # Log message format
    handlers=[
        logging.StreamHandler()  # Log to the console
    ]
)

logger = logging.getLogger(__name__)

backend_no = os.environ['BACKEND_NO']

@app.route("/", methods=['POST'])
def main_route():
    logger.info(f"Backend {backend_no} received webhook")
    data = request.get_data(as_text=True)
    
    if f'backend=backend_{backend_no}' in data:
        logger.info("Processing webhook request")
        return "Request processed", 200
    
    return "Nothing to process", 204

if __name__ == "__main__":
    app.run(debug=True)
