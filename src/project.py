from dataclasses import dataclass, field
import os
from . import utils as ut
from beautifultable import BeautifulTable as Table
import colorama as cl

@dataclass
class BaseProjectConfig:
	name:str
	path: str			= field(default=".")
	description: str	= field(default=" * No description * ")
	sources:list[str]	= field(default_factory=list)
	ignore: list[str]	= field(default_factory=list)



@dataclass
class ProjectManager:
	path: str;
	projects:dict = field(default_factory=dict);

	def __post_init__(self):
		projects_data = ut.load_json_data(self.path);

		for proj in projects_data:
			self.new_project(proj)

	def update_projects_file(self):
		if not ut.save_json_data(self.path, self.projects):
			ut.cerr("Projects were not updated!")

	def new_project(self, config):
		_project = ut.create_from("Project",BaseProjectConfig,config,[])
		_name = _project.name;
		_tries = 1
		while _name in self.projects:
			_name = _project.name + f"-{_tries}"
		if _name != _project.name:
			ut.warn(f"Trying to load similar named projects: Renamed to {_name}")
		self.projects[_name] = _project

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
		tabele.set_style(Table.STYLE_COMPACT)
		tabele.columns.header = ("***","name","description") if not use_colors else ("***",f"{cl.Fore.GREEN}name{cl.Fore.RESET}",f"{cl.Fore.CYAN}description{cl.Fore.RESET}")
		tabele.columns.width = 70;tabele.columns.width[0] = 5;tabele.columns.width[1] = 20
		tabele.columns.alignment = Table.ALIGN_LEFT
		tabele.columns.separator = "\uE0B1" if not use_colors else f"{cl.Fore.GREEN}\uE0B1{cl.Fore.RESET}"
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
			


if __name__=="__main__":
	workspace = ut.load_workspace()
	#load projects
	projects_file = ut.load_workspace_projects(workspace)
	#generate manager
	projects_manager = ProjectManager(projects_file)
	projects_manager.show_projects()



