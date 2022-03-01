import os, sys, json

def warn(text):
	print(f"WARNING: {text}",file=sys.stdout)

def cerr(text):
	print(f"ERROR: {text}",file=sys.stderr)

def load_json_data(path:str):
    data = None
    try:
        with open(path,"r") as file:
            data = json.load(file)
    except IOError:
        cerr(f"couldn't load file {path}")
    except json.JSONDecodeError as error:
        cerr(f"invalid JSON file:\n{error}")
    return data

def load_workspace():
	local = os.environ.get("WORKSPACE_FOLDER")
	if local is None:
		cerr("you haven't settup a workspace yet!")
		exit()
	return local

def load_workspace_config(workspace):
	local_file = os.environ.get("WORKSPACE_CONFIG")
	if local_file is not None:
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing configuration file!:\nfile {local_file} does not exist")
			exit()
	elif workspace is not None:
		local_file = os.path.join(workspace, ".wcm_config.json")
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing configuration file!:\nfile {local_file} does not exist")
			exit()
	else:
		cerr("invalid workspace settup!")
		exit()
