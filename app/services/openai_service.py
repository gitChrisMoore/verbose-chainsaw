import requests
import re
from app.utils import configuration


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
        "Authorization": f"Bearer {configuration.OPENAI_API_KEY}",
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
        configuration.OPENAI_API_ENDPOINT, headers=headers, json=data, timeout=10
    )

    if response.status_code == 200:
        return parse_openai_response(response)
    else:
        # Handle errors as needed. For simplicity, returning an empty string here.
        return ""


def parse_score(text):
    """
    Parses the score from the OpenAI response.
    """
    # pattern = r"###score_b(.*?)###score_e"

    # match = re.search(pattern, raw_string)
    match = re.search(r"(?<=###score_b\n)\d+(?=\n###score_e)", text)
    print(match)

    if match:
        return match.group()
    else:
        print("no score found")
        return 0


def parse_suggestions(raw_string):
    """
    Parses the suggestions from the OpenAI response.
    """
    content = raw_string.split("###recs_b")[1].split("###recs_e")[0].strip()
    entries = [entry.strip() for entry in content.split("####") if entry.strip()]
    if entries:
        print(entries)
        return entries
    else:
        return []


def get_user_story_data_analysis(user_story):
    """
    Returns the response from OpenAI API for the given user story.
    """

    res = {
        "score": 0,
        "suggestions": [],
    }
    previous_messages = [
        {
            "role": "system",
            "content": "You are a data systems analyst responsible for evaluating user story complete and correctness.\n\nStart at 0, and add points only if one of these conditions is observed:\n- It must provide specific data fields and each of the fields formats\n\nDo not grant any score for the base user story.  All additional notes must come after the user story.\n\nRespond only with the SCORE and list of SUGGESTIONS contextual to the user story.\nSUGGESTIONS should be a list of no more than 5 concise statements that should not contain explanations.\nThe SCORE should be located between ###score_b and ###score_e. The SCORE should be a number between 0 and 100.\nThe SUGGESTIONS should be located between ###recs_b and ###recs_e, each starting with ####.",
        },
        {
            "role": "user",
            "content": "As a Covered Member, I want to submit a short term disability claim.",
        },
        {
            "role": "assistant",
            "content": "###score_b\n0\n###score_e\n\n###recs_b\n#### Specify the data fields required for submitting a short-term disability claim.\n#### Define the formats for each of these data fields.\n#### Determine if there are any conditions or rules associated with the submission of the short term disability claim.\n#### The user story could be more detailed in terms of processes and expected outcomes.\n#### It is recommended to clarify how the process of claim submission should be implemented or automated for the covered member.\n###recs_e",
        },
        {
            "role": "user",
            "content": user_story,
        },
    ]

    openai_res = get_openai_response(previous_messages)
    res["score"] = parse_score(openai_res)
    res["suggestions"] = parse_suggestions(openai_res)

    return res


def get_story_ui_analysis(user_story):
    """
    Returns the response from OpenAI API for the given user story.
    """

    res = {
        "score": 0,
        "suggestions": [],
    }

    previous_messages = [
        {
            "role": "system",
            "content": "As a UI analyst, your role is to evaluate the completeness and correctness of a user story. Please use the following criteria for your evaluation:\n1. Document main, alternative, and exit flows for the user\n2. Specify each UI component'''s type and whether to reuse it from an existing design system.\n3. Provide layout guidelines, including responsiveness for different screen sizes.\n4. Highlight accessibility standards, brand, and style guidelines\n\n\nRespond only with the SCORE and list of SUGGESTIONS contextual to the user story.\n\nSUGGESTIONS should be a list of no more than 5 concise statements that should not contain explinations.\n\nThe SCORE should be located between ###score_b and ###score_e. The SCORE should be a number between 0 and 100.\nThe SUGGESTIONS should be located between ###recs_b and ###recs_e, each starting with ####.\n",
        },
        {
            "role": "user",
            "content": "As a Covered Member, I want to submit a short term disability claim.",
        },
        {
            "role": "assistant",
            "content": "###score_b 5 ###score_e\n\n###recs_b\n##Document the main, alternative, and exit path of the user\n##Specify the type of each UI component\n##Provide layout and responsiveness guidelines\n###recs_e",
        },
        {
            "role": "user",
            "content": user_story,
        },
    ]

    openai_res = get_openai_response(previous_messages)
    res["score"] = parse_score(openai_res)
    res["suggestions"] = parse_suggestions(openai_res)

    return res


def get_story_data_reccomendation(user_story):
    """
    Returns the response from OpenAI API for the given user story.
    """

    res = {
        "updated_story": "",
    }
    previous_messages = [
        {
            "role": "system",
            "content": 'You are a Business Data Analyst, and your job is to update the story regard data.  You should add a list of fields, whether or not they are required, and any other information that is important. Provide as a response the original story, with your edits under the "**Data Context**.',
        },
        {
            "role": "user",
            "content": user_story,
        },
    ]

    openai_res = get_openai_response(previous_messages)
    print(openai_res)
    res["updated_story"] = openai_res

    return res


def get_story_data_acceptance_criteria(user_story):
    """
    Returns the response from OpenAI API for the given user story.
    """

    # res = {
    #     "updated_story": "",
    # }
    # previous_messages = [
    #     {
    #         "role": "system",
    #         "content": 'You are a Business Data Analyst, and your job is to update the story regard data.  You should add a list of fields, whether or not they are required, and any other information that is important. Provide as a response the original story, with your edits under the "**Data Context**.',
    #     },
    #     {
    #         "role": "user",
    #         "content": user_story,
    #     },
    # ]

    # openai_res = get_openai_response(previous_messages)
    # print(openai_res)
    # res["updated_story"] = openai_res
    tmp_res = [
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
        {
            "id": "3",
            "description": "Employee ID or Number: Text/Numeric field, Required, Source: Employment Database",
            "checked": False,
        },
        {
            "id": "4",
            "description": "Disability Onset Date: Date format (MM/DD/YYYY), Required, API: Disability Claims Processing",
            "checked": False,
        },
    ]

    return tmp_res
