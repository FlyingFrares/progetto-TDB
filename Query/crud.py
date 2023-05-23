import pyodbc
server = 'localhost'
database = 'HR'
username = 'tbd'
password = 'TechBD'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
print ('Seleziona operazione da eseguire:')
print ('[1] Insert')
print ('[2] Update')
print ('[3] Select')
print ('[4] Delete')
operation = int(input())

if operation == 1:
    print ('Inserting a new row into table jobs')
    #Insert Query
    tsql = "INSERT INTO jobs (job_title, min_salary, max_salary) VALUES (?,?,?);"
    with cursor.execute(tsql,'Spennapolli','1000','10000'):
        print ('Successfully Inserted!')

elif operation == 2:
    #Update Query
    print ('Updating phone number for William')
    tsql = "UPDATE employees SET phone_number = ? WHERE first_name = ?"
    with cursor.execute(tsql,'111222333444','William'):
        print ('Successfully Updated!')

elif operation == 3:
    #Select Query
    print ('Reading data from table locations')
    tsql = "SELECT * FROM locations;"
    with cursor.execute(tsql):
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()

elif operation == 4:
    #Delete Query
    print ('Deleting Spennapolli')
    tsql = "DELETE FROM jobs WHERE job_title = ?"
    with cursor.execute(tsql,'Spennapolli'):
        print ('Successfully Deleted!')

else:
    print('Adios')