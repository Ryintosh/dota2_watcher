import os
import json

def load_secret_config(filename):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', filename+".json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            try:
                config_data = json.load(f)
                return config_data
            except Exception as e:
                print(f"Error decoding JSON file '{filename}': {e}")
                return None
    else:
        print(f"Secret config file '{filename}' not found.")
        return None
