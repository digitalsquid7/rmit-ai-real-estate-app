import yaml


class Config:
    def __init__(self):
        self.api_key = None
        self.base_url = None
        self.real_estate_listings_path = None
        self.logging_level = None


def load_config(path):
    with open(path, 'r') as file:
        yaml_config = yaml.safe_load(file)

        config = Config()
        config.api_key = yaml_config['api-key']
        config.base_url = yaml_config['base-url']
        config.real_estate_listings_path = yaml_config['real-estate-listings-path']
        config.logging_level = yaml_config['logging-level']

        return config
