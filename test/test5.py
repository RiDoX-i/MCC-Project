from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Code.turing_machine import lire_machine_tms, configuration_initiale, afficher_configuration, simuler_avec_affichage


def test_question5_affichage_simple(capsys):
    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))
    config = configuration_initiale(machine, "0")

    afficher_configuration(config)

    captured = capsys.readouterr()
    output = captured.out

    assert "Etat" in output
    assert "Ruban" in output
    assert "0" in output


def test_question5_apres_un_pas(capsys):
    from Code.turing_machine import executer_un_pas

    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))
    config = configuration_initiale(machine, "0")

    executer_un_pas(machine, config)
    afficher_configuration(config)

    captured = capsys.readouterr()
    output = captured.out

    assert "F" in output
    assert "1" in output


def test_question5_simulation_complete(capsys):
    machine = lire_machine_tms(str(ROOT / "test" / "q2.tms"))

    simuler_avec_affichage(machine, "0")

    captured = capsys.readouterr()
    output = captured.out

    assert "I" in output
    assert "F" in output
def test_simple():
    assert True    