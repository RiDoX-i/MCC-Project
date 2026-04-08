from Code.turing_machine import configuration_initiale, executer_un_pas, lire_machine_tms

# garder le code et ajouter du code pour executer la question faite

if __name__ == "__main__":
    
    machine = lire_machine_tms("test/q2.tms")
    config = configuration_initiale(machine, "0")
    fait = executer_un_pas(machine, config)
    print(f"pas_execute={fait}")
    print(config)
