import time
import requests
from lumaai import LumaAI

def generate_video(quote, api_key):
    """Generate video using LumaAI based on the quote."""
    client = LumaAI(auth_token=api_key)
    prompt = (
        f"A cinematic scene that captures the essence of this quote: {quote}. "
        "Use inspiring visuals with smooth camera movements."
    )
    
    generation = client.generations.create(
        prompt=prompt,
        loop=True,
        aspect_ratio="16:9"
    )
    
    while True:
        time.sleep(3)
        generation = client.generations.get(id=generation.id)
        print(f"Video generation status: {generation.state}")
        
        if generation.state == "completed":
            video_url = generation.assets.video
            response = requests.get(video_url, timeout=30)
            video_path = 'temp_video.mp4'
            with open(video_path, 'wb') as file:
                file.write(response.content)
            return video_path
        if generation.state == "failed":
            raise RuntimeError("Video generation failed") 