import os.path
from pathlib import Path

DATA_PATH = Path(os.path.dirname(__file__)).parent.parent / 'image'
if not DATA_PATH.exists():
    DATA_PATH = Path(os.path.dirname(__file__)).parent / 'image'
