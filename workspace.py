
import colorama as cl
import os

cl.init()

class Workspace:
	def __init__(self,path) -> None:
		self.path = path
		if not self.checkValidity(): exit(1)
		pass
	
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

	def valid(self):
		if self.path is None: return False
		return os.path.exists(self.path)
	

	def setWorkspace(self, path):
		os.putenv("WORKSPACE_FOLDER",path)
		pass

	def printInfo(self):
		print(f"current workspace folder: {self.path}")


if __name__=="__main__":
	current_workspace = Workspace(os.environ.get("WORKSPACE_FOLDER"))
	current_workspace.printInfo()
