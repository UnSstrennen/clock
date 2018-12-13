from ntplib import NTPClient
from datetime import datetime
from time import ctime, localtime, strftime, sleep



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
                    return {'day': time_obj[2], 'month': time_obj[1], 'year': time_obj[0],
                            'hours': time_obj[3], 'minutes': time_obj[4], 'seconds': time_obj[5],
                            'day of week': time_obj[6]}
            except Exception:
                pass


def get_local_time():
    """ returns the time on machine """
    t = datetime.now()
    return {'day': t.day, 'month': t.month, 'year': t.year, 'hours': t.hour,
            'minutes': t.minute, 'seconds': t.second, 'microseconds': t.microsecond}
