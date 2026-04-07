from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import (
    machine_comparaison,
    machine_recherche,
    machine_multiplication_unaire,
    simuler_borne,
)


# ================= TEST COMPARAISON =================

def test_comparaison_arret():
    m = machine_comparaison()
    config = simuler_borne(m, "0#1")

    assert config.etat == "F"


def test_comparaison_boucle():
    m = machine_comparaison()
    config = simuler_borne(m, "1#0", max_pas=50)

    assert config.etat != "F"


# ================= TEST RECHERCHE =================

def test_recherche_trouve():
    m = machine_recherche()
    config = simuler_borne(m, "1#1#0")

    assert config.etat == "F"


def test_recherche_pas_trouve():
    m = machine_recherche()
    config = simuler_borne(m, "1#0#0", max_pas=50)

    assert config.etat != "F"


# ================= TEST MULTIPLICATION =================

def test_multiplication_unaire():
    m = machine_multiplication_unaire()
    config = simuler_borne(m, "11#11")

    assert config.etat == "F"