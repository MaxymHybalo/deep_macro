from base64 import decode
from flask import Flask, jsonify, request
from flask_cors import CORS

from models.windows import Windows

app = Flask(__name__)
CORS(app)
windows = Windows()

@app.route('/windows')
def state():
    return jsonify(windows.instances)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    from models.settings import Settings
    settings = Settings()
    if request.method == 'GET':
        return jsonify({
            "types": settings.types
        })
    else:
        print(request.get_json())
        windows.set_prop(request.get_json())
        
        return jsonify({"status": "success"})

@app.route('/run/<int:handle>', methods=['POST'])
def run(handle):
    process = windows.run(handle)
    print(process)
    return jsonify(process)


@app.route('/stop/<int:handle>', methods=['POST'])
def stop(handle):
    process = windows.stop(handle)
    print(process)
    return jsonify(process)