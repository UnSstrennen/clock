from ntplib import NTPClient
from datetime import datetime
from time import ctime, localtime
from urllib import request


class ServerTime:
    """ server client class """
    def __init__(self):
        self.hosts = ['ntp1.stratum2.ru', 'ntp2.stratum2.ru', 'pool.ntp.org']
        self.client = NTPClient()

    def print_time(self):
        """ prints the server time """
        print(ctime(self.client.request(self.hosts[0]).tx_time))

    def get_time(self):
        for host in self.hosts:
            try:
                time_obj = localtime(self.client.request(host).tx_time)
                if bool(time_obj):
                    return [time_obj[2], time_obj[1], time_obj[0], time_obj[3], time_obj[4], time_obj[5]]
            except Exception:
                pass


def get_local_time():
    """ returns the time on machine """
    t = datetime.now()
    return [t.day, t.month, t.year, t.hour, t.minute, t.second, t.microsecond]
