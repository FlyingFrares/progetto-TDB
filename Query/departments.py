import pyodbc
from time import sleep

server = 'localhost'
database = 'HR'
username = 'tbd'
password = 'TechBD'
try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("Connessione per " + username + " fallita")
else:
    print('\nTabella departments')
    ans=True
    while ans:
        print ('Seleziona operazione da eseguire:')
        print ('[1] Select')
        print ('[2] Insert')
        print ('[3] Delete')
        print ('[4] Update')
        print ('[0] Esci')
        ans=input('Input: ')

        if ans=="1": 
            #Select Query
            department = input('Inserisci dipartimento da cercare: ')
            tsql =  "SELECT d.department_id, d.department_name,l.street_address, l.city " +\
                    "FROM departments AS d, locations AS l " +\
                    "WHERE d.location_id = l.location_id AND d.department_name LIKE ?;"
            try:
                with cursor.execute(tsql,'%'+department+'%'):
                    print('\ndepartment_id | department_name | street_address, city')
                    row = cursor.fetchone()
                    while row:
                        print (str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + ", " + str(row[3]))
                        row = cursor.fetchone()
                        sleep(0.2)
            except pyodbc.Error as ex:
                print(ex.args[1])
            print('-------------------------------------------------------------')       
            
        elif ans=="2":
            #Insert Query
            print ('Inserisci un nuovo record')
            department_name = input('Inserisci il department_name [varchar(30)]: ')
            location_id = int(input('Inserisci il location_id [int]: '))
            tsql = "INSERT INTO departments VALUES (?,?);"
            try:
                with cursor.execute(tsql,department_name,location_id):
                    print ('Record inserito correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
           
        elif ans=="3":
            #Delete Query
            department_id = int(input('Inserisci il department_id del record da eliminare: '))
            tsql = "DELETE FROM departments WHERE department_id = ?;"
            try: 
                with cursor.execute(tsql,department_id):
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con department_id = ' + str(department_id) + '\n')
                        else:
                            print ('Record eliminato correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
                
        elif ans=="4":
            #Update Query
            department_id = int(input('Inserisci il department_id del record da modificare: '))
            tsql = "SELECT * FROM departments WHERE department_id = ?;"
            try: 
                with cursor.execute(tsql,department_id):
                    row = cursor.fetchone()
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con department_id = ' + str(department_id) + '\n')
                        else:
                            print('\ndepartment_name | location_id')
                            print (str(row[1]) + " | " + str(row[2]))
                            sleep(0.2)
                            print('\nNuovi valori')
                            department_name = input('Inserisci il department_name [varchar(30)]: ')
                            location_id = int(input('Inserisci il location_id [int]: '))
                            tsql = "UPDATE departments SET department_name = ?, location_id = ? WHERE department_id = ?;"
                            try:
                                with cursor.execute(tsql,department_name,location_id,department_id):
                                    print ('Record aggiornato correttamente\n')
                            except pyodbc.Error as ex:
                                print(ex.args[1])
            except pyodbc.Error as ex:
                print(ex.args[1])

        elif ans =="0":
            #Exit
            print('Adios\n')
            ans = None

        else:
            #Retry
            print('Selezione non valida, riprova\n')
        
        sleep(0.5)