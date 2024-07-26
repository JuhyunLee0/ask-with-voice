import os
import requests
from openai import AzureOpenAI

aoai_api_key = os.getenv("AZURE_OPENAI_KEY")
aoai_api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
aoai_api_deployment_name = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT_NAME")


client = AzureOpenAI(
    api_key=aoai_api_key,
    api_version="2023-05-15",
    azure_endpoint=aoai_api_endpoint
)

default_system_message = "you are helpful assistant that answer is short and concise manner."

def init_conversation() -> list:
    """Initialize the conversation with a system message"""
    return [
        {"role": "system", "content": default_system_message}
    ]


def get_chat_response(user_input: str) -> str:
    """Generate a response to the user"""
    # return "this is test response"

    conversation = init_conversation()
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=aoai_api_deployment_name,
        messages=conversation,
        temperature=0.7,
        top_p=1,
    )
    print(response)

    responseText = response.choices[0].message.content
    return responseText