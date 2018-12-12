from ntplib import NTPClient
from time import ctime

def printservertime():
    """ prints the server time """
    c = NTPClient()
    response = c.request('pool.ntp.org')
    print(ctime(response.tx_time))