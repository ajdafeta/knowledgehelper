# Simple Flask server to serve document HTML files
from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

@app.route('/document/<path:filename>')
def serve_document(filename):
    """Serve document HTML files"""
    try:
        return send_from_directory('static', filename)
    except:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)