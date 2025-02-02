from flask import Flask, request, jsonify
import json
import os
from serverless_wsgi import handle_request

app = Flask(__name__)

# Load student data
with open(os.path.join(os.path.dirname(__file__), 'pyth.json')) as f:
    data = json.load(f)
students = {item['name']: item['marks'] for item in data}

@app.route('/api', methods=['GET', 'OPTIONS'])
def handle_api():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        return response
    else:
        names = request.args.getlist('name')
        marks = []
        for name in names:
            if name not in students:
                return jsonify(error=f"Name {name} not found"), 404
            marks.append(students[name])
        return jsonify(marks=marks)

@app.route('/api', methods=['GET', 'OPTIONS'])
def Home():
    return jsonify(message="Welcome to the API")

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response

def handler(event, context):
    return handle_request(app, event, context)