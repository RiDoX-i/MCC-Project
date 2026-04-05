from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import BLANC, DROITE, MT, Configuration

def test_question1_minimal():
    m = MT(1, {"I", "F"}, {"0", "1"}, {"0", "1", BLANC})
    assert m.k == 1
    assert m.etat_initial == "I"
    assert m.etat_final == "F"

    c = Configuration("I", [{0: "1"}], [0])
    assert c.lire(0) == "1"

    c.ecrire(0, "0")
    assert c.lire(0) == "0"

    c.deplacer(0, DROITE)
    assert c.lire(0) == BLANC