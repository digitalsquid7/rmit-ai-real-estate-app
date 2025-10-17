import os
# from langchain.llms import OpenAI
from openai import OpenAI
import yaml


REAL_ESTATE_LISTINGS_PATH = "real_estate_listings.json"


def main():
    config = load_config('local.yaml')

    ai_client = OpenAI(
        base_url=config.base_url,
        api_key=config.api_key,
    )

    generate_real_estate_listings(ai_client)


class Config:
    def __init__(self):
        self.base_url = None
        self.api_key = None


def load_config(path):
    with open(path, 'r') as file:
        yaml_config = yaml.safe_load(file)

        config = Config()
        config.base_url = yaml_config['chat-gpt']['base-url']
        config.api_key = yaml_config['chat-gpt']['api-key']

        return config


def generate_real_estate_listings(ai_client):
    """Generates Real Estate listings using AI and saves the results as a JSON object to a local file.
    If the file already exists, this function does nothing."""

    if os.path.exists(REAL_ESTATE_LISTINGS_PATH):
        return

    prompt = """
    Generate 10 diverse Real Estate listings.
    Only generate fake data. Don't use real data.
    
    Each listing must be in the following JSON format:
    {
      "price": <integer>,
      "neighborhood": <string>,
      "property_type": <string>,
      "bedrooms": <integer>,
      "bathrooms": <integer>,
      "area_sqft": <integer>,
      "description": <3-4 sentences>
    }
    
    Return ONLY valid JSON structured as:
    {
      "listings": [ ... ]
    }
    """

    response = ai_client.chat.completions.create(
        model="gpt-5",
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": prompt}]
    )

    with open(REAL_ESTATE_LISTINGS_PATH, 'w') as file:
        file.write(response.choices[0].message.content)


if __name__ == "__main__":
    main()
