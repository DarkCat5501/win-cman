from dataclasses import asdict, dataclass, field
import os
from unicodedata import name
from . import utils as ut
from beautifultable import BeautifulTable as Table
import colorama as cl
import argparse as agp


class ZipArgument(agp.Action):
	def __init__(self,attr, *args, **kwargs):
		self.attr = attr;
		super(ZipArgument, self).__init__(*args, **kwargs)

	def __call__(self, parser, namespace, values, option_string): 
		try:
			attr_data = getattr(namespace,self.attr)
			self_data = getattr(namespace,self.dest)
			to_add = len(attr_data) - len(self_data)-1
			if to_add > 0 :
				for i in [[]]*to_add: self_data.append(i);
			self_data.append(values)
			setattr(namespace, self.dest, self_data)
		except Exception as error:
			parser.error(f"{self.attr} not provided: {error}")
		
class FileValid(agp.Action):
	def __init__(self, abs:bool, *args, **kwargs):
		self.abs = abs
		super(FileValid, self).__init__(*args, **kwargs)

	def check__file_exist(self, path):
		_path = path
		if self.abs: _path = os.path.abspath(path);
		if not os.path.exists(_path):
			print("Not exist")
			raise IOError(f"File `{path}` is not a valid directory ")
		else:
			return _path

	def __call__(self, parser, namespace, values, option_string): 
		try:
			values = self.check__file_exist(values)
			setattr(namespace, self.dest, values)
		except IOError as error:
			parser.error(f"{error}")
		except TypeError as error:
			print(values)
			parser.error(f"mais de um arquivo foi enviado para o parâmetro `{self.dest}`: {error}")
		except Exception as error:
			parser.error(f": {error}")

# class FileAt(agp.Action):
# 	def __init__(self,path:str, abs:bool, *args, **kwargs):
# 		self.path = path
# 		self.abs = abs
# 		super(ZipArgument, self).__init__(*args, **kwargs)

# 	def check__file_exist(self, files:list):
# 		output = []
# 		for path in files:
# 			_path = ut.norm_path(self.path,path)
# 			if self.abs: _path = os.path.abspath(_path);
# 			if not os.path.exists(_path):
# 				IOError(f"File `{path}` is not in directory `{self.path}` ")
# 			else:
# 				output.append(_path)
# 		return output

# 	def __call__(self, parser, namespace, values, option_string): 
# 		try:
# 			values = self.check__file_exist(values if isinstance(values,list) else [values])
# 			self_data = getattr(namespace,self.dest)
# 			self_data.append(values)
# 			setattr(namespace, self.dest, self_data)
# 		except IOError as error:
# 			parser.error(f"{error}")

# class FileAtAttr(agp.Action):
# 	def __init__(self,attr:str, abs:bool, *args, **kwargs):
# 		self.attr = attr
# 		self.abs = abs
# 		super(ZipArgument, self).__init__(*args, **kwargs)

# 	def check__file_exist(self, s_path:str, files:list):
# 		for path in files:
# 			_path = ut.norm_path(s_path,path)
# 			if self.abs: _path = os.path.abspath(_path);
# 			if not os.path.exists(_path):
# 				IOError(f"File `{path}` is not in directory `{s_path}` ")

# 	def __call__(self, parser, namespace, values, option_string): 
# 		try:
# 			attr_data = getattr(namespace,self.attr)
# 			self.check__file_exist(attr_data, values if isinstance(values,list) else [values])
# 			self_data = getattr(namespace,self.dest)
# 			self_data.append(values)
# 			setattr(namespace, self.dest, self_data)
# 		except IOError as error:
# 			parser.error(f"{error}")



@dataclass
class BaseProjectConfig:
	name: str
	path: str			= field(default=".")
	description: str	= field(default=" * No description * ")
	groups: list[str]   = field(default_factory=list)

