import os

print("Database HR")
print("Seleziona la tabella su cui operare:")
print ('[1] countires')
print ('[2] departments')
print ('[3] employees')
print ('[4] jobs')
print ('[0] Esci')
ans=input('Input: ')

if ans=="1":
    os.system('python Query\countries.py')