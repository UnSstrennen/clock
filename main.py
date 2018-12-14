from ntplib import NTPClient
from datetime import datetime
from time import ctime, localtime, mktime
from win32api import SetSystemTime



class ServerTime:
    """ server client class """
    def __init__(self):
        self.hosts = ['ntp1.stratum2.ru', 'ntp2.stratum2.ru', 'pool.ntp.org']
        self.client = NTPClient()
        self.get_time()

    def print_time(self):
        """ prints the server time """
        print(ctime(self.client.request(self.hosts[0]).tx_time))

    def get_time(self):
        for host in self.hosts:
            try:
                self.x = self.client.request(host).tx_time
                self.time_obj = localtime(self.x)
                if bool(self.time_obj):
                    return {'day': self.time_obj[2], 'month': self.time_obj[1], 'year': self.time_obj[0],
                            'hours': self.time_obj[3], 'minutes': self.time_obj[4], 'seconds': self.time_obj[5],
                            'day of week': self.time_obj[6]}
            except Exception:
                pass

    def get_time_float(self):
        return self.time_obj


def get_local_time():
    """ returns the time on machine """
    t = datetime.now()
    return {'day': t.day, 'month': t.month, 'year': t.year, 'hours': t.hour,
            'minutes': t.minute, 'seconds': t.second, 'microseconds': t.microsecond}


def count_delta():
    server = datetime.fromtimestamp(mktime(ServerTime().time_obj))
    local = datetime.now()
    print(local)
    print(server)
    delta = server - local
    print(delta.seconds)
