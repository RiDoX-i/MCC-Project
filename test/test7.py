from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import coder_machine_q7

def test_question7_minimal():
    chemin_tms = Path(__file__).resolve().parent / "q7.tms"
    resultat = coder_machine_q7(str(chemin_tms))
    attendu = "0|0|1|>|1|0|□|□|-|1"
    assert resultat == attendu