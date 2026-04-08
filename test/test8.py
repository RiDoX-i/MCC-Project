from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import coder_machine_binaire


def test_question8_codage_binaire():
    code = coder_machine_binaire(str(ROOT / "test" / "q2.tms"))

    assert all(c in "01" for c in code)
    assert len(code) > 0