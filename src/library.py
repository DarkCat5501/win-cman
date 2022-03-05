import os
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

	_lib_name:str = field(init=False,repr=False)
	_lib_abs_path:str = field(init=False,repr=False)

	@staticmethod
	def load(path):
		config = ut.load_json_data(path)
		return Lib(**config)

	def __post_init__(self):
		self._lib_abs_path = os.path.abspath(self.path)
		#raise erros if path to lib is not found
		if not os.path.exists(self._lib_abs_path):
			ut.cerr(f"( Library {self.name} ) path {self.path} is not valid!")
			exit(1)
		#replace space for lib name
		self._lib_name = self.name.replace(' ','_')

	@property
	def abs_path(self):
		return self._lib_abs_path

	@property
	def esc_name(self):
		return self._lib_name
		
if __name__=="__main__":
	lib_teste = Lib.load("lib.json")
	