# Ask-with-voice

This is an simple app to help demo a whisper, GPT, TTS service from Azure OpenAI using streamlit

## Requiremnets

- python 3.11 or above.

## Before Starting

1. Clone the repository: `git clone <URL>`
2. Install dependencies: `pip install -r requirements.txt`
3. Prep the env file: Change the name of `env.sample` file to `.env`.
4. Configure the Environment Variable: Fill in the `.env` file with appropriate values.
5. Start the application: `streamlit run main.py`
6. Optional:
    - change the `silence_threshold` variable inside `services/record_audio.py` to change the threshold for stop recording.
    - change the `default_system_message` variable inside `services/aoai_gpt.py` to change the system prompt.

## Usage

- click on the mic button and begin speaking when `listening` text shows up
- stay silent will stop the recording, and begin transcribing the audio
- it will then ask the GPT for answer and respond in text + audio.

## Contributing

Contributions are welcome! Please follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the [MIT License](LICENSE).
