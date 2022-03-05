from src.data import ConfigData
from src.project import ProjectManager
import src.utils as ut

class Workspace:
	path:str
	projects_manager:ProjectManager
	templates_path:str


	config: ConfigData

	def __init__(self) -> None:
		self.path = ut.load_workspace()
		self.projects_manager = ProjectManager(ut.load_workspace_projects(self.path))


	def printInfo(self):
		print("Workspace:")
		print(f"current workspace folder: {self.path}")

	def parseAction(self,args):
		if args.subcommand is None:
			print("No arguments provided!")
			return

		match args.subcommand:
			case "proj":
				if args.info: self.projects_manager.show_info()
				if args.list: self.projects_manager.show_projects(True)

				if (args.open or args.terminal or args.explorer): self.projects_manager.try_open(args.project,args.open,args.terminal,args.explorer)
					

			case "gen":
				print("command gen")
				

if __name__=="__main__":
	current_workspace = Workspace()
	current_workspace.printInfo()
