from openai import OpenAI

def generate_quote(api_key):
    """Generate an inspirational quote using OpenAI."""
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "Generate a short, inspiring quote about creativity, success, or life."
        }]
    )
    return response.choices[0].message.content 