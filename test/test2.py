from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import BLANC, DROITE, configuration_initiale, lire_machine_tms


def test_question2_minimal(tmp_path):
    tms = tmp_path / "machine.tms"
    tms.write_text(
        "\n".join(
            [
                "name: q2-min",
                "init: I",
                "accept: F",
                "I,0,F,1,>",
                "I,_,F,_,-",
            ]
        ),
        encoding="utf-8",
    )

    m = lire_machine_tms(str(tms))
    assert m.k == 1
    assert m.etat_initial == "I"
    assert m.etat_final == "F"
    assert m.alphabet_entree == {"0"}
    assert m.transitions[("I", ("0",))] == ("F", ("1",), (DROITE,))

    c = configuration_initiale(m, "01")
    assert c.etat == "I"
    assert c.lire(0) == "0"
    c.deplacer(0, DROITE)
    assert c.lire(0) == "1"
    c.deplacer(0, DROITE)
    assert c.lire(0) == BLANC
