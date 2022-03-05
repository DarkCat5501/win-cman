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

	def parseProjectAction(self,args):
		
		match args.project_cmd:
			case None:
				print("getting information about current")
			
			case "list": self.projects_manager.show_projects(True)
			case "open":
				if args.code or args.terminal or args.explorer:
					self.projects_manager.try_open(args.project,args.code,args.terminal,args.explorer)

			case "add":
				config = {"name":args.project_name,"path":args.project_path}
				if args.project_description is not None: config["description"] = args.project_description
				p_data = self.projects_manager.new_project(config)
				self.projects_manager.update_projects_file()
				print(f"added new project to management: {p_data.name}")
			
			case "remove":
				for p_name in args.project_names:
					p_data = self.projects_manager.delete_project(p_name)
					#TODO: check if needs to delete the project, or just forget
					if p_data is not None:
						self.projects_manager.update_projects_file()
						print(f"removed project from management: {p_data.name}")
					else:
						ut.cerr(f"No project named `{p_name}` was found!")
						exit(1)

		pass

	def parseAction(self,args):
		if args.subcommand is None:
			print("No arguments provided!")
			return

		match args.subcommand:
			case "proj":
				self.parseProjectAction(args)
				pass
			case "gen":
				print("command gen")
				

if __name__=="__main__":
	current_workspace = Workspace()
	current_workspace.printInfo()
