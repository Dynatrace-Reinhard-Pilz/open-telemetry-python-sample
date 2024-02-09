import logging
import uuid

from flask import Flask, make_response
from mongo import talk_to_mongo
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from postgres import talk_to_postgres
from utils import LoggerAdapter

from otel import ot

app = Flask("Py-Flask-App")
app.logger = LoggerAdapter(app.logger)
app.logger.setLevel(logging.INFO)

# --------------------------------------
# Allows Auto Instrumentation to kick in
# --------------------------------------
FlaskInstrumentor().instrument_app(app)

@app.route("/", methods=["GET"])
async def quote():
    app.logger.info('Request received')    
    name = str(uuid.uuid4())

    await talk_to_postgres(name)
    await talk_to_mongo(name)

    return make_response({}, 200)

def main():
    app.run(host='0.0.0.0', port=8090, debug=False)
    
if __name__ == "__main__":
    main()