import requests

def text_to_speech(text, api_key):
    """Convert text to speech using ElevenLabs API."""
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
        with open('temp_audio.mp3', 'wb') as audio_file:
            audio_file.write(response.content)
        return 'temp_audio.mp3'
    msg = f"Failed to generate audio. Status: {response.status_code}"
    raise requests.RequestException(msg) 