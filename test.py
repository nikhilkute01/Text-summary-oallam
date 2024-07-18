import click
import requests

# Constants
OLLAMA_API_KEY = 'your_ollama_api_key'
OLLAMA_URL = 'https://api.ollama.com/v1/ollama/summarize'
MODEL_NAME = 'qwen2-0.5B'

@click.command()
@click.option('-t', '--text', type=str, help='Text or path to a text file to summarize.')
def summarize(text):
    """Summarize text using Ollama API."""
    if text.lower().endswith('hello.txt'):
        # Read text from file
        try:
            with open(text, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            click.echo(f"Error: File '{text}' not found.")
            return

    # Make API request to Ollama
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OLLAMA_API_KEY}'
    }
    data = {
        'model': MODEL_NAME,
        'text': text
    }
    try:
        response = requests.post(OLLAMA_URL, json=data, headers=headers)
        if response.status_code == 200:
            summary = response.json()['summary']
            click.echo(f".Summary of {text if len(text) < 50 else 'text pasted'}.\n")
            click.echo(summary)
        else:
            click.echo(f"Error: Failed to summarize. Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    summarize()
