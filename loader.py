from src import utils as ut
import os
import json


def load_json(path:str) -> dict:
	try:
		with open(path,"r") as file:
			data = json.load(file)
		return data
	except IOError:
		ut.cerr(f"couldn't load file {path}")
	except json.JSONDecodeError as error:
		ut.cerr(f"invalid json file!\n\t{error}")
	return None


if __name__=="__main__":
	load_json("teste.json")



@dataclass
class Library:
	name: str
	path:str
	include: str 	= field(default="include")   #its include folder
	src: str     	= field(default="src")       #its source folder
	obj: str	 	= field(default="obj") 		 #its objects folder
	link: str	 	= field(default="libs") 	 #its link folder
	make: bool 		= field(default=True)		 #tels the compiler if it have com call make before getting the objects or link

	defines: list[str]  = field(default_factory=list)
	links:   list[str] 	= field(default_factory=list)

	def validate(self):
		return True

	def load_libdef_json(self, showStats=False):
		def_file = os.path.join(self.path, "libdef.json")
		has_def_file = os.path.exists(def_file)
		if has_def_file:
			try:
				data = {}
				with open(def_file, "r") as _catalog:
					data = json.load(_catalog)
				return ( data , def_file )
			except json.JSONDecodeError as error:
				print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR{cl.Style.RESET_ALL}: invalid file {def_file}!")
				print(error)
		return None

	def load_libdef_data(self,showStats=False):
		config = self.load_libdef_json(showStats=showStats)
		if config is not None:
			(_data, _file) = config
			#update current variables
			if "name" in _data: self.name = _data["name"];
			return _data
		return None

	@staticmethod
	def load(name,spath, data, recursion = -1, showStats = False):
		lib_path = os.path.join(spath, name) if not "path" in data else os.path.join(spath, data["path"])
		if not os.path.exists(lib_path):
			return None
		if showStats:
			print(f"\t{cl.Fore.CYAN}lib{cl.Style.RESET_ALL}: {name} : {lib_path}")
		return True

	@staticmethod
	def find(start_path, skip=[], recurion = -1, showStats = False):
		#walk through all folders and set them as projects
		for dir in [d for d in os.listdir(start_path) if (os.path.isdir(os.path.join(start_path,d)) and not d in skip) ]:
			library = Library(name=dir, path=os.path.join(start_path, dir))
			if library.load_libdef_data() is not None:
				yield library
				