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
    
    # Check if the payload size exceeds 64KB
    if len(data.encode('utf-8')) > 64 * 1024:
        logger.warning(f"Big payload of 64KB at backend {backend_no}")
        return f"Big payload of 64KB  at backend {backend_no}", 200

    if f'backend_{backend_no}' in data:
        logger.info(f"Processing webhook request on backend {backend_no}")
        return f"Request processed on backend {backend_no}", 200
    
    if f'fail_{backend_no}' in data:
        logger.error(f"Major failure on backend {backend_no}!")
        return f"Major failure on backend {backend_no}!", 404
    
    if f'fail_all' in data:
        logger.error(f"All failing! I'm backend {backend_no}")
        return f"All failing! I'm backend {backend_no}", 404
    
    return "Wrong backend but ok!", 200

if __name__ == "__main__":
    app.run(debug=True)
