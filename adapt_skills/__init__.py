import os
import inspect
filename = inspect.stack()[0][1][:-11]
__all__ = list(set([os.path.splitext(f)[0] for f in os.listdir(filename) if f.endswith("Skill.py") or f.endswith("Skill.pyc")]))
