from pathlib import Path
from dotenv import load_dotenv
import os

def load_environment():
    env_path = Path('.') / '.env'
    load_dotenv(env_path)
    
    required_vars = [
        'OPENAI_API_KEY',
        'ELEVEN_API_KEY',
        'LUMA_API_KEY',
        'FFMPEG_PATH'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    return {var: os.getenv(var) for var in required_vars}