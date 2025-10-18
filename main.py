import logging

from openai import OpenAI

from home_match.config import load_config
from home_match.database import setup_collection, query_collection
from home_match.genai import generate_real_estate_listings, generate_home_recommendation


def main():
    print(r"""
      _    _                        __  __       _       _     
     | |  | |                      |  \/  |     | |     | |    
     | |__| | ___  _ __ ___   ___  | \  / | __ _| |_ ___| |__  
     |  __  |/ _ \| '_ ` _ \ / _ \ | |\/| |/ _` | __/ __| '_ \ 
     | |  | | (_) | | | | | |  __/ | |  | | (_| | || (__| | | |
     |_|  |_|\___/|_| |_| |_|\___| |_|  |_|\__,_|\__\___|_| |_|

     """)

    # Setup config, logging, AI client, real estate listings and ChromaDB collection.
    config = load_config('config.yaml')
    setup_logging(config)
    ai_client = OpenAI(base_url=config.base_url, api_key=config.api_key)
    generate_real_estate_listings(config, ai_client)
    collection = setup_collection(config)

    # Gather user input.
    print("Describe your perfect home, what would it look like? What features or qualities matter most to you?")
    user_input = input("> ")

    # Retrieve relevant listing from ChromaDB collection and use AI to generate a personalised recommendation.
    relevant_listings = query_collection(collection, user_input)
    recommendation = generate_home_recommendation(user_input, relevant_listings, ai_client)
    print(f"\n{recommendation}")


def setup_logging(config):
    logging.basicConfig(level=config.logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set noisy loggers to WARNING level.
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger('chromadb').setLevel(logging.WARNING)


if __name__ == "__main__":
    main()
