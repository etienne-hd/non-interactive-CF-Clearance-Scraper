from flask import Flask, request, jsonify
from scraper import solve
from dotenv import load_dotenv
import os
from logger import logging, logger

load_dotenv()
app = Flask(__name__)
logger.setLevel(logging.DEBUG if os.getenv("DEBUG").strip().lower() == "true" else logging.INFO)

REQUIRED_TOKEN = os.getenv("TOKEN")

@app.route('/', methods=['POST', 'GET'])
def non_interaction_cf_clearance():
    """
    This route is used to retreive cf clearance with different parameter
    """
    url = request.args.get('url', default=None, type=str)
    user_agent = request.args.get('user_agent', default=None, type=str)
    timeout = request.args.get('timeout', default=20, type=int)
    proxy = request.args.get('proxy', default=None, type=str)
    
    logger.info(f"CATCH REQUEST -> {url}")

    # Token verification
    if (
        REQUIRED_TOKEN != None and REQUIRED_TOKEN.strip() != "" and
        REQUIRED_TOKEN.strip() != request.args.get('token', type=str)
    ):
        logger.info(f"Returning a 403 error, invalid token")
        return jsonify({"code": 403, "message": "Unauthorized", "data": None})

    return jsonify(
        solve(
            url=url,
            user_agent=user_agent,
            timeout=timeout,
            proxy=proxy
        )
    )

if __name__ == '__main__':
    app.run()
