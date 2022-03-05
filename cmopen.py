import argparse as agp
import workspace as wp
import sys 

#small project opener
if __name__=="__main__":
	current_workspace = wp.Workspace()
	main_parser = agp.ArgumentParser(sys.argv[0],
	description= "Window C/C++ project manager (opener)")
	main_parser.add_argument('--version',action='version',version=f"win-cman 0.1")
	main_parser.add_argument("project",help="The name of the project to be open",action="store")
	main_parser.add_argument("--code","-c",help="Open a specific project in default editor",action="store_true",default=False)
	main_parser.add_argument("--terminal","-t",help="Open the project in a terminal",action="store_true",default=False)
	main_parser.add_argument("--explorer","-e",help="Open the project folder in explorer",action="store_true",default=False)	
	args = main_parser.parse_args(sys.argv[1:])
	current_workspace.parseProjectOpen(args)

