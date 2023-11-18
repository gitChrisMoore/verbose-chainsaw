from flask import Flask, jsonify, render_template, request
from .services.openai_service import (
    get_story_data_acceptance_criteria,
    get_user_story_data_analysis,
    get_story_ui_analysis,
    get_story_data_reccomendation,
)
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route("/api", methods=["GET"])
def get_data():
    data = {"message": "Hello from Flask!", "items": ["item1", "item2", "item3"]}
    return jsonify(data), 200


@app.route("/api/story/data-analysis", methods=["POST"])
def get_data_analysis():
    user_story = request.get_json().get("user_story")

    # Check if the user_story is valid.
    if not isinstance(user_story, str):
        return jsonify({"error": "User story must be a string."}), 400
    if len(user_story) <= 3:
        return jsonify({"error": "User story is too short."}), 400

    try:
        # Try to analyze the user_story.
        data = get_user_story_data_analysis(user_story)
        return jsonify(data), 200
    except Exception as e:
        # Handle any unexpected errors during analysis.
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/api/story/ui-analysis", methods=["POST"])
def get_ui_analysis():
    user_story = request.get_json().get("user_story")

    # Check if the user_story is valid.
    if not isinstance(user_story, str):
        return jsonify({"error": "User story must be a string."}), 400
    if len(user_story) <= 3:
        return jsonify({"error": "User story is too short."}), 400

    try:
        # Try to analyze the user_story.
        data = get_story_ui_analysis(user_story)
        return jsonify(data), 200
    except Exception as e:
        # Handle any unexpected errors during analysis.
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/api/story/data-reccomendation", methods=["POST"])
def get_data_reccomendation():
    user_story = request.get_json().get("user_story")

    # Check if the user_story is valid.
    if not isinstance(user_story, str):
        return jsonify({"error": "User story must be a string."}), 400
    if len(user_story) <= 3:
        return jsonify({"error": "User story is too short."}), 400

    try:
        # Try to analyze the user_story.
        data = get_story_data_reccomendation(user_story)
        return jsonify(data), 200
    except Exception as e:
        # Handle any unexpected errors during analysis.
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/api/story/data-acceptance-criteria", methods=["POST"])
def get_data_acceptance_criteria():
    user_story = request.get_json().get("user_story")

    # Check if the user_story is valid.
    if not isinstance(user_story, str):
        return jsonify({"error": "User story must be a string."}), 400
    if len(user_story) <= 3:
        return jsonify({"error": "User story is too short."}), 400

    try:
        # Try to analyze the user_story.
        data = get_story_data_acceptance_criteria(user_story)
        print(data)
        return jsonify(data), 200
    except Exception as e:
        # Handle any unexpected errors during analysis.
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


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


CORS(app)
