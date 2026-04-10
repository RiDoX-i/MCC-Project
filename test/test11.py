from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import decide_L1


def test_L1_vrai():
    result = decide_L1(str(ROOT / "test" / "q11.tms"), 2)
    assert result is True


def test_L1_faux():
    result = decide_L1(str(ROOT / "test" / "q11.tms"), 1)
    assert result is False