from dataclasses import dataclass,field,asdict
from json import load
from . import utils as ut

#load workspace folder settings
WORKSPACE_FOLDER = ut.load_workspace()
WORKSPACE_CONFIG = ut.load_workspace_config(WORKSPACE_FOLDER)

@dataclass()
class Compiler:
	path: str = field(default=None)
	cflags: list[str]= field(default_factory=list)
	lflags: list[str]= field(default_factory=list)
	include: list[str]= field(default_factory=list)
	link: list[str]= field(default_factory=list)
	external_objs: list[str]= field(default_factory=list)

	@staticmethod
	def from_config(config,alias="compiler"):
		if alias in config:
			if type(config[alias]) is str:
				config[alias] = Compiler(path=config[alias]);
			elif type(config[alias]) is dict:
				config[alias] = Compiler(**config[alias]);
			else:
				ut.cerr("Unexpected compiler options")
				exit()
		return config;

	@staticmethod
	def load_from(config, current,alias="compiler"):
		if alias in config:
			if type(config[alias]) is str:
				config[alias] = Compiler(path=config[alias])
			elif type(config[alias]) is dict:
				current[alias].update(config[alias])
				config[alias] =  Compiler(**current[alias])
		return config


@dataclass()
class ConfigData:
	version: str  = field()
	compiler: Compiler = field(default_factory=Compiler)
	makefile: bool = field(default=False)

	@staticmethod
	def load(path:str):
		config = ut.load_json_data(path)
		if type(config) is dict:
			config = Compiler.from_config(config)
			return ConfigData(**config);
		return None

	@staticmethod
	def load_from(path:str, current):
		config = asdict(current)
		loaded = ut.load_json_data(path)
		if type(loaded) is dict:
			loaded = Compiler.load_from(loaded,config)
			config.update(loaded)
		return ConfigData(**config)


if __name__=="__main__":
	config = ConfigData.load(WORKSPACE_CONFIG)
	print(config)
