import os

from flask import Flask, request
from personalization import personalization
import db_model
import logging as log
import google.cloud.logging as logging

logging_client = logging.Client()
logging_client.setup_logging()

app = Flask(__name__)



log.info(f"Some log here") 

print('starting')

@app.route("/")
def on_event_change():
    """
        on_event_change() : This function will triggered when event is updated or created
    """
    try:
        event_id = request.json['event_id']
        personalization(event_id)
    except Exception as e:
        return f"An Error Occured: {e}"
    return True


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))