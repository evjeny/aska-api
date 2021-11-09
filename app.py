from flask import Flask, send_file

app = Flask(__name__)


@app.route("/status", methods=["GET", "POST"])
def status():
    return "good!"


@app.route("/get_result_viz", methods=["GET", "POST"])
def get_result_viz():
    return send_file("mock.jpeg", mimetype='image/jpeg')

