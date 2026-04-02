from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import configuration_initiale, executer_un_pas, lire_machine_tms


def test_question3_un_pas():
    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))
    config = configuration_initiale(machine, "0")

    fait = executer_un_pas(machine, config)

    assert fait is True
    assert config.etat == "F"
    assert config.tetes[0] == 1
    assert config.rubans[0].get(0) == "1"


def test_question3_pas_impossible():
    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))
    config = configuration_initiale(machine, "1")

    fait = executer_un_pas(machine, config)

    assert fait is False
    assert config.etat == "I"
