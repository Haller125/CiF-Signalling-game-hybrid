import sys
from pathlib import Path

# add repository root to sys.path so `src` can be imported
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
