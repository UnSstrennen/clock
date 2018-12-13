from ntplib import NTPClient
from datetime import datetime
from time import ctime


def print_server_time():
    """ prints the server time """
    c = NTPClient()
    response = c.request('pool.ntp.org')
    x = ctime(response.tx_time)
    print(type(x))


def get_local_time():
    """ returns the time on machine """
    t = datetime.now()
    return [t.day, t.month, t.year, t.hour, t.minute, t.second, t.microsecond]
