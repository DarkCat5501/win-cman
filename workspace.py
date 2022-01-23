from dataclasses import dataclass, field
from enum import Enum, auto, unique
import json
import colorama as cl
import os

cl.init()

@unique
class PType(Enum):
	UNDEFINED = auto()
	C = auto()
	CPP = auto()
	NODE = auto()
	STYLED = auto()
	_count = auto()


@dataclass
class Project:
	name: str
	path: str
	type: PType

	@staticmethod
	def generate_project(name, path, type=PType.UNDEFINED, showStats = False):
		if type is PType.C:
			print("generating a new C project")
		elif type is PType.CPP:
			print("generation a new C++ project")

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
		pass

	@staticmethod
	def loaddef(spath, recursion = -1, showStats = False):
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
	def check_libdef_json(spath, showStats = False):
		dir_files = [f for f in  os.listdir(spath) if os.path.isfile( os.path.join(spath, f) )]
		if "libdef.json" in dir_files:
			lib = Library.loaddef(spath,showStats = showStats)
			return lib
		return None
		
			

	@staticmethod
	def find(spath, skip=[], recurion = -1, showStats = False):
		for dir in [os.path.join(spath, _d) for _d in  os.listdir(spath)]:
			_isdir = os.path.isdir(dir)
			if _isdir and not dir in skip:
				print(f"found file at:{dir}")


@dataclass
class Compiler:
	path:str

class Workspace:
	compilers: list[Compiler]	= []
	libraries: list[Library]	= []

	def __init__(self,path) -> None:
		self.path = path
		if not self.checkValidity():
			exit(1)
		pass
	
	
	def load_library_catalog_data(self, path:str):
		catalog_file = os.path.join(path, "catalog.json");
		has_catalog = os.path.exists(catalog_file)
		if has_catalog:
			try:
				data = {}
				with open(catalog_file, "r") as _catalog:
					data = json.load(_catalog)
				return ( data , catalog_file ) 
			except json.JSONDecodeError as error:
				print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR: {cl.Style.RESET_ALL} invalid catalog.json!")
				print(error)
				exit(1)
		else:
			print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR: {cl.Style.RESET_ALL} {catalog_file} not found!")
			exit(1)

	def check_libraries(self, file_path, data, recursion = -1,showStats = False):
		total_valid_libraries = 0;
		total_invalid_libraries = 0;
		total_libraries = len(data.keys())
		if  total_libraries < 1:
			print(f"{cl.Back.YELLOW}{cl.Fore.BLACK}WARNING: {cl.Style.RESET_ALL} no libraries were found in {file_path}!\n")

		else:
			current_path =  os.path.dirname(file_path)
			for library in  data:
				lib = Library.load(library,current_path,data[library],showStats=showStats)
				if lib is None:
					total_invalid_libraries += 1
				else:
					total_valid_libraries += 1

			if showStats:
				print(f"{cl.Back.YELLOW}{cl.Fore.BLACK}Found: {total_libraries} libraries; {total_valid_libraries} valid, {total_invalid_libraries} with error{cl.Style.RESET_ALL}")

		return (total_valid_libraries, total_invalid_libraries )

	def list_libraries(self):
		libs_dir = os.path.join(self.path, "libs")
		if not os.path.exists(libs_dir):
			return None

		print(f"{cl.Style.DIM}{cl.Back.CYAN}{cl.Fore.BLACK}libraries in {libs_dir} {cl.Style.RESET_ALL}")
		( data, catalog_path ) = self.load_library_catalog_data(libs_dir)
		self.check_libraries(catalog_path, data, showStats=True)
		
		return True

	def settupManual(self):
		print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR:{cl.Style.RESET_ALL}\tinvalid workspace settup\n")
		print(f"\tHow to configure the workspace folder\n"
		"TODO:"
		"\n\n"
		f"if you already have the workspace settup then run this code as admin:\n\n\tSETX WORKSPACE_FOLDER <path> /M \n\nto set the path to your workspace folder")

	def checkValidity(self):
		if not self.valid():
			#TODO: try to settup workspace path automatic
			self.settupManual()
			exit(1)
		return True

	def valid(self):
		if self.path is None: return False
		return os.path.exists(self.path)
	
	def setWorkspace(self, path):
		os.putenv("WORKSPACE_FOLDER",path)
		pass

	def printInfo(self):
		print(f"current workspace folder: {self.path}\n\n")
		if self.list_libraries() is None:
			print(f"{cl.Back.YELLOW}{cl.Fore.BLACK}WARN{cl.Style.RESET_ALL}: libs folder not found!")



if __name__=="__main__":
	current_workspace = Workspace(os.environ.get("WORKSPACE_FOLDER"))
	current_workspace.printInfo()
