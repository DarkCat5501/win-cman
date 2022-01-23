
import os, sys
import argparse as agp
import generator
import libsmanager
import projmanager



if __name__=="__main__":

	
	main_parser = agp.ArgumentParser(sys.argv[0],
	description= "Window C/C++ project manager")
	######## main arguments
	main_parser.add_argument('--version',action='version',version="win-cman 0.1")

	subparser = main_parser.add_subparsers(help="sub-commands help",dest="subcommand")

	library_parser = subparser.add_parser("libs",help="manage libraries and dependencies")
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

	#library option

	#make option
	make_parser = generator_parser.add_argument_group("make")
	make_parser.add_argument("--make",
		help="skips asking for makefile generation",
		action =agp.BooleanOptionalAction)

	make_parser.add_argument("--make-sub",
		help="skips asking for makefile generation",
		action="store_true",default=False)

	make_parser.add_argument("--list","-ls",help="List all libraries installed",action="store_true",default=False)
	
	##project generation END

	##libraries management START
	
	library_parser.add_argument("--list","-ls",help="List all libraries installed",action="store_true",default=False)

	# parser.add_argument('--use-lib',"--ul",
	# type=str, nargs="+",
	# help="adds a library to current project's dependencies",
	# action='extend')

	##libraries management END



	args = main_parser.parse_args(sys.argv[1:])
	
	if args.subcommand == "gen" :
		#generator implementation
		generator.generate( args.name, args)
	elif args.subcommand == "libs" :
		#library manager implementation
		libsmanager.run(args)
	elif args.subcommand == "proj" :
		#project manager implemntation
		pass
	else:
		print("No arguments provided")