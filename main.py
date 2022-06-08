#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from RPi.GPIO import cleanup
from sys import exit

from flask import Flask, request
from flask_cors import CORS

from routes import init_routes
from libraries.logger import setup_logger, DEBUG

logger = setup_logger(__file__, DEBUG) 

""" FLASK SETUP """
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'application/json'
CORS(app, supports_credentials=True)
init_routes(app)

@app.route("/api/connection", methods=['POST'])
def api_connection():
    if request.is_json:
        payload = request.get_json()
        
        r = payload.get('Handshake', 0) # Return default value 0 if not found
        
        if (r != "123456789"):
            return {"result": "NACK"}, 200       
        
        return {"result": "ACK"}, 200
    else:
        return {"result": "Request must be JSON"}, 415 


def main():
	if __name__ == '__main__':
		try:
			app.run(host='0.0.0.0', port=5000, debug=False)
			
		except Exception as e:
			logger.error(e)
			return 1

		finally:
			logger.info("Clean up GPIOs")
			cleanup()
			logger.info("End of program")
			return 0

if __name__ == '__main__':
	exit(main())