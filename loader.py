import os
import json
import sys

def cerr(text):
	print(f"ERROR: {text}",file=sys.stderr)

def load_json(path:str) -> dict:
	try:
		with open(path,"r") as file:
			data = json.load(file)
		return data
	except IOError:
		cerr(f"couldn't load file {path}")
	except json.JSONDecodeError as error:
		cerr(f"invalid json file!\n\t{error}")
	return None
