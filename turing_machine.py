from dataclasses import dataclass, field
from typing import Dict, Tuple, List

BLANC = "."   # représente □
GAUCHE = "L"
DROITE = "R"
IMMOBILE = "S"


@dataclass
class MT:
    # nombre de rubans
    k: int

    # ensemble des états (optionnel pour la simulation, mais utile pour valider)
    etats: set

    # alphabets
    alphabet_entree: set
    alphabet_travail: set

    # état initial et état final
    etat_initial: str = "I"
    etat_final: str = "F"

    # transitions :
    # clé    = (etat_courant, (symbole_lu_ruban1, ..., symbole_lu_rubank))
    # valeur = (nouvel_etat, (symbole_ecrit_ruban1, ..., symbole_ecrit_rubank),
    #                         (deplacement1, ..., deplacementk))
    transitions: Dict[
        Tuple[str, Tuple[str, ...]],
        Tuple[str, Tuple[str, ...], Tuple[str, ...]]
    ] = field(default_factory=dict)


#--------------------------------------------------------- Question 2 ---------------------------------------------------------
# initialise une instance de MT à partir d'un fichier au format turingmachinesimulator.com
# crée ensuite la configuration initiale à partir du mot d'entrée et de la machine
# Syntaxe attendue : name, init, accept, puis delta en deux lignes ou une ligne.
def lire_machine_tms(path: str) -> MT:
    with open(path, encoding="utf-8") as f:
        lignes = [l.strip() for l in f if l.strip() and not l.strip().startswith("//")]
    init = None
    accept = set()
    transitions = {}
    etats = set()
    alphabet_entree = set()
    alphabet_travail = {BLANC}
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        if ligne.startswith("name:"):
            i += 1
            continue
        if ligne.startswith("init:"):
            init = ligne.split(":", 1)[1].strip()
            etats.add(init)
            i += 1
            continue
        if ligne.startswith("accept:"):
            accept = {s.strip() for s in ligne.split(":", 1)[1].split(",") if s.strip()}
            etats.update(accept)
            i += 1
            continue
        parts = [p.strip() for p in ligne.split(",")]
        if len(parts) == 2:
            etat, lecture = parts
            if i + 1 >= len(lignes):
                raise ValueError("Format TMS invalide : transition incomplète")
            etat2, ecriture, mouv = [p.strip() for p in lignes[i + 1].split(",")]
            i += 2
        elif len(parts) == 5:
            etat, lecture, etat2, ecriture, mouv = parts
            i += 1
        else:
            raise ValueError(f"Ligne TMS invalide : {ligne}")
        lecture = BLANC if lecture == "_" else lecture
        ecriture = BLANC if ecriture == "_" else ecriture
        if mouv == ">":
            dep = DROITE
        elif mouv == "<":
            dep = GAUCHE
        elif mouv == "-":
            dep = IMMOBILE
        else:
            raise ValueError(f"Mouvement invalide : {mouv}")
        transitions[(etat, (lecture,))] = (etat2, (ecriture,), (dep,))
        etats.update({etat, etat2})
        alphabet_entree.add(lecture)
        alphabet_travail.update({lecture, ecriture})
    if init is None:
        raise ValueError("Fichier TMS sans init")
    if not accept:
        raise ValueError("Fichier TMS sans accept")
    return MT(
        1,
        etats,
        alphabet_entree,
        alphabet_travail,
        etat_initial=init,
        etat_final=next(iter(accept)),
        transitions=transitions,
    )

# fonction de création de la configuration initiale à partir du mot d'entrée et de la machine.
def configuration_initiale(machine: MT, mot: str) -> Configuration:
    return Configuration(machine.etat_initial, [{i: c for i, c in enumerate(mot)}], [0])
#------------------------------------------------------------------------------------------------------------------------------



@dataclass
class Configuration:
    # état courant
    etat: str

    # un ruban = dictionnaire position -> symbole
    # on utilise une représentation creuse pour simuler un ruban infini
    rubans: List[Dict[int, str]]

    # position de la tête sur chaque ruban
    tetes: List[int]

    def lire(self, i: int) -> str:
        return self.rubans[i].get(self.tetes[i], BLANC)

    def ecrire(self, i: int, symbole: str) -> None:
        if symbole == BLANC:
            self.rubans[i].pop(self.tetes[i], None)
        else:
            self.rubans[i][self.tetes[i]] = symbole

    def deplacer(self, i: int, mouvement: str) -> None:
        if mouvement == DROITE:
            self.tetes[i] += 1
        elif mouvement == GAUCHE:
            self.tetes[i] -= 1
        elif mouvement == IMMOBILE:
            pass
        else:
            raise ValueError(f"Mouvement invalide : {mouvement}")