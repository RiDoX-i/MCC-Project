from Code.turing_machine import configuration_initiale, executer_un_pas, lire_machine_tms, simuler

# garder le code et ajouter du code pour executer la question faite

if __name__ == "__main__":
    
    machine = lire_machine_tms("test/q2.tms")

    # ------------------- Q3 -------------------
    config = configuration_initiale(machine, "0")
    fait = executer_un_pas(machine, config)
    print("Q3 :")
    print(f"pas_execute={fait}")
    print(config)

    # ------------------- Q4 -------------------
    config_finale = simuler(machine, "0")
    print("\nQ4 :")
    print("Etat final :", config_finale.etat)
    print("Ruban :", config_finale.rubans)
    print("Têtes :", config_finale.tetes)