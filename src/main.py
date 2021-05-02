import os
import sys
  
# def print_to_stdout(*a):
  
#     # Here a is the array holding the objects
#     # passed as the arguement of the function
#     print(*a, file = sys.stdout)
  
# print_to_stdout("Hello World")


from flask import Flask, request
from personalization import personalization
import db_model
import base64
import json

app = Flask(__name__)  

print('starting')

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

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "eventId" in pubsub_message:
        event_id = base64.b64decode(pubsub_message["eventId"]).decode("utf-8").strip()

    print(f"Pub/Sub {event_id}!")

    return ("", 204)

@app.route("/<event_id>")
def on_event_change(event_id):
    """
        on_event_change(event_id) : This function will triggered when event is updated or created
    """
    try:
        personalization(int(event_id))
    except Exception as e:
        return f"An Error Occured: {e}"
    return "Success"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
