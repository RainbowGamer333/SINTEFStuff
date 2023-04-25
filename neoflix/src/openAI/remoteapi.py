import yaml
import os
import openai

def loadCredential():
    with open("../openai.credential", 'r') as stream:
        credential_data = yaml.safe_load(stream)
    openai_config = credential_data['openai']
    openai.api_type = "azure"
    openai.api_base = openai_config['endpoint']
    openai.api_version = "2023-03-15-preview"
    openai.api_key = openai_config["key"]