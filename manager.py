from ast import arg, parse
import os, sys
import argparse as agp
import pygit2

def initializeGit(init, repo, path=".", clone=False):

	#checks if the current path already has a git repository initialized
	if pygit2.discover_repository(path) is not None:

		return

	if init is None:
		for i in range(3):
			ichoice = input("do you want to initialize a git repo?[Y|n]")
			if ichoice in ['Y','y']: init=True;break;
			elif ichoice in ['N','n']: return;
	elif init == False: return

	#assuming you want to init ...
	while repo is None:
		repo_name = input("Pls enter the git url for the repository setup\nor just [enter] to skip setup and just init\n>:");
		#TODO have a default git profile to just initialize a new repo
		if repo_name.startswith("git@") or repo_name.startswith("https://"): repo = repo_name; break;
		else: print(f"Sorry, but {repo_name} is not a valid repository name, try again")
	#TODO initialize or clone git repo

	if clone == True:
		pygit2.clone_repository(repo, path)



if __name__=="__main__":
	parser = agp.ArgumentParser(sys.argv[0],
	description= "Window C/C++ project manager")


	#check version
	parser.add_argument('--version',action='version',version="win-cman 0.1")
	

	#git repository and initialization arguments
	parser.add_argument('--git', 
		help="skips asking for git repository initialization",
		action=agp.BooleanOptionalAction)
	parser.add_argument('--repo', 
		help="sets the git repository to be initialized",
		default=None)
	parser.add_argument('--git-clone', 
		help="change the behavior of repository initialization for cloning",
		action="store_true",default=False)


	#add libraries
	parser.add_argument('--use-lib',"--ul",
	type=str, nargs="+",
	help="adds a library to current project's dependencies",
	action='extend')

	args = parser.parse_args(sys.argv[1:])
	
	if(args.git != False): initializeGit(args.git, args.repo, clone = args.git_clone)
		

	print(vars(args))

	

