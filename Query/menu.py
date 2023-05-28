import os

def show_menu():
    print("Menu:")
    print("1. Esegui file 1")
    print("2. Esegui file 2")
    print("3. Esegui file 3")
    print("4. Esci")

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
            execute_file("file2.py")
        elif choice == "3":
            execute_file("file3.py")
        elif choice == "4":
            break
        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()