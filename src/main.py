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

app = Flask(__name__)  

print('starting')

@app.route("/<event_id>")
def on_event_change(event_id):
    """
        on_event_change(event_id) : This function will triggered when event is updated or created
    """
    try:
        personalization(int(event_id))
    except Exception as e:
        return f"An Error Occured: {e}"
    return True


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))