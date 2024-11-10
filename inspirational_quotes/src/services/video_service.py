import time
import requests
import logging
from lumaai import LumaAI

def generate_video(quote, api_key, path_manager):
    """Generate video using LumaAI based on the quote."""
    logging.info("Starting video generation with LumaAI...")
    client = LumaAI(auth_token=api_key)
    prompt = (
        f"A cinematic scene that captures the essence of this quote: {quote}. "
        "Use inspiring visuals with smooth camera movements."
    )
    
    logging.info(f"Using prompt: {prompt}")
    generation = client.generations.create(
        prompt=prompt,
        loop=True,
        aspect_ratio="16:9"
    )
    
    while True:
        time.sleep(3)
        generation = client.generations.get(id=generation.id)
        logging.info(f"Video generation status: {generation.state}")
        
        if generation.state == "completed":
            video_url = generation.assets.video
            response = requests.get(video_url, timeout=30)
            video_path = path_manager.get_temp_path('temp_video.mp4')
            with open(video_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"Video generated successfully: {video_path}")
            return video_path
            
        if generation.state == "failed":
            error_msg = "Video generation failed"
            logging.error(error_msg)
            raise RuntimeError(error_msg) 