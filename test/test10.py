from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import machine_universelle_bornee


def test_q10_arret_avant_limite():
    config = machine_universelle_bornee(
        str(ROOT / "test" / "q2.tms"),
        "0",
        10
    )

    assert config.etat == "F"


def test_q10_limite_pas():
    config = machine_universelle_bornee(
        str(ROOT / "test" / "q2.tms"),
        "0",
        0
    )

    assert config.etat != "F"