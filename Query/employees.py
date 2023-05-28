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
    print('\nTabella employees')
    ans=True
    while ans:
        print ('Seleziona operazione da eseguire:')
        print ('[1] Select')
        print ('[2] Insert')
        print ('[3] Persone a carico')
        print ('[4] Update')
        print ('[0] Esci')
        ans=input('Input: ')

        if ans=="1": 
            #Select Query
            employee = input('Inserisci il nome o cognome del dipendente da cercare: ')
            tsql =  "SELECT e.employee_id, e.first_name, e.last_name, e.email, e.phone_number, " +\
                    "e.hire_date, j.job_title, e.salary, e.manager_id, d.department_name " +\
                    "FROM employees AS e, jobs AS j,departments AS d " +\
                    "WHERE e.job_id = j.job_id AND e.department_id = d.department_id " +\
                    "AND (e.first_name LIKE ? OR e.last_name LIKE ?);"
            try:
                with cursor.execute(tsql,'%'+employee+'%', '%'+employee+'%'):
                    print('\nemployee_id | first_name, last_name | email | phone_number | hire_date | job_title | salary | manager_id | department_name')
                    row = cursor.fetchone()
                    while row:
                        print (str(row[0]) + " | " + str(row[1]) + ", " + str(row[2]) + " | " + str(row[3]) + " | " + 
                               str(row[4]) + " | " + str(row[5]) + " | " + str(row[6]) + " | " +
                               str(row[7]) + " | " + str(row[8]) + " | " + str(row[9]))
                        row = cursor.fetchone()
                        sleep(0.2)
            except pyodbc.Error as ex:
                print(ex.args[1])
            print('-----------------------------------------------------------------------------------------------------------------------------------')       
            
        elif ans=="2":
            #Insert Query
            print ('Inserisci un nuovo record')
            first_name = input('Inserisci il first_name [varchar(20)]: ')
            last_name = input('Inserisci il last_name [varchar(25)]: ')
            email = input('Inserisci l\'email [varchar(100)]: ')
            phone_number = input('Inserisci il phone_number [varchar(20)]: ')
            hire_date = input('Inserisci  l\'hire_date [YYYY-MM-DD]: ')
            job_id = int(input('Inserisci il job_id [int]: '))
            salary = int(input('Inserisci il salary [int]: '))
            manager_id = int(input('Inserisci il manager_id [int]: '))
            department_id = int(input('Inserisci il department_id [int]: '))
            tsql = "INSERT INTO employees VALUES (?,?,?,?,?,?,?,?,?);"
            try:
                with cursor.execute(tsql,first_name,last_name,email,phone_number,hire_date,job_id,salary,manager_id,department_id):
                    print ('Record inserito correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
           
        elif ans=="3":
            #Dependencies Query
            employee_id = int(input('Inserisci l\'employee_id del record della quale vuoi vedere le persone a carico: '))
            tsql =  "SELECT dependents.first_name, dependents.last_name, dependents.relationship " +\
                    "FROM employees, dependents " +\
                    "WHERE employees.employee_id = dependents.employee_id AND employees.employee_id = ?;"
            try: 
                with cursor.execute(tsql,employee_id):
                    print()
                    row = cursor.fetchone()
                    while row:
                        print (str(row[0]) + ", " + str(row[1]) + " | " + str(row[2]))
                        row = cursor.fetchone()
                        sleep(0.2)
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('L\'employee_id inserito non ha nessuna persona a carico\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
            print('-----------------------------------------------------------------------------------')
                    
        elif ans=="4":
            #Update Query
            employee_id = int(input('Inserisci l\'employee_id del record da modificare: '))
            tsql = "SELECT * FROM employees WHERE employee_id = ?;"
            try: 
                with cursor.execute(tsql,employee_id):
                    row = cursor.fetchone()
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con l\'employee_id inserito\n')
                        else:
                            print('\nfirst_name, last_name | email | phone_number | hire_date')
                            print (str(row[1]) + ", " + str(row[2]) + " | " + str(row[3]) + " | " + str(row[4]) + " | " + str(row[5]))
                            sleep(0.2)
                            print('\nNuovi valori')
                            email = input('Inserisci l\'email [varchar(100)]: ')
                            phone_number = input('Inserisci il phone_number [varchar(20)]: ')
                            tsql = "UPDATE employees SET email = ?, phone_number = ? WHERE employee_id = ?;"
                            try:
                                with cursor.execute(tsql,email,phone_number,employee_id):
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