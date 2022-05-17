from flask import Flask, jsonify
from flask_cors import CORS

from models.windows import Windows

app = Flask(__name__)
CORS(app)
windows = Windows()

@app.route('/windows')
def state():
    return jsonify(windows.instances)

@app.route('/run/<int:handle>', methods=['POST'])
def run(handle):
    process = windows.run(handle)
    print(process)
    return jsonify({ 'status': 'success'})


@app.route('/stop/<int:handle>', methods=['POST'])
def stop(handle):
    process = windows.stop(handle)
    print(process)
    return jsonify({ 'status': 'success'})