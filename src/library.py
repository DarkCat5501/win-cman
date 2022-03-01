import os, sys

from gym import make
import utils as ut
from dataclasses import dataclass, field


@dataclass
class Lib:
	name:str
	path:str
	includes:list[str]		= field(default_factory=list)
	sources:list[str]		= field(default_factory=list)
	objects:list[str]		= field(default_factory=list)
	dependencies:list[str]	= field(default_factory=list)
	cflags:list[str]		= field(default_factory=list)
	lflags:list[str]		= field(default_factory=list)
	ignore:list[str]		= field(default_factory=list) #files or directories to be ignored

	lib_name:str = field(init=False,repr=False)
	lib_included_files:list[str] = field(init=False,repr=False, default_factory=list)
	lib_source_files:list[str] = field(init=False,repr=False, default_factory=list)


	@staticmethod
	def load(path):
		config = ut.load_json_data(path);
		return Lib(**config)

	def __post_init__(self):
		#replace space for lib name
		self.lib_name = self.name.replace(' ','_')
		#normalize paths for directories
		self.includes = [os.path.normpath(os.path.join(self.path, inc)) for inc in self.includes]
		self.sources = [os.path.normpath(os.path.join(self.path, src)) for src in self.sources]
		self.objects = [ os.path.normpath(os.path.join(self.path, obj)) for obj in self.objects]
		#find all files inside directories
		self.lib_included_files = self.find_includes()
		self.lib_source_files = self.find_sources()
	def find_includes(self):
		for include in self.includes:
			if not include in self.ignore:
				if not os.path.exists(include):
					ut.cerr(f"include directory \"{include}\" for library \"{self.name}\" was not found!")
					exit()
				for base,dirs,files in os.walk(include):
					base_abs = os.path.join(base)
					print(base_abs, files)
				#files = [os.path.join(include,file) for file in os.listdir(include) if os.path.isfile(os.path.join(include,file))]
				#print(files)

	def find_sources(self):
		for source in self.sources:
			if not source in self.ignore:
				if not os.path.exists(source):
					ut.cerr(f"source directory \"{source}\" for library \"{self.name}\" was not found!")
					exit()
				for base,dirs,files in os.walk(source):
					base_abs = os.path.join(base)
					print(base_abs, files)
				# files = [os.path.join(source,file) for file in os.listdir(source) if os.path.isfile(os.path.join(source,file))]
				# print(files)

	def find_cross_refs(self):
		pass



	def generate_make(self):
		make_out = f"INCLUDE := $(INCLUDE) { ' '.join(self.includes) }\n"\
		f"{self.lib_name} := {' '.join(self.sources)}\n"\
		f"dep_{self.lib_name}: {' '.join(self.sources)}\n"\
		f"\t$(CC) -c (files) -o (output.a) -flags -include"

		return make_out

if __name__=="__main__":
	lib_teste = Lib.load("lib.json")
	print(lib_teste)
	print(lib_teste.generate_make())
