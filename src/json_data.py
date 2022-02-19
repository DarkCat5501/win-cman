import os
import json
from dataclasses import dataclass,field


@dataclass()
class ConfigData:
    version: str  = field()
