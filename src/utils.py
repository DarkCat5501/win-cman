from dataclasses import dataclass,is_dataclass
import os, sys, json
import inspect
import colorama as cl

cl.init()

def to_win_path(path):
	return os.path.abspath(path).replace('/','\\');

def norm_path(base, path):
	return os.path.normpath(os.path.join(base, path))

def warn(text):
	print(f"{cl.Back.YELLOW}{cl.Fore.BLACK} WARNING: {cl.Style.RESET_ALL} {text}",file=sys.stdout,end="\n")

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


def save_json_data(path:str, data):
	try:
		with open(path,"w") as file:	
			json.dump(data,file,ensure_ascii=True,check_circular=True,allow_nan=False,indent=1,sort_keys=False)
	except IOError as error:
		warn(f"couldn't save file {path}: {error}")
		return False
	return True

def settupManual():
		print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR:{cl.Style.RESET_ALL}\tinvalid workspace settup\n")
		print(f"\tHow to configure the workspace folder\n"
		"TODO:"
		"\n\n"
		f"if you already have the workspace settup then run this code as admin:\n\n\tSETX WORKSPACE_FOLDER <path> /M \n\nto set the path to your workspace folder")

def load_workspace():
	local = os.environ.get("WORKSPACE_FOLDER")
	if local is None:
		settupManual()
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
		local_file = os.path.join(workspace, "config/.wcm_config.json")
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing configuration file!:\nfile {local_file} does not exist")
			exit()
	else:
		cerr("invalid workspace settup!")
		exit()
		
def load_workspace_projects(workspace):
	local_file = os.environ.get("WORKSPACE_PROJETS")

	if local_file is not None:
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing projects file!:\nfile {local_file} does not exist")
			exit()
	elif workspace is not None:
		local_file = os.path.join(workspace, "config/.wcm_projects.json")
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing projects file!:\nfile {local_file} does not exist")
			exit()
	else:
		cerr("invalid workspace settup!")
		exit()

def load_workspace_templates(workspace):
	local_file = os.environ.get("WORKSPACE_TEMPLATES")
	if local_file is not None:
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing templates file!:\nfile {local_file} does not exist")
			exit()
	elif workspace is not None:
		local_file = os.path.join(workspace, "config/.wcm_templates.json")
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing templates file!:\nfile {local_file} does not exist")
			exit()
	else:
		cerr("invalid workspace settup!")
		exit()

def load_workspace_libraries(workspace):
	local_file = os.environ.get("WORKSPACE_LIBRARIES")
	if local_file is not None:
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing libraries file!:\nfile {local_file} does not exist")
			exit()
	elif workspace is not None:
		local_file = os.path.join(workspace, "config/.wcm_libraries.json")
		if os.path.exists(local_file):
			return local_file
		else:
			cerr(f"missing libraries file!:\nfile {local_file} does not exist")
			exit()
	else:
		cerr("invalid workspace settup!")
		exit()
	
def create_from(name:str,cls, data:dict,args=[]):
	variables = vars(cls)["__annotations__"]
	#list of (key,data,type)
	filtered = [(key,data[key],variables[key]) for key in data.keys() if key in variables.keys()]
	arguments = {}
	for key,value,tp in filtered:
		try:
			_value = [value] if "list" in str(tp) and "list" not in str(type(value)) else value
			if tp != type(value) and "list[" not in str(tp):
				raise TypeError()
			arguments.setdefault(key,tp(_value))
		except TypeError:
			tp_name = tp if type(tp) is str else tp.__name__
			cerr(f"an error has ocurred during {name} generation: variabel ({key}) expected `{tp_name}` but got `{type(value).__name__}`")
		
	try:
		inspect.signature(cls.__init__).bind(args,**arguments)
		out = cls(*args,**arguments)
		return out
	except TypeError as error:
		cerr(f"an error has ocurred during {name} generation: \n{error}")
		exit(1)
