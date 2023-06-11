import os
from time import sleep

def show_menu():
    print("Benvenuto nel programma di gestione del database HR")
    print("Seleziona la tabella su cui effettuare operazioni:")
    print("[1] countries")
    print("[2] departments")
    print("[3] employees")
    print("[4] jobs")
    print("[5] locations")
    print("[0] Esci")

def execute_file(file_name):
    try:
        exec(open(file_name).read())
    except FileNotFoundError:
        print("File non trovato.")
    except Exception as e:
        print("Si è verificato un errore durante l'esecuzione del file:", e)

def main():
    while True:
        show_menu()
        choice = input("Seleziona un'opzione: ")

        if choice == "1":
            execute_file("Query/countries.py")
        elif choice == "2":
            execute_file("Query/departments.py")
        elif choice == "3":
            execute_file("Query/employees.py")
        elif choice == "4":
            execute_file("Query/jobs.py")
        elif choice == "5":
            execute_file("Query/locations.py")
        elif choice == "0":
            print("Arrivederci!")
            break
        else:
            print('Selezione non valida, riprova\n')
            sleep(0.5)

if __name__ == "__main__":
    main()