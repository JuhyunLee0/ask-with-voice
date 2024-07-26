import os
import requests

aoai_api_key = os.getenv("AZURE_OPENAI_KEY")
aoai_api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
aoai_tts_deploy_name = os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT_NAME")
# alloy, echo, fable, onyx, nova, and shimmer.
aoai_tts_voice_name = "nova"
aoai_tts_model = "tts-1"


def text_to_speech(text):
    azure_openai_endpoint = f"{aoai_api_endpoint}/openai/deployments/{aoai_tts_deploy_name}/audio/speech"
    api_version = "2024-02-15-preview"
    headers = {
        "api-key": aoai_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "model": aoai_tts_model,
        "input": text,
        "voice": aoai_tts_voice_name
    }

    try:
        response = requests.post(f"{azure_openai_endpoint}?api-version={api_version}", json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error generating speech: {e}")
        return None

    return response.content