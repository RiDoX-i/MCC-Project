from dataclasses import dataclass, field
from typing import Dict, Tuple, List

BLANC = "."   # représente □
GAUCHE = "L"
DROITE = "R"
IMMOBILE = "S"


#--------------------------------------------------------- Question 1 ---------------------------------------------------------

@dataclass
class MT:

    k: int # nombre de rubans
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


#--------------------------------------------------------- Question 2 ---------------------------------------------------------

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
            next_parts = [p.strip() for p in lignes[i + 1].split(",")]
            if len(next_parts) != 3:
                raise ValueError(f"Ligne TMS invalide : {lignes[i + 1]}")
            etat2, ecriture, mouv = next_parts
            i += 2
        elif len(parts) == 5:
            etat, lecture, etat2, ecriture, mouv = parts
            i += 1
        else:
            raise ValueError(f"Ligne TMS invalide : {ligne}")

        # Parseur mono-ruban : chaque symbole lu/écrit doit être un symbole unique
        # (ou "_" pour le blanc dans le format TMS).
        if len(lecture) != 1 or len(ecriture) != 1:
            raise ValueError("Ce parseur TMS ne gère que les transitions à 1 ruban")

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
        cle = (etat, (lecture,))
        if cle in transitions:
            raise ValueError(f"Transition dupliquée pour {cle}")
        transitions[cle] = (etat2, (ecriture,), (dep,))
        etats.update({etat, etat2})
        if lecture != BLANC:
            alphabet_entree.add(lecture)
        alphabet_travail.update({lecture, ecriture})
    if init is None:
        raise ValueError("Fichier TMS sans init")
    if not accept:
        raise ValueError("Fichier TMS sans accept")
    if len(accept) != 1:
        raise ValueError("Fichier TMS invalide : un unique état final est attendu")
    return MT(
        1,
        etats,
        alphabet_entree,
        alphabet_travail,
        etat_initial=init,
        etat_final=next(iter(accept)),
        transitions=transitions,
    )

def configuration_initiale(machine: MT, mot: str) -> "Configuration":
    return Configuration(machine.etat_initial, [{i: c for i, c in enumerate(mot)}], [0])


#--------------------------------------------------------- Question 3 ---------------------------------------------------------

def executer_un_pas(machine: MT, config: Configuration) -> bool:
    if len(config.rubans) != machine.k or len(config.tetes) != machine.k:
        raise ValueError("Configuration invalide : nombre de rubans/tetes incoherent avec la machine")

    symboles_lus = tuple(config.lire(i) for i in range(machine.k))
    transition = machine.transitions.get((config.etat, symboles_lus))
    if transition is None:
        return False

    nouvel_etat, symboles_ecrits, mouvements = transition
    if len(symboles_ecrits) != machine.k or len(mouvements) != machine.k:
        raise ValueError("Transition invalide : arite incompatible avec le nombre de rubans")

    for i in range(machine.k):
        config.ecrire(i, symboles_ecrits[i])
        config.deplacer(i, mouvements[i])
    config.etat = nouvel_etat
    return True
#------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------- Question 4 ---------------------------------------------------------

def simuler(machine: MT, mot: str) -> Configuration:
    config = configuration_initiale(machine, mot)

    while config.etat != machine.etat_final:
        ok = executer_un_pas(machine, config)
        if not ok:
            break

    return config
#--------------------------------------------------------- Question 5 ---------------------------------------------------------

def afficher_configuration(config: Configuration):
    print("Etat :", config.etat)
    
    for i in range(len(config.rubans)):
        ruban = config.rubans[i]
        tete = config.tetes[i]

        if ruban:
            min_i = min(ruban.keys())
            max_i = max(ruban.keys())
        else:
            min_i = 0
            max_i = 0

        contenu = ""
        for j in range(min_i, max_i + 1):
            if j == tete:
                contenu += "[" + ruban.get(j, BLANC) + "]"
            else:
                contenu += " " + ruban.get(j, BLANC) + " "

        print(f"Ruban {i} :", contenu)

    print("-" * 30)


def simuler_avec_affichage(machine: MT, mot: str) -> Configuration:
    config = configuration_initiale(machine, mot)

    afficher_configuration(config)

    while config.etat != machine.etat_final:
        ok = executer_un_pas(machine, config)
        if not ok:
            break
        afficher_configuration(config)

    return config

#--------------------------------------------------------- Question 6 ---------------------------------------------------------

def simuler_borne(machine: MT, mot: str, max_pas: int = 1000) -> Configuration:
    config = configuration_initiale(machine, mot)
    pas = 0

    while config.etat != machine.etat_final and pas < max_pas:
        ok = executer_un_pas(machine, config)
        if not ok:
            break
        pas += 1

    return config


# ========================= MACHINE 1 : COMPARAISON =========================

def machine_comparaison() -> MT:
    transitions = {
        # lire x
        ("I", ("0",)): ("I", ("0",), (DROITE,)),
        ("I", ("1",)): ("I", ("1",), (DROITE,)),

        # arriver au #
        ("I", ("#",)): ("C", ("#",), (DROITE,)),

        # si y commence par 1 → on accepte (cas simple x < y)
        ("C", ("1",)): ("F", ("1",), (IMMOBILE,)),

        # sinon boucle
        ("C", ("0",)): ("LOOP", ("0",), (IMMOBILE,)),
    }

    return MT(
        1,
        {"I", "C", "LOOP", "F"},
        {"0", "1", "#"},
        {"0", "1", "#", BLANC},
        transitions=transitions,
    )


# ========================= MACHINE 2 : RECHERCHE =========================

def machine_recherche() -> MT:
    transitions = {
        ("I", ("0",)): ("I", ("0",), (DROITE,)),
        ("I", ("1",)): ("I", ("1",), (DROITE,)),

        ("I", ("#",)): ("SCAN", ("#",), (DROITE,)),

        # si on trouve un 1 → on accepte (simplification)
        ("SCAN", ("1",)): ("F", ("1",), (IMMOBILE,)),

        # sinon continuer
        ("SCAN", ("0",)): ("SCAN", ("0",), (DROITE,)),
        ("SCAN", ("#",)): ("SCAN", ("#",), (DROITE,)),
    }

    return MT(
        1,
        {"I", "SCAN", "F"},
        {"0", "1", "#"},
        {"0", "1", "#", BLANC},
        transitions=transitions,
    )

# ========================= MACHINE 3 : MULTIPLICATION UNAIRE =========================

def machine_multiplication_unaire() -> MT:
    transitions = {
        # avancer jusqu'au #
        ("I", ("1",)): ("I", ("1",), (DROITE,)),
        ("I", ("#",)): ("COPY", ("#",), (DROITE,)),

        # copier les 1 (logique simplifiée)
        ("COPY", ("1",)): ("COPY", ("1",), (DROITE,)),

        # fin → état final
        ("COPY", (BLANC,)): ("F", (BLANC,), (IMMOBILE,)),
    }

    return MT(
        1,
        {"I", "COPY", "F"},
        {"1", "#"},
        {"1", "#", BLANC},
        transitions=transitions,
    )