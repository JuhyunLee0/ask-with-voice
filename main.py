import os
import time
import streamlit as st
import base64
from dotenv import load_dotenv
load_dotenv()

from services.record_audio import record_audio_til_silence, record_audio_to_local_til_silence
from services.aoai_gpt import init_conversation, get_chat_response
from services.aoai_tts import text_to_speech
from services.aoai_whisper import transcribe_audio, transcribe_audio_from_filepath

def main():
    # Streamlit app title
    st.title("Ask with voice")
    # load custom CSS
    st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

    # Streamlit app state
    if "messages" not in st.session_state:
        st.session_state.messages = init_conversation()     
    if 'user_prompt' not in st.session_state:
        st.session_state.user_prompt = ""
    if "ai_response" not in st.session_state:
        st.session_state.ai_response = ""
    if 'text_ready' not in st.session_state:
        st.session_state.text_ready = False
    if 'audio_ready' not in st.session_state:
        st.session_state.audio_ready = False

    if 'voice_button' in st.session_state and st.session_state.voice_button == True:
        st.session_state.voice_button_running = True
    else:
        st.session_state.voice_button_running = False

    if 'send_button' in st.session_state and st.session_state.send_button == True:
        st.session_state.send_button_running = True
    else:
        st.session_state.send_button_running = False

    with st.container():
        user_prompt_element = st.text_input("Press the Voice Button to begin", disabled=True, value=st.session_state.user_prompt)
        col1, col2, col3 = st.columns([1.5, 7.5, 1])
        with col1:
            if st.button("🎤", disabled=st.session_state.voice_button_running, key='voice_button'):
                with col2:
                    with st.spinner("Listening..."):
                        # file_path = record_audio_to_local_til_silence()
                        audio_content = record_audio_til_silence()
                    with st.spinner("Transcribing..."):
                        # transcribed_text = transcribe_audio_from_filepath(file_path)
                        transcribed_text = transcribe_audio(audio_content)
                        st.session_state.user_prompt = transcribed_text
                    with st.spinner("Asking AI..."):
                        response = get_chat_response(transcribed_text)
                        st.session_state.ai_response = response
                        st.session_state.text_ready = True
                    # st.rerun()
                st.rerun()
        with col3:
            st.empty()
            # if not user_prompt_element:
            #     st.button("Send", disabled=True)
            # else:
            #     if st.button("Send", disabled=st.session_state.send_button_running, key='send_button'):
            #         response = get_chat_response(user_prompt_element)
            #         st.session_state.ai_response = response
            #         st.session_state.text_ready = True
            #         st.rerun()
    
    st.divider()
    # page layout with placeholders
    # Chat history display in a container at the top
    with st.container():
        if st.session_state.text_ready:            
            with st.spinner('generating response...'):
                # Convert text to speech
                speech_data = text_to_speech(st.session_state.ai_response)
                # Encode the speech data for embedding in HTML
                b64_audio = base64.b64encode(speech_data).decode()
                # Set the audio ready flag in session state
                st.session_state.audio_ready = True
                # Wait for the next iteration to display the audio player
                time.sleep(1)        
            
            if st.session_state.audio_ready:
                st.markdown(st.session_state.ai_response)
                audio_tag = f"""
                <div style='margin-top:20px;'>
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
                </div>
                """
                
                # Display the audio player in Streamlit
                st.markdown(audio_tag, unsafe_allow_html=True)

    # Reset button state after displaying the response
    if st.session_state.audio_ready:
        st.session_state.text_ready = False
        st.session_state.audio_ready = False
            
if __name__ == "__main__":
    main()