from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import lire_machine_tms, simuler


def test_question4_simulation_complete():
    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))
    
    config = simuler(machine, "0")

    assert config.etat == "F"
    assert config.tetes[0] == 1
    assert config.rubans[0].get(0) == "1"


def test_question4_blocage():
    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))
    
    config = simuler(machine, "1")

    assert config.etat == "I"