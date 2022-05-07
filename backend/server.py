from flask import Flask, jsonify
from flask_cors import CORS

from models.windows import Windows

app = Flask(__name__)
CORS(app)

@app.route("/windows")
def windows():
    w = Windows().instances
    return jsonify(w)