@dataclass
class ProjectManager:
	path: str;
	projects:dict[BaseProjectConfig] = field(default_factory=dict);

	def __post_init__(self):
		projects_data = ut.load_json_data(self.path);

		for proj in projects_data:
			self.new_project(proj)

	def update_projects_file(self):
		if not ut.save_json_data(self.path, [ asdict(proj) for name, proj in self.projects.items() ]):
			ut.cerr("Projects were not updated!")

	def new_project(self, config:dict,check_path=False):
		_path = ut.to_win_path(config["path"])
		if check_path and not os.path.isdir(_path):
			ut.cerr(f"path: { config['path'] } is not a valid project directory!")
			exit(1)
		_project = ut.create_from("Project",BaseProjectConfig,config,[])
		_name = _project.name;
		_tries = 1
		while _name in self.projects:
			_name = _project.name + f"-{_tries}"
			_tries+=1
		if _name != _project.name:
			ut.warn(f"Trying to load similar named projects: Renamed to {_name}")
			_project.name = _name
		self.projects[_name] = _project
		return _project

	def rename_project(self,name,new_name):
		if not name in self.projects:
			ut.cerr(f"Trying to rename an inexistent project: `{name}`!")
			return False
		elif new_name in self.projects:
			ut.cerr(f"Trying to name a project with an existing name: `{name}` -> `{new_name}`!")
			return False
		tmp = self.projects[name]
		del self.projects[name]
		tmp.name = new_name
		self.projects[new_name] = tmp
		return True

	def add_groups(self, name, groups):
		added = 0
		if len(groups) == 0: return added
		if name in self.projects:
			__proj = self.projects[name]
			for gp in groups:
				if not gp in __proj.groups:
					__proj.groups.append(gp)
					added+=1
				else: ut.warn(f"project {name} is already in the group `{gp}`!")
		return added

	def remove_groups(self, name, groups):
		removed = 0
		if len(groups) == 0: return removed
		if name in self.projects:
			__proj = self.projects[name]
			for gp in groups:
				if gp in __proj.groups:
					__proj.groups.remove(gp)
					removed+=1
				else: ut.warn(f"project {name} is not in group `{gp}`!")
		return removed


	def delete_project(self, name):
		if name in self.projects:
			tmp = self.projects[name]
			del self.projects[name]
			return tmp
		return None

	def list_project_names(self) -> list[str]:
		return list(self.projects.keys())

	def list_project(self,use_colors = False, filter_groups=None):
		for pname,proj in self.projects.items():
			if filter_groups is not None and not any(x in proj.groups for x in filter_groups):
				continue
			if use_colors:
				yield ("",f"{cl.Fore.GREEN}{pname}{cl.Fore.RESET}",f"{cl.Fore.YELLOW}{','.join(proj.groups)}{cl.Fore.RESET}",f"{cl.Fore.CYAN}{proj.description}{cl.Fore.RESET}")
			else :
				yield ("",pname,",".join(proj.groups), proj.description)

	def show_projects(self, use_colors = False, filter_groups=None):	
		tabele = Table(maxwidth=100)
		tabele.set_style(Table.STYLE_BOX)
		tabele.columns.header = ("***","name","group","description") if not use_colors else ("***",f"{cl.Fore.GREEN}name{cl.Fore.RESET}",f"{cl.Fore.YELLOW}groups{cl.Fore.RESET}",f"{cl.Fore.CYAN}description{cl.Fore.RESET}")
		tabele.columns.width = 70;tabele.columns.width[0] = 5;tabele.columns.width[1] = tabele.columns.width[2] = 30
		tabele.columns.alignment = Table.ALIGN_LEFT
		for line in tabele.stream(self.list_project(use_colors,filter_groups)):
			print(line)

	def show_info(self,project=None,name=False,path=True,description=False,groups=False, use_colors = True):
		if name is None:
			print(f"Current projects list folder: {self.path}")
			print(f" {len(self.projects.keys())} projects loaded")
		else:
			if not project in self.projects:
				ut.cerr(f"Project `{project}` not found!")
				exit(1)
			_project = self.projects[project]
			if not name and not path and not description and not groups:
				ut.warn("Your dum ass! what you want!!!!")
				exit(1)
			tabele = Table(maxwidth=120);tabele.set_style(Table.STYLE_BOX)
			fields = []
			if name: fields.append("name")# if not use_colors else f"{cl.Fore.GREEN}name{cl.Fore.RESET}" )
			if path: fields.append("path")# if not use_colors else f"{cl.Fore.GREEN}path{cl.Fore.RESET}" )
			if groups: fields.append("groups")# if not use_colors else f"{cl.Fore.GREEN}groups{cl.Fore.RESET}" )
			if description: fields.append("description")# if not use_colors else f"{cl.Fore.GREEN}description{cl.Fore.RESET}" )
			data = [getattr(_project,value) for value in fields]
			tabele.columns.header = fields
			tabele.columns.alignment = Table.ALIGN_LEFT
			tabele.rows.append([",".join(dt) if isinstance(dt,list) else dt for dt in data ])
			print(tabele)

			
	def try_open(self, name, editor, terminal,explorer):
		if name is not None:
			if name in self.projects:
				p_path = ut.to_win_path(self.projects[name].path)
				if editor: os.system(f"code \"{p_path}\"")
				if terminal: os.system(f"wt -w 1 -d \"{p_path}\"")
				if explorer: os.system(f"explorer \"{p_path}\"")
			else:
				ut.cerr(f"Project \"{name}\" not found!")

		elif editor or terminal:
			ut.cerr("No project name was provided!")
			
	##start argparse functions
	@staticmethod
	def add_parser_lister_arguments(parser: agp.ArgumentParser):
		parser.add_argument('-color', help="enables colorization",action=agp.BooleanOptionalAction,default=False,required=False,dest="use_colors")
		parser.add_argument('-groups',"--g", help="filter by group name",nargs="+",action="extend",default=None,dest="filter_groups")
		
	@staticmethod
	def add_parser_editor_arguments(parser: agp.ArgumentParser):
		parser.add_argument("projects",help="project(s) to be edited",nargs="+",action="append")
		parser.add_argument("-p",help="project(s) to be edited",nargs="+",action="append",dest="projects")
		parser.add_argument("-add-group","--ag",nargs="+",action=ZipArgument,attr="projects", help="adds the project into a new group, if its not already in",dest="add_groups", default=[])
		parser.add_argument("-remove-group","--rg",nargs="+",action=ZipArgument,attr="projects", help="remore groups from projects",dest="remove_groups", default=[])
		parser.add_argument("-rename","--rn",nargs="+", action=ZipArgument,attr="projects", help="adds the project into a new group, if its not already in",dest="rename_projects", default=[])
		parser.add_argument("-power-rename","--prn",nargs=1,type=str, action=ZipArgument,attr="projects", help="adds the project into a new group, if its not already in",dest="power_rename_projects", default=[])

	@staticmethod
	def add_parser_opener_arguments(parser: agp.ArgumentParser):
		parser.add_argument("project",help="The name of the project to be open",action="store")
		parser.add_argument("--code","-c",help="Open a specific project in default editor",action=agp.BooleanOptionalAction,default=True)
		parser.add_argument("--terminal","-t",help="Open the project in a terminal",action=agp.BooleanOptionalAction,default=False)
		parser.add_argument("--explorer","-e",help="Open the project folder in explorer",action="store_true",default=False)

	@staticmethod
	def add_parser_adder_arguments(parser: agp.ArgumentParser):
		parser.add_argument("project_name",help="The name for the project to be added",action="store")
		parser.add_argument("project_path",help="The path to the project to be added",action=FileValid,abs=True)
		parser.add_argument("-d",help="Description for the project",action="store",default=None, dest="project_description")
		parser.add_argument("-add-group","--ag",nargs="+",action="extend",help="adds the project into groups",dest="projects_groups", default=[])

	@staticmethod
	def add_parser_info_arguments(parser: agp.ArgumentParser):
		parser.add_argument("info_project",help="The name for the project to be added",action="store")
		parser.add_argument("-n","--name",help="Shows the name of the project",action=agp.BooleanOptionalAction, default=False, dest="info_name")
		parser.add_argument("-p","--path",help="Shows the path of the project",action=agp.BooleanOptionalAction, default=True, dest="info_path")
		parser.add_argument("-d","--description",help="Shows the description of the project",action=agp.BooleanOptionalAction, default=False, dest="info_description")
		parser.add_argument("-g","--groups",help="Shows the name of the project",action=agp.BooleanOptionalAction, default=False, dest="info_groups")
		#TODO: add type query

	@staticmethod
	def add_parser_remover_arguments(parser: agp.ArgumentParser):
		parser.add_argument("project_names",help="Project to be removed from management",nargs="+",action="extend")

	@staticmethod
	def add_parser_arguments(parser:agp.ArgumentParser):
		p_parser = parser.add_subparsers(help="project actions",dest="_project_action")
		opener_parser = p_parser.add_parser("open",help="opens a specified project")
		editor_parser = p_parser.add_parser("edit",help="edit information about one or multiple projects")
		lister_parser = p_parser.add_parser("list",help="list all projects")
		adder_parser = p_parser.add_parser("add",help="adds a new project directly to projects list")
		remover_parser = p_parser.add_parser("remove",help="removes a project from management list")
		info_parser = p_parser.add_parser("info",help="shows info of an specific project")
		ProjectManager.add_parser_opener_arguments(opener_parser)
		ProjectManager.add_parser_editor_arguments(editor_parser)
		ProjectManager.add_parser_lister_arguments(lister_parser)
		ProjectManager.add_parser_adder_arguments(adder_parser)
		ProjectManager.add_parser_remover_arguments(remover_parser)
		ProjectManager.add_parser_info_arguments(info_parser)
		return p_parser

	##actions
	def parse_lister_actions(self,args):
		self.show_projects(args.use_colors,args.filter_groups)

	def parse_opener_actions(self,args):
		if args.code or args.terminal or args.explorer:
			self.try_open(args.project,args.code,args.terminal,args.explorer)

	def parse_info_actions(self,args):
		self.show_info(args.info_project,args.info_name,args.info_path,args.info_description,args.info_groups)

	def parse_editor_actions(self,args):
		__error = False
		__need_save = False

		if len(args.add_groups) != 0:
			for __projects,__groups in zip(args.projects, args.add_groups):
				for proj in __projects: __need_save |= self.add_groups(proj,__groups)>0

		if len(args.remove_groups) != 0:
			for __projects,__groups in zip(args.projects, args.remove_groups):
				for proj in __projects: __need_save |= self.remove_groups(proj,__groups)>0

		
		if len(args.rename_projects) != 0:
			for __projects, __renames in zip(args.projects, args.rename_projects):
				if len(__projects) != len(__renames):
					ut.cerr("The amount of projects renamed is different from the amount of names")
					__error = True
				for proj,new_name in zip(__projects,__renames): __need_save |= self.rename_project(proj,new_name)

		if len(args.power_rename_projects) != 0:
			ut.warn("power renaming is not an official feature yet!")
			# for action in zip(args.projects, args.power_rename_projects):
			

		if __error:
			ut.cerr("An error has ocurred during editing therefore all the editing is invalid!")
			exit(1)
		elif __need_save: self.update_projects_file()

	def parse_adder_actions(self,args):
		config = {"name":args.project_name,"path":args.project_path,"groups":args.projects_groups }
		if args.project_description is not None: config["description"] = args.project_description
		p_data = self.new_project(config,True)
		self.update_projects_file()
		print(f"added new project to management: {p_data.name}")

	def parse_remover_actions(self,args):
		for p_name in args.project_names:
			p_data = self.delete_project(p_name)
			#TODO: check if needs to delete the project, or just forget
			if p_data is not None:
				self.update_projects_file()
				print(f"removed project from management: {p_data.name}")
			else:
				ut.cerr(f"No project named `{p_name}` was found!")
				exit(1)
	
	def parse_actions(self,args):
		match args._project_action:
			case "open": self.parse_opener_actions(args)
			case "edit": self.parse_editor_actions(args)
			case "list": self.parse_lister_actions(args)
			case "add": self.parse_adder_actions(args)
			case "remove": self.parse_remover_actions(args)
			case "info": self.parse_info_actions(args)
			case None:ut.cerr("No project option was provided!")

	##end argparse functions