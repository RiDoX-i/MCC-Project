from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import machine_universelle_simulation


def test_q9_simulation_simple():
    config = machine_universelle_simulation(
        str(ROOT / "test" / "q2.tms"),
        "0"
    )

    assert config.etat == "F"