import os
from pathlib import Path
import sys

if os.environ.get("TESTS_IMPORT_LOCAL"):
    p = Path(__file__).parent.parent
    sys.path[0:0] = str(p / "src"), str(p / "extra/fake_rpds/src")
