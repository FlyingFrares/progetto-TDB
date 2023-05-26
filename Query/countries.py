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
    print('Tabella countries')
    ans=True
    while ans:
        print ('Seleziona operazione da eseguire:')
        print ('[1] Select')
        print ('[2] Insert')
        print ('[3] Delete')
        print ('[0] Esci')
        ans=input('Input: ')

        if ans=="1": 
            #Select Query
            country = input('Inserisci nazione da cercare:')
            try:
                tsql = "SELECT * FROM countries WHERE country_name LIKE ?;"
                cursor.execute(tsql,'%'+country+'%')
                row = cursor.fetchone()
                while row:
                    print (str(row[0]) + "  " + str(row[1]) + "  " + str(row[2]))
                    row = cursor.fetchone()
                    sleep(0.2)
            except pyodbc.Error as ex:
                print(ex.args[1])
            print()
            sleep(1)
            
        elif ans=="2":
            #Insert Query
            print ('Inserisci un nuovo record')
            country_id = input('country_id [char(2)]: ')
            country_name = input('country_name: ')
            region_id = int(input('region_id [int 1..4]: '))
            try:
                tsql = "INSERT INTO countries VALUES (?,?,?);"
                cursor.execute(tsql,country_id.upper(),country_name,region_id)
                print ('Record inserito correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
            sleep(0.5)
           
        elif ans=="3":
            #Delete Query
            country_id = input('Inserisci il country_id [char(2)] da eliminare: ')
            try:
                tsql = "DELETE FROM countries WHERE country_id = ?;"
                cursor.execute(tsql,country_id)
                cursor.execute("select @@rowcount")
                rowcount = cursor.fetchall()[0][0]
                if rowcount == 0: 
                    print('Nessun record presente con country id '+ country_id +'\n')
                else:
                    print ('Record eliminato\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
            sleep(0.5)

        elif ans =="0":
            print("Adios\n")
            sleep(0.5) 
            ans = None

        else:
            print("Selezione non valida\n")
            sleep(0.5)