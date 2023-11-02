from flask import Flask, jsonify, render_template, request
from .services.openai_service import get_user_story_data_analysis, get_story_ui_analysis
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api", methods=["GET"])
def get_data():
    data = {"message": "Hello from Flask!", "items": ["item1", "item2", "item3"]}
    return jsonify(data), 200


@app.route("/", methods=["GET", "POST"])
def index():
    res_data_analysis = ""
    res_ui_analysis = ""
    if request.method == "POST":
        user_story = request.form.get("user_story")

        # Check if user_story is a string and its length is greater than 3
        if isinstance(user_story, str) and len(user_story) > 3:
            res_data_analysis = get_user_story_data_analysis(user_story)
            res_ui_analysis = get_story_ui_analysis(user_story)

    return render_template(
        "hello.html",
        res_data_analysis=res_data_analysis,
        res_ui_analysis=res_ui_analysis,
    )
