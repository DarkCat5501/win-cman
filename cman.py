import argparse as agp
from email.policy import default
import workspace as wp
import sys 

if __name__=="__main__":
	current_workspace = wp.Workspace()

	main_parser = agp.ArgumentParser(sys.argv[0],
	description= "Window C/C++ project manager")
	######## main arguments
	main_parser.add_argument('--version',action='version',version=f"win-cman 0.1")
	main_parser.add_argument("-info",default=False, action="store_true",help="acquire information about submodule")

	#separating parsers
	subparser = main_parser.add_subparsers(help="sub-commands help",dest="subcommand")
	library_parser = subparser.add_parser("lib",help="manage libraries and dependencies")
	project_parser = subparser.add_parser("proj",help="manage current project, it's libraries and dependencies")
	generator_parser = subparser.add_parser("gen",help="Project generator")

	##project generation START
	generator_parser.add_argument("name", type=str, default="project")
	#git options
	git_parser = generator_parser.add_argument_group("git")
	git_parser.add_argument('--git', 
		help="skips asking for git repository initialization",
		action=agp.BooleanOptionalAction)
	git_parser.add_argument("-git-repo", 
		help="sets the git repository to be initialized",
		default=None)
	git_parser.add_argument("-git-clone", 
		help="change the behavior of repository initialization for cloning",
		action="store_true",default=False)	
	#make option
	make_parser = generator_parser.add_argument_group("make")
	make_parser.add_argument("--make",
		help="skips asking for makefile generation",
		action =agp.BooleanOptionalAction)
	make_parser.add_argument("--make-sub",
		help="skips asking for makefile generation",
		action="store_true",default=False)
	##project generation END

	##libraries management START
	library_parser.add_argument("--list","-ls",help="List all libraries installed",action="store_true",default=False)

	# parser.add_argument('--use-lib',"--ul",
	# type=str, nargs="+",
	# help="adds a library to current project's dependencies",
	# action='extend')

	##libraries management END

	##projects manager START

	project_action_parser = project_parser.add_subparsers(help="project actions",dest="project_cmd")
	library_parser = project_action_parser.add_parser("list",help="list all projects")

	projects_open_options = project_action_parser.add_parser("open",help="opens a specified project")
	projects_open_options.add_argument("project",help="The name of the project to be open",action="store")
	projects_open_options.add_argument("--code","-c",help="Open a specific project in default editor",action="store_true",default=False)
	projects_open_options.add_argument("--terminal","-t",help="Open the project in a terminal",action="store_true",default=False)
	projects_open_options.add_argument("--explorer","-e",help="Open the project folder in explorer",action="store_true",default=False)	

	projects_open_options = project_action_parser.add_parser("add",help="adds a new project directly to projects list")
	projects_open_options.add_argument("project_name",help="The name for the project to be added",action="store")
	projects_open_options.add_argument("project_path",help="The path to the project to be added",action="store")
	projects_open_options.add_argument("-d",help="Description for the project",action="store",default=None, dest="project_description")


	projects_open_options = project_action_parser.add_parser("remove",help="removes a project from management")
	projects_open_options.add_argument("project_names",help="Project to be removed from management",nargs="+",action="extend")

	##projects manager END

	##run actions
	args = main_parser.parse_args(sys.argv[1:])
	if not args.subcommand:
		current_workspace.printInfo()
	# print(vars(args)) DEBUG
	current_workspace.parseAction(args)

