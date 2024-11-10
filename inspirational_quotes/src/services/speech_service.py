import requests
import logging

def text_to_speech(text, api_key, path_manager):
    """Convert text to speech using ElevenLabs API."""
    logging.info("Generating audio from text...")
    voice_id = '21m00Tcm4TlvDq8ikWAM'
    response = requests.post(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
        headers={
            'xi-api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'audio/mpeg'
        },
        json={'text': text},
        timeout=30
    )
    
    if response.status_code == 200:
        audio_path = path_manager.get_temp_path('temp_audio.mp3')
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(response.content)
        logging.info(f"Audio generated successfully: {audio_path}")
        return audio_path
    
    msg = f"Failed to generate audio. Status: {response.status_code}"
    logging.error(msg)
    raise requests.RequestException(msg) 