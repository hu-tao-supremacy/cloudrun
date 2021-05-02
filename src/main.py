import os
import sys

from flask import Flask, request
from personalization import personalization
import db_model
import base64
import json

app = Flask(__name__)

print("Starting Flask")


@app.route("/pubsub", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    print("Valid Pub/Sub message format")
    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        payload = json.loads(data)
        event_id = payload['eventId']
        try:
            personalization(int(event_id))
        except Exception as e:
            return f"Error: {e}"

    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
