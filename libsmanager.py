import os
import colorama as cl

cl.init();



def list_libraries(workspace):
	#checks for WORKSPACE_FOLDER variable
	libs_folder = os.path.join(workspace, "libs")
	print(f"{cl.Style.DIM}{cl.Back.WHITE}{cl.Fore.BLACK}  Libraries located at {libs_folder}:  {cl.Style.RESET_ALL}")


def run(args):
	#checks for workspace variable
	workspace_folder =  os.environ.get("WORKSPACE_FOLDER") 
	
	if workspace_folder is not None:
		if args.list:
			list_libraries(workspace_folder)
	else:
		print("Workspace was not setted yet!")
