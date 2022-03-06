from dataclasses import asdict, dataclass, field
import os
from . import utils as ut
from beautifultable import BeautifulTable as Table
import colorama as cl
import argparse as agp

@dataclass
class BaseProjectConfig:
	name:str
	path: str			= field(default=".")
	description: str	= field(default=" * No description * ")



@dataclass
class ProjectManager:
	path: str;
	projects:dict = field(default_factory=dict);

	def __post_init__(self):
		projects_data = ut.load_json_data(self.path);

		for proj in projects_data:
			self.new_project(proj)

	def update_projects_file(self):
		if not ut.save_json_data(self.path, [ asdict(proj) for name, proj in self.projects.items() ]):
			ut.cerr("Projects were not updated!")

	def new_project(self, config:dict,check_path=False):
		if check_path and not os.path.isdir( config["path"] ):
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

	def delete_project(self, name):
		if name in self.projects:
			tmp = self.projects[name]
			del self.projects[name]
			return tmp
		return None

	def list_project_names(self) -> list[str]:
		return list(self.projects.keys())

	def list_project(self,use_colors = False ):
		for pname,proj in self.projects.items():
			if use_colors:
				yield ("",f"{cl.Fore.GREEN}{pname}{cl.Fore.RESET}",f"{cl.Fore.CYAN}{proj.description}{cl.Fore.RESET}")
			else :
				yield ("",pname, proj.description)

	def show_projects(self, use_colors = False):	
		tabele = Table(maxwidth=100)
		tabele.set_style(Table.STYLE_BOX)
		tabele.columns.header = ("***","name","description") if not use_colors else ("***",f"{cl.Fore.GREEN}name{cl.Fore.RESET}",f"{cl.Fore.CYAN}description{cl.Fore.RESET}")
		tabele.columns.width = 70;tabele.columns.width[0] = 5;tabele.columns.width[1] = 20
		tabele.columns.alignment = Table.ALIGN_LEFT
		for line in tabele.stream(self.list_project(use_colors)):
			print(line)

	def show_info(self):
		print(f"Current projects list folder: {self.path}")
		print(f" {len(self.projects.keys())} projects loaded")

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
		parser.add_argument('--color', help="enables colorization",action=agp.BooleanOptionalAction,default=False,required=False,dest="use_colors")
		
	@staticmethod
	def add_parser_opener_arguments(parser: agp.ArgumentParser):
		parser.add_argument("project",help="The name of the project to be open",action="store")
		parser.add_argument("--code","-c",help="Open a specific project in default editor",action=agp.BooleanOptionalAction,default=True)
		parser.add_argument("--terminal","-t",help="Open the project in a terminal",action=agp.BooleanOptionalAction,default=False)
		parser.add_argument("--explorer","-e",help="Open the project folder in explorer",action="store_true",default=False)

	@staticmethod
	def add_parser_adder_arguments(parser: agp.ArgumentParser):
		parser.add_argument("project_name",help="The name for the project to be added",action="store")
		parser.add_argument("project_path",help="The path to the project to be added",action="store")
		parser.add_argument("-d",help="Description for the project",action="store",default=None, dest="project_description")

	@staticmethod
	def add_parser_remover_arguments(parser: agp.ArgumentParser):
		parser.add_argument("project_names",help="Project to be removed from management",nargs="+",action="extend")

	@staticmethod
	def add_parser_arguments(parser:agp.ArgumentParser):
		p_parser = parser.add_subparsers(help="project actions",dest="_project_action")
		opener_parser = p_parser.add_parser("open",help="opens a specified project")
		lister_parser = p_parser.add_parser("list",help="list all projects")
		adder_parser = p_parser.add_parser("add",help="adds a new project directly to projects list")
		remover_parser = p_parser.add_parser("add",help="adds a new project directly to projects list")
		ProjectManager.add_parser_opener_arguments(opener_parser)
		ProjectManager.add_parser_lister_arguments(lister_parser)
		ProjectManager.add_parser_adder_arguments(adder_parser)
		ProjectManager.add_parser_remover_arguments(remover_parser)
		return p_parser

	##actions
	def parse_lister_actions(self,args):
		self.show_projects(args.use_colors)

	def parse_opener_actions(self,args):
		if args.code or args.terminal or args.explorer:
			self.try_open(args.project,args.code,args.terminal,args.explorer)

	def parse_adder_actions(self,args):
		config = {"name":args.project_name,"path":args.project_path}
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
			case "list": self.parse_lister_actions(args)
			case "add": self.parse_adder_actions(args)
			case "remove": self.parse_remover_actions(args)
			case None: ut.cerr("No project option was provided!")

	##end argparse functions