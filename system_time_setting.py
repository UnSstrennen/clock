from win32api import SetSystemTime
from os import path
from sys import argv, executable
from sys import exit as sysexit
import win32com.shell.shell as shell


DEBUG = False

ASADMIN = 'asadmin'
if argv[-1] != ASADMIN:
    script = path.abspath(argv[0])
    params = ' '.join([script] + argv[1:] + [ASADMIN])
    shell.ShellExecuteEx(lpVerb='runas', lpFile=executable, lpParameters=params)
    sysexit(0)
with open('time.txt', 'r') as file:
    t = file.readline()
t = t.split()
t = list(map(lambda n: int(n.rstrip(',')), t))
if DEBUG:
    t = str(t)
    my_file = open("some.txt", "w")
    my_file.write(t)
    my_file.close()
SetSystemTime(t[0], t[1], t[6], t[2], t[3], t[4], t[5], 0)