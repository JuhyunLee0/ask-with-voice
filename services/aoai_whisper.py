import os
from openai import AzureOpenAI

aoai_api_key = os.getenv("AZURE_OPENAI_KEY")
aoai_api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
aoai_whisper_deployment_name = os.getenv("AZURE_OPENAI_WHISPER_DEPLOYMENT_NAME")

client = AzureOpenAI(
    api_key = aoai_api_key,  
    api_version = "2024-02-01",
    azure_endpoint = aoai_api_endpoint
)
    
def transcribe_audio(audio_buffer):

    response = client.audio.transcriptions.create(
        file=audio_buffer,            
        model=aoai_whisper_deployment_name
    )

    response_text = response.text
    return response_text


def transcribe_audio_from_filepath(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            file=audio_file,            
            model=aoai_whisper_deployment_name
        )
    response_text = result.text

    # Remove the audio file after transcription
    os.remove(audio_file_path)

    return response_text