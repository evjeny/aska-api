from flask import Flask, send_file

app = Flask(__name__)


@app.route("/get_result_viz")
def get_result_viz():
    return send_file("mock.jpeg", mimetype='image/jpeg')

