from base64 import decode
from flask import Flask, jsonify, request
from flask_cors import CORS

from models.windows import Windows

app = Flask(__name__)
CORS(app)
windows = Windows()


SUCCESS = {"status": "success"}
@app.route('/windows')
def state():
    windows = Windows()
    return jsonify(windows.settings())

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    from models.settings import Settings
    settings = Settings()
    if request.method == 'GET':
        return jsonify({
            "types": settings.types
        })
    else:
        data = windows.set_prop(request.get_json())
        print(data)
        return jsonify(data)

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


@app.route('/client', methods=['POST'])
def client():
    print(request.get_json())
    from clients_utils import launch_map
    json = request.get_json()
    launch_map[json['type']]()
    return jsonify(SUCCESS)