from io import BytesIO
from flask import Flask, send_file, request
from viz.split_rect import SplitRect
from validation import all_in_range, all_rgba_code


app = Flask(__name__)


@app.route("/status", methods=["GET", "POST"])
def status():
    return "good!"


@app.route("/get_split_rect_viz", methods=["GET", "POST"])
def get_result_viz():
    choices = [int(choice) for choice in request.args.getlist("choices")]
    colors = request.args.getlist("colors")
    if len(colors) != 4:
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
    
    if all_in_range(choices, 0, 3) and all_rgba_code(colors):
        buffer = BytesIO()

        rect = SplitRect(choices, colors)
        rect.save_gif(buffer)
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, attachment_filename="askaquestion_result.gif")
    
    return f"Error for values: choices={choices}, colors={colors}"
