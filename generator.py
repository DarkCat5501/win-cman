import os
import pygit2

#def generate(name, args):
# 	if(args.git != False): initializeGit(args.git, args.git_repo, clone = args.git_clone)
# 	project_path = os.getcwd()
# 	print(f"Project {name} generated at {project_path}")

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


def genMakeFile(project):
