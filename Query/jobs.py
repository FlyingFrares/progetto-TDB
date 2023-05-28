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
    print('\nTabella jobs')
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
            job = input('Inserisci il job_title da cercare: ')
            tsql =  "SELECT job_id, job_title, min_salary, max_salary " +\
                    "FROM jobs " +\
                    "WHERE job_title LIKE ?;"  
            try:
                with cursor.execute(tsql,'%'+job+'%'):
                    print('\njob_id | job_title | min_salary | max_salary')
                    row = cursor.fetchone()
                    while row:
                        print (str(row[0]) + " | " + str(row[1]) + ", " + str(row[2]) + " | " + str(row[3]))
                        row = cursor.fetchone()
                        sleep(0.2)
            except pyodbc.Error as ex:
                print(ex.args[1])
            print('-------------------------------------------------------')       
            
        elif ans=="2":
            #Insert Query
            print ('Inserisci un nuovo record')
            job_title = input('Inserisci il job_title [varchar(35)]: ')
            min_salary = int(input('Inserisci il min_salary [int]: '))
            max_salary = int(input('Inserisci il max_salary [int]: '))
            tsql = "INSERT INTO jobs VALUES (?,?,?);"
            try:
                with cursor.execute(tsql,job_title,min_salary,max_salary):
                    print ('Record inserito correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
           
        elif ans=="3":
            #Delete Query
            job_id = int(input('Insserisci il job_id del record da eliminare: '))
            tsql = "DELETE FROM jobs WHERE job_id = ?;"
            try: 
                with cursor.execute(tsql,job_id):
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con il job_id inserito\n')
                        else:
                            print ('Record eliminato correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
                    
        elif ans=="4":
            #Update Query
            job_id = int(input('Inserisci il job_id del record da aggiornare: '))
            tsql = "SELECT * FROM jobs WHERE job_id = ?;"
            try: 
                with cursor.execute(tsql,job_id):
                    row = cursor.fetchone()
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con il job_id inserito\n')
                        else:
                            print('\njob_title | min_salary | max_salary')
                            print (str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]))
                            sleep(0.2)
                            print('\nAggiorna salari')
                            min_salary = int(input('Inserisci il min_salary [int]: '))
                            max_salary = int(input('Inserisci il max_salary [int]: '))
                            tsql = "UPDATE jobs SET min_salary = ?, max_salary = ? WHERE job_id = ?;"
                            try:
                                with cursor.execute(tsql,min_salary,max_salary,job_id):
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