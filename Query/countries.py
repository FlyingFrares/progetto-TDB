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
    print('\nTabella countries')
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
            country = input('Inserisci nazione da cercare: ')
            tsql =  "SELECT c.country_id, c.country_name, r.region_name " +\
                    "FROM countries AS c, regions AS r " +\
                    "WHERE c.region_id = r.region_id AND c.country_name LIKE ?;"
            try:
                with cursor.execute(tsql,'%'+country+'%'):
                    print('\ncountry_id | country_name | region_id')
                    row = cursor.fetchone()
                    while row:
                        print (str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]))
                        row = cursor.fetchone()
                        sleep(0.2)
            except pyodbc.Error as ex:
                print(ex.args[1])
            print('-----------------------------------------')       
            
        elif ans=="2":
            #Insert Query
            print ('Inserisci un nuovo record')
            country_id = input('country_id [char(2)]: ')
            country_name = input('country_name: ')
            region_id = int(input('region_id [int 1..4]: '))
            tsql = "INSERT INTO countries VALUES (?,?,?);"
            try:
                with cursor.execute(tsql,country_id.upper(),country_name,region_id):
                    print ('Record inserito correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
           
        elif ans=="3":
            #Delete Query
            country_id = input('Inserisci il country_id [char(2)] da eliminare: ')
            tsql = "DELETE FROM countries WHERE country_id = ?;"
            try: 
                with cursor.execute(tsql,country_id.upper()):
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con country_id '+ country_id.upper() +'\n')
                        else:
                            print ('Record eliminato correttamente\n')
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