from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import lire_machine_tms, simuler_avec_affichage


def test_question5_affichage(capsys):
    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))
    
    simuler_avec_affichage(machine, "0")

    captured = capsys.readouterr()

    assert "Etat" in captured.out
    assert "Ruban" in captured.out
    assert "Têtes" in captured.out
def test_simple():
    assert True