'''
app.py
Entry point for the Flask application.
'''

import flask
from api import route_bp

# Initialize a new Flask application.
app = flask.Flask(__name__)

# Register the API routes under the '/api' URL prefix.
app.register_blueprint(route_bp, url_prefix='/api')

# @app.route('/')
# def index():
#     return "Main app route"

# Main entry point for running the Flask application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)