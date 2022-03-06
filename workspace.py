from src.data import ConfigData
from src.project import ProjectManager
import src.utils as ut
import argparse as agp

class Workspace:
	path:str
	projects_manager:ProjectManager
	templates_path:str
	config: ConfigData

	def __init__(self) -> None:
		self.path = ut.load_workspace()
		self.projects_manager = ProjectManager(ut.load_workspace_projects(self.path))
		self.config = ut.create_from("Configuration",ConfigData,ut.load_json_data(ut.load_workspace_config(self.path)))


	def printInfo(self):
		print("Workspace:")
		print(f"current workspace folder: {self.path}")

	## start argparse options ##

	@staticmethod
	def add_parser_version_arguments(parser: agp.ArgumentParser):
		parser.add_argument('--version',action='version',version=f"win-cman 0.1")

	@staticmethod
	def add_parser_arguments(parser: agp.ArgumentParser):
		Workspace.add_parser_version_arguments(parser)
		submodule = parser.add_subparsers(dest="submodule")
		#lib_parser = submodule.add_parser("lib",help="manage libraries and dependencies")
		prj_parser = submodule.add_parser("proj",help="manage current project, it's libraries and dependencies")
		#gen_parser = submodule.add_parser("gen",help="Project generator")
		ProjectManager.add_parser_arguments(prj_parser)

	def parse_arguments(self, args):
		if not args.submodule: self.printInfo();exit()
		match args.submodule:
			case "proj": self.projects_manager.parse_actions(args,self.config)

	## end argparse options ##

if __name__=="__main__":
	current_workspace = Workspace()
	current_workspace.printInfo()
