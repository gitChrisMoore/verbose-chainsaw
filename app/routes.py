from flask import Flask, render_template, request
from .services.openai_service import get_user_story_data_analysis

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_story = request.form.get("user_story")

        # Check if user_story is a string and its length is greater than 3
        if isinstance(user_story, str) and len(user_story) > 3:
            response_text = get_user_story_data_analysis(user_story)

    return render_template("hello.html", response_text=response_text)
