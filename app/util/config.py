import json

CONFIG_FILE_NAME = "config.json"

def load():
	try:
		with open(CONFIG_FILE_NAME, 'r') as f:
			return json.load(f)
	except FileNotFoundError:
		print(f"File '{CONFIG_FILE_NAME}' not found.")
	except json.JSONDecodeError as e:
		print(f"Error decoding JSON from '{CONFIG_FILE_NAME}': {e}")

def save(data):
	try:
		with open(CONFIG_FILE_NAME, 'w') as f:
			json.dump(data, f, indent=4)
		print(f"Data saved to '{CONFIG_FILE_NAME}'.")
	except Exception as e:
		print(f"Error saving data to '{CONFIG_FILE_NAME}': {e}")