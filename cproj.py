import argparse as agp
from src.project import ProjectManager
import workspace as wp
import sys 

#small project opener
if __name__=="__main__":
	current_workspace = wp.Workspace()
	main_parser = agp.ArgumentParser(sys.argv[0], description= "Window C/C++ project manager (opener)")
	wp.Workspace.add_parser_version_arguments(main_parser)
	ProjectManager.add_parser_arguments(main_parser)
	args = main_parser.parse_args(sys.argv[1:])
	current_workspace.projects_manager.parse_actions(args)

