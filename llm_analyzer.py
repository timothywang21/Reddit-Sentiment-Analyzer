import anthropic
import configparser #native python package
from openai import OpenAI

system_prompt = '''
You are a reddit thread analyzer. Your job is the analyze a text file given to you in order to give a 1-10 sentiment rating.
IN your response, only write a few short sentences summarizing your result and why you say it.
Make sure to give a 1-10 sentiment rating at the very beginning of your response. Do not consider the topic of the thread. Focus solely on the commenter's tone and language.
Do not answer anything else but ANALYZING the sentiment of a reddit thread. Be as objective as possible. Take into account your bias to be slightly positive.
Always start the response as this: Sentiment rating: [enter sentiment rating here (x, not x/10 where x is the rating from 1 to 10)][insert newline character "\n"][analysis here]
'''

def get_anthropic_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['API_KEYS']['ANTHROPIC_API_KEY']

def analyze_with_claude(text: str) -> str:
    """
    Analyze text using Anthropic Claude model.
    Returns the content string of the response.
    """
    client = anthropic.Anthropic(
        api_key=get_anthropic_api_key()
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=509,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    )
    # Ensure the content is a string
    content = message.content
    if not isinstance(content, str):
        raise TypeError(f"Expected string content from Claude, got {type(content)}")
    return content


def get_openai_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['API_KEYS']['OPENAI_API_KEY']

def analyze_with_openai(text: str) -> str:
    """
    Analyze text using OpenAI GPT-4.1-mini chat completions.
    Returns the content string of the first choice message.
    """
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "developer",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            max_tokens=6003,
            temperature=0
        )
        content = completion.choices[0].message.content
        if not isinstance(content, str):
            raise TypeError(f"Expected string content from OpenAI, got {type(content)}")
        return content
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {e}")
