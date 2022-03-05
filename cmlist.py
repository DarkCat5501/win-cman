import argparse as agp
from email.policy import default
from urllib import request
import workspace as wp
import sys 

#small project lister
if __name__=="__main__":
	current_workspace = wp.Workspace()
	main_parser = agp.ArgumentParser(sys.argv[0],
	description= "Window C/C++ project manager (project lister)")
	main_parser.add_argument('--version',action='version',version=f"win-cman 0.1")
	main_parser.add_argument('--color', help="enables colorization",action=agp.BooleanOptionalAction,default=False,required=False,dest="use_colors")
	args = main_parser.parse_args(sys.argv[1:])
	current_workspace.parseProjectLister(args)

