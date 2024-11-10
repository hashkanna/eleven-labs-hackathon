from .utils.env_loader import load_environment

env_vars = load_environment()

OPENAI_API_KEY = env_vars['OPENAI_API_KEY']
ELEVEN_API_KEY = env_vars['ELEVEN_API_KEY']
LUMA_API_KEY = env_vars['LUMA_API_KEY']
FFMPEG_PATH = env_vars['FFMPEG_PATH']