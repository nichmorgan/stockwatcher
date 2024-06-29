import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parents[1]
sys.path.append((ROOT_DIR / "src").absolute().as_posix())
