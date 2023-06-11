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
        print("Connessione per " + username + " fallita\n")
        sleep(0.5)
else:
    print('\n')
    print(' -------------------')
    print('| Tabella locations |')
    print(' -------------------')
    ans=True
    while ans:
        print ('Seleziona operazione da eseguire:')
        print ('[1] Select')
        print ('[2] Insert')
        print ('[3] Delete')
        print ('[4] Update')
        print ('[0] Torna al menu principale')
        ans=input('Input: ')

        if ans=="1": 
            #Select Query
            location = input('Inserisci la nazione da cercare: ')
            tsql =  "SELECT l.location_id, l.street_address, l.postal_code, l.city, l.state_province, c.country_name, r.region_name " +\
                    "FROM locations AS l JOIN countries AS c ON l.country_id = c.country_id " +\
                    "JOIN regions AS r ON c.region_id = r.region_id " +\
                    "WHERE c.country_name LIKE ?;"
            try:
                with cursor.execute(tsql,'%'+location+'%'):
                    print('\nlocation_id | street_address, postal_code, city, state_province, country_name, region_name')
                    row = cursor.fetchone()
                    while row:
                        print (str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " +
                               str(row[3]) + ", " + str(row[4]) + ", " + str(row[5]) + ", " + str(row[6]))
                        row = cursor.fetchone()
                        sleep(0.2)
            except pyodbc.Error as ex:
                print(ex.args[1])
            print('---------------------------------------------------------------------------------------------------')       
            
        elif ans=="2":
            #Insert Query
            print ('Inserisci un nuovo record')
            street_address = input('Inserisci lo street_address [varchar(40)]: ')
            postal_code = input('Inserisci il postal_code [varchar(12)]: ')
            city = input('Inserisci la città [varchar(30)]: ')
            state_province = input('Inserisci lo state_province [varchar(25)]: ')
            country_id = input('Inserisci il country_id [varchar(2)]: ')
            tsql = "INSERT INTO locations VALUES (?,?,?,?,?);"
            try:
                with cursor.execute(tsql,street_address,postal_code,city,state_province,country_id.upper()):
                    print ('Record inserito correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
           
        elif ans=="3":
            #Delete Query
            location_id = int(input('Insserisci la location_id del record da eliminare: '))
            tsql = "DELETE FROM locations WHERE location_id = ?;" 
            try: 
                with cursor.execute(tsql,location_id):
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con la location_id inserita\n')
                        else:
                            print ('Record eliminato correttamente\n')
            except pyodbc.Error as ex:
                print(ex.args[1])
                    
        elif ans=="4":
            #Update Query
            location_id = int(input('Inserisci la location_id del record da aggiornare: '))
            tsql = "SELECT * FROM locations WHERE location_id = ?;"
            try: 
                with cursor.execute(tsql,location_id):
                    row = cursor.fetchone()
                    with cursor.execute("select @@rowcount"):
                        rowcount = cursor.fetchall()[0][0]
                        if rowcount == 0: 
                            print('Nessun record presente con la location_id inserita\n')
                        else:
                            print('\nstreet_address, postal_code, city, state_province, country_id')
                            print ( str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " +
                                    str(row[4]) + ", " + str(row[5]))
                            sleep(0.2)
                            print('\nInserisci i nuovi valori')
                            street_address = input('Inserisci lo street_address [varchar(40)]: ')
                            postal_code = input('Inserisci il postal_code [varchar(12)]: ')
                            city = input('Inserisci la città [varchar(30)]: ')
                            state_province = input('Inserisci lo state_province [varchar(25)]: ')
                            country_id = input('Inserisci il country_id [varchar(2)]: ')
                            tsql =  "UPDATE locations SET street_address = ?, postal_code = ?, city = ?, " +\
                                    "state_province = ?, country_id = ? WHERE location_id = ?;"
                            try:
                                with cursor.execute(tsql,street_address,postal_code,city,state_province,country_id.upper(),location_id):
                                    print ('Record aggiornato correttamente\n')
                            except pyodbc.Error as ex:
                                print(ex.args[1])
            except pyodbc.Error as ex:
                print(ex.args[1])

        elif ans =="0":
            #Exit
            print('\nTornando al menu principale...')
            ans = None

        else:
            #Retry
            print('Selezione non valida, riprova\n')
        
        sleep(0.5)