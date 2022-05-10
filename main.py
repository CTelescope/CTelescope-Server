#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from RPi.GPIO import cleanup

from flask import Flask
from flask_cors import CORS

from routes import init_routes
from libraries.logger import setup_logger, DEBUG

logger = setup_logger(__file__, DEBUG)

""" FLASK SETUP """
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'application/json'
CORS(app, supports_credentials=True)
init_routes(app)

# Entry point
if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0', port=5000, debug=False)
	
	except Exception as e:
		logger.error(e)

	finally:
		logger.info("Clean up GPIOs")
		cleanup()
		logger.info("End of program")	