import sys
from pathlib import Path

# Add this project's root to the PATH, to be able to do from utils.xxx import xxx
sys.path.append(str(Path(__file__).resolve().parent.parent))
