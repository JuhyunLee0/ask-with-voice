
import os
import io
from pydub import AudioSegment
import pyaudio
import wave
import tempfile
import numpy as np
import time

minimum_record_time = 3  # Minimum recording time in seconds
silence_threshold = 200  # Threshold for silence detection
append_buffer = 1   # Seconds to wait before stopping the recording

# Function to detect silence in the audio stream
def is_silence(data, threshold=500):
    """Check if the audio data is below a silence threshold."""
    return np.abs(np.frombuffer(data, dtype=np.int16)).mean() < threshold

def record_audio_til_silence():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    threshold = silence_threshold  # Adjust this threshold based on your testing
    grace_period = 1  # 1-second grace period after silence is detected

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    start_time = time.time()
    silence_start_time = None  # Track when silence starts

    while True:
        data = stream.read(chunk)
        frames.append(data)
        current_time = time.time()

        # Debugging: Print the average amplitude
        # avg_amplitude = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
        # print(f"Average Amplitude: {avg_amplitude}")

        # Check for silence only after min_record_time has passed
        if current_time - start_time > minimum_record_time:
            if is_silence(data, threshold):
                if silence_start_time is None:
                    silence_start_time = current_time  # Mark the start of silence
                    print("Silence detected, starting grace period.")
                elif current_time - silence_start_time > grace_period:
                    print("Grace period ended, stopping recording.")
                    break
            else:
                if silence_start_time is not None:
                    print("Audio detected, resetting grace period.")
                    silence_start_time = None  # Reset silence start time

    stream.stop_stream()
    stream.close()
    p.terminate()

   # Create an in-memory buffer
    audio_buffer = io.BytesIO()
    wf = wave.open(audio_buffer, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    # Move the buffer's position to the beginning
    audio_buffer.seek(0)
    audio_buffer.name = 'audio.wav'
    
    return audio_buffer



def record_audio_to_local_til_silence():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    threshold = silence_threshold  # Adjust this threshold based on your testing
    grace_period = 1  # 1-second grace period after silence is detected

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    start_time = time.time()
    silence_start_time = None  # Track when silence starts

    while True:
        data = stream.read(chunk)
        frames.append(data)
        current_time = time.time()

        # Debugging: Print the average amplitude
        # avg_amplitude = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
        # print(f"Average Amplitude: {avg_amplitude}")

        # Check for silence only after min_record_time has passed
        if current_time - start_time > minimum_record_time:
            if is_silence(data, threshold):
                if silence_start_time is None:
                    silence_start_time = current_time  # Mark the start of silence
                    print("Silence detected, starting grace period.")
                elif current_time - silence_start_time > grace_period:
                    print("Grace period ended, stopping recording.")
                    break
            else:
                if silence_start_time is not None:
                    print("Audio detected, resetting grace period.")
                    silence_start_time = None  # Reset silence start time

    stream.stop_stream()
    stream.close()
    p.terminate()

    save_dir = "temp"
    os.makedirs(save_dir, exist_ok=True)
    temp_file_path = os.path.join(save_dir, 'audio_' + tempfile.mktemp(suffix='.wav').split(os.sep)[-1])

    wf = wave.open(temp_file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return temp_file_path