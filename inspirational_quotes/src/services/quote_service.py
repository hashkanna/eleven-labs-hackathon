import logging
from openai import OpenAI
from datetime import datetime

def generate_quote(api_key):
    """Generate an inspirational quote using OpenAI."""
    logging.info("Generating new quote...")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "Generate a unique, short, inspiring quote about creativity, success, or life. Make it original and not a famous quote."
        }]
    )
    quote = response.choices[0].message.content
    logging.info(f"Generated quote: {quote}")
    return quote 