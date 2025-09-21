import os
from openai import OpenAI

endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o-mini"

client = None

# Sends a question to the OpenAI API using the provided API key and returns the model's response as a string.
# Parameters:
#   question (str): The user's question to send to the model.
#   system_prompt (str): Optional system prompt for the assistant's behavior.
#   api_key (str): The user's OpenAI API key (required).
# Returns: The model's response or an error message if not available.

def ask_openai(question, system_prompt="You are a helpful assistant.", api_key=None):
    if not api_key:
        raise ValueError("API key (token) is required for OpenAI requests.")
    _client = OpenAI(base_url=endpoint, api_key=api_key)
    response = _client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        model=model_name,
        stream=False
    )
    if hasattr(response, 'choices') and response.choices:
        return response.choices[0].message.content
    return "No response from model."