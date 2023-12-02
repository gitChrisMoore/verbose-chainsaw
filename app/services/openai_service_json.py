import requests
import re
import json
from app.utils import configuration


def parse_openai_response(response):
    """
    Parses the response from OpenAI API and returns the text.
    """

    res_content = response.json()["choices"][0]["message"]["content"].strip()

    return res_content


def get_openai_response(messages):
    """
    Sends the provided text to OpenAI API and returns the response.
    """
    headers = {
        "Authorization": f"Bearer {configuration.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo-1106",
        "response_format": {"type": "json_object"},
        "messages": messages,
        # "temperature": 1,
        "max_tokens": 1194,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    response = requests.post(
        configuration.OPENAI_API_ENDPOINT, headers=headers, json=data, timeout=10
    )

    if response.status_code == 200:
        return parse_openai_response(response)
    else:
        # Handle errors as needed. For simplicity, returning an empty string here.
        return ""


def parse_acceptance_criteria(json_string):
    data = json.loads(json_string)
    acceptance_criteria = data.get("acceptance_criteria", [])
    parsed_criteria = []

    for criteria in acceptance_criteria:
        id = criteria.get("id")
        description = criteria.get("description")
        checked = criteria.get("checked")

        parsed_criteria.append(
            {"id": id, "description": description, "checked": checked}
        )

    print("parsed_criteria: ", parsed_criteria)
    return parsed_criteria


def get_story_data_acceptance_criteria(user_story):
    """
    Returns the response from OpenAI API for the given user story.
    """

    print(user_story)

    output_schema = """
    You are designed only to output JSON and should follow this example:
    {
        "acceptance_criteria": [
            {
                "id": "CD-001",
                "description": "Member's Full Name: Text field, Required, Source: Member Profile System",
                "checked": false
            }
        ]
    }
    
    """

    # "description": "Member's Full Name: Text field, Required, Source: Member Profile System",

    previous_messages = [
        {
            "role": "system",
            "content": "You are a helping refine user stories and are responsable for detailing out the data requirements."
            + output_schema
            + """
            Review the user story below, and provide new and different data acceptance criteria. Do not repeat the same criteria that exists in the user story.
            """,
        },
        {
            "role": "user",
            "content": user_story,
        },
    ]

    print(previous_messages)

    temp_res = [
        {
            "id": "1",
            "description": "Member's Full Name: Text field, Required, Source: Member Profile System",
            "checked": False,
        },
        {
            "id": "2",
            "description": "Date of Birth: Date format (MM/DD/YYYY), Required, Source: Member Profile System",
            "checked": False,
        },
    ]

    openai_res = get_openai_response(previous_messages)

    try:
        return parse_acceptance_criteria(openai_res)
    except Exception as e:
        print(e)
        return temp_res
