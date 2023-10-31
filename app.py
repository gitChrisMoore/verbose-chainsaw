# app.py
from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_ENDPOINT = os.environ.get("OPENAI_API_ENDPOINT")


def parse_openai_response(response):
    """
    Parses the response from OpenAI API and returns the text.
    """
    res_content = response.json()["choices"][0]["message"]["content"].strip()
    print(res_content)
    return res_content


def get_openai_response(messages):
    """
    Sends the provided text to OpenAI API and returns the response.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 1,
        "max_tokens": 1194,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    response = requests.post(
        OPENAI_API_ENDPOINT, headers=headers, json=data, timeout=10
    )

    if response.status_code == 200:
        return parse_openai_response(response)
    else:
        # Handle errors as needed. For simplicity, returning an empty string here.
        return ""


def get_user_story_data_analysis(user_story):
    """
    Returns the response from OpenAI API for the given user story.
    """
    previous_messages = [
        {
            "role": "system",
            "content": "You are a data systems analyst responsible for evaluating user story complete and correctness.\n\nStart at 0, and add points only if one of these conditions is observed:\n- It must provide specific data fields and each of the fields formats\n\nDo not grant any score for the base user story.  All additional notes must come after the user story.\n\nRespond with the score and a list of suggested improvements",
        },
        {
            "role": "user",
            "content": user_story,
        },
    ]
    return get_openai_response(previous_messages)


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_story = request.form.get("user_story")

        # Check if user_story is a string and its length is greater than 3
        if isinstance(user_story, str) and len(user_story) > 3:
            response_text = get_user_story_data_analysis(user_story)

    return render_template("hello.html", response_text=response_text)


if __name__ == "__main__":
    app.run(debug=True)
