#!/usr/bin/python3
from flask import Flask, request
import threading 
import os
app = Flask(__name__)

@app.route('/')
def hello(*args):
   return "Hello! This is LIDRE"

@app.route('/run_proc')
def run_proc(*args):
    def run():
        import iterator
    if "tokenID" in request.args and request.args["tokenID"] == os.getenv("FLASK_API_KEY"):
        thread = threading.Thread(target=run)
        thread.start()
        return "Process ran"
    else:
        return "Invalid token"

if __name__ == "__main__":
    app.run(port=os.getenv("PORT"))