from dataclasses import dataclass, field
from distutils import command
from enum import Enum, auto, unique
import json
from msilib.schema import Property
from tkinter import UNDERLINE
from xml.etree.ElementInclude import default_loader
import colorama as cl
import os

from numpy import lib

cl.init()

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

		# for dir in [os.path.join(start_path, _d) for _d in  os.listdir(start_path)]:
		# 	_isdir = os.path.isdir(dir)
		# 	if _isdir and not dir in skip:
		# 		print(f"found file at:{dir}")

@unique
class DType(Enum): #Dependency Type
	UNDEFINED = auto()
	LIB = auto()
	PROJ = auto()
	_count = auto()

@dataclass
class Dependency:
	data: object
	type: DType = field(default=DType.UNDEFINED)

	@staticmethod
	def parse_dependency(data):
		pass

@unique
class PType(Enum):
	UNDEFINED = auto()
	C = auto()
	CPP = auto()
	NODE = auto()
	_count = auto()

@dataclass
class Project:
	name: str #name of the project
	path: str #absolute path to the project folder
	type: PType = field(default=PType.UNDEFINED)
	dependencies: list = field(default_factory=list)

	@staticmethod
	def generate_project(name, path, type=PType.UNDEFINED, showStats = False):
		if type is PType.C:
			print("generating a new C project")
		elif type is PType.CPP:
			print("generation a new C++ project")

	def load_cman_proj_json(self, showStats=False):
		config_file = os.path.join(self.path, "cman-proj.json")
		has_project_config = os.path.exists(config_file)
		if has_project_config:
			try:
				data = {}
				with open(config_file, "r") as _catalog:
					data = json.load(_catalog)
				return ( data , config_file ) 
			except json.JSONDecodeError as error:
				print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR{cl.Style.RESET_ALL}: invalid file {config_file}!")
				print(error)
		return None

	def load_project_data(self,showStats=False):
		config = self.load_cman_proj_json(showStats=showStats)
		if config is not None:
			(_data, _file) = config
			#update current variables
			if "name" in _data: self.name = _data["name"];
			if "type" in _data:
				if _data["type"] in PType.__members__:
					self.type = PType[ _data["type"] ]
			if "dependencies" in _data: self.dependencies = _data["dependencies"]
			return _data
		return None

	@staticmethod
	def find(start_path, skip=[], recurion = -1, showStats = False):
		#walk through all folders and set them as projects
		for dir in [d for d in os.listdir(start_path) if (os.path.isdir(os.path.join(start_path,d)) and not d in skip) ]:
			project = Project(name=dir, path=os.path.join(start_path, dir))
			if project.load_project_data() is not None:
				print(project)
				yield project

	# @staticmethod
	# def load(name,start_path, data, recursion = -1, showStats = False):
	# 	project = Project(name=name, path=start_path)
	# 	project.check_valid()


	# 	lib_path = os.path.join(start_path, name) if not "path" in data else os.path.join(start_path, data["path"])
	# 	if not os.path.exists(lib_path):
	# 		return None
	# 	if showStats:
	# 		print(f"\t{cl.Fore.CYAN}lib{cl.Style.RESET_ALL}: {name} : {lib_path}")

	# 	return True	



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
	
	def load_catalog_data(self, path:str, required=True):
		catalog_file = os.path.join(path, "catalog.json");
		has_catalog = os.path.exists(catalog_file)
		if has_catalog:
			try:
				data = {}
				with open(catalog_file, "r") as _catalog:
					data = json.load(_catalog)
				return ( data , catalog_file ) 
			except json.JSONDecodeError as error:
				print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR{cl.Style.RESET_ALL}: invalid catalog.json!")
				print(error)
				if required:
					exit(1)
		else:
			if required:
				print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR{cl.Style.RESET_ALL}: {catalog_file} not found!")
				exit(1)
			else:
				print(f"{cl.Back.YELLOW}{cl.Fore.BLACK}WARN{cl.Style.RESET_ALL}: {catalog_file} not found!")
		return None

	##libraries START#############################################
	# TODO: add libraries
	# def add_library_to_catalog_json(self, path:str, library: Library):
		
	# 	#a bit of safety check
	# 	if not Library.validate():
	# 		print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR{cl.Style.RESET_ALL}: trying to save an invalid library: {library.name} ")
	# 		exit(1)
	# 		return None

	# 	catalog_file = os.path.join(path, "catalog.json");
	# 	has_catalog = os.path.exists(catalog_file)
	# 	if has_catalog:
	# 		try:
	# 			data = {}
	# 			with open(catalog_file, "rw") as _catalog:
	# 				data = json.load(_catalog)
	# 				data.update()

	# 			return ( data , catalog_file ) 
	# 		except json.JSONDecodeError as error:
	# 			print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR: {cl.Style.RESET_ALL} invalid catalog.json!")
	# 			print(error)
	# 			exit(1)
	# 	else:
	# 		print(f"{cl.Back.RED}{cl.Fore.BLACK}ERROR: {cl.Style.RESET_ALL} {catalog_file} not found!")
	# 		exit(1)
	def findLibraries(self,path=None,showStats=False):
		find_path = path if path is not None else os.path.join(self.path,"libs")
		found_libs:list[Library] = [l for l in Library.find(find_path,skip=[],showStats=showStats)]

		if len( found_libs ) < 1:
			print(f"{cl.Back.YELLOW}{cl.Back.BLACK}NO LIBRARIES FOUND{cl.Style.RESET_ALL}: Any file was found at {find_path}")
		else:
			for lib in found_libs:
				print(f"{lib}")

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
		( data, catalog_path ) = self.load_catalog_data(libs_dir)
		self.check_libraries(catalog_path, data, showStats=True)
		
		return True

	##libraries END #############################################

	##projects START #############################################

	def parse_projects(self,data, showStats=False):
		pass

	def list_projects(self):
		proj_dir = os.path.join(self.path, "projects")
		if not os.path.exists(proj_dir):
			return None

		#check for project catalog
		#catalog = self.load_catalog_data(proj_dir,required=False)

		project_list:list[Project] = []
		skip_folders = []
		

		# #load projects from catalog if not None
		# if catalog is not None: 
		# 	(projects, path) = catalog;
		# 	for project in projects:
		# 		print(project)
			
		folder_projects = [ p for p in Project.find(proj_dir,skip=skip_folders)]
		if len(project_list) < 1:
			print(f"{cl.Style.DIM}{cl.Back.CYAN}{cl.Fore.BLACK}No projects found in {proj_dir}{cl.Style.RESET_ALL}")
		else:
			print(f"{cl.Style.DIM}{cl.Back.CYAN}{cl.Fore.BLACK}Projects in {proj_dir} {cl.Style.RESET_ALL}")
	
		
		# print(f"{cl.Style.DIM}{cl.Back.CYAN}{cl.Fore.BLACK}Projects in {proj_dir} {cl.Style.RESET_ALL}")
		# Project.

		# Project.find(proj_dir)
		return True

	##projects END   #############################################

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
		print("Workspace:")
		print(f"current workspace folder: {self.path}")
	
	def parseAction(self,args):
		if args.subcommand == "libs":
			if args.list: self.list_libraries();
				
		elif args.subcommand == "proj":
			if args.list: self.list_projects();

		elif args.subcommand == "gen":
			print("command gen")
		else:
			print("No arguments provided!")

if __name__=="__main__":
	current_workspace = Workspace(os.environ.get("WORKSPACE_FOLDER"))
	current_workspace.printInfo()
