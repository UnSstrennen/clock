from ntplib import NTPClient
from datetime import datetime
from time import ctime, localtime, mktime
from subprocess import Popen, PIPE, check_call
from datetime import datetime, timedelta, timezone


class ServerTime:
    """ server client class """
    def __init__(self):
        self.hosts = ['ntp1.stratum2.ru', 'ntp2.stratum2.ru', 'pool.ntp.org']
        self.client = NTPClient()
        self.time_obj = None
        self.get_time()
        self.TIMEZONE = datetime.now(timezone.utc).astimezone().utcoffset() // timedelta(seconds=1) // 3600

    def print_time(self):
        """ prints the server time """
        print(ctime(self.client.request(self.hosts[0]).tx_time))

    def get_time(self):
        for host in self.hosts:
            try:
                self.time_obj = localtime(self.client.request(host).tx_time)
                if bool(self.time_obj):
                    return {'day': self.time_obj[2], 'month': self.time_obj[1], 'year': self.time_obj[0],
                            'hours': self.time_obj[3] - self.TIMEZONE, 'minutes': self.time_obj[4], 'seconds': self.time_obj[5],
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
    """ counts the time delta """
    server = datetime.fromtimestamp(mktime(ServerTime().time_obj))
    local = datetime.now()
    delta = server - local
    days = delta.days
    seconds = delta.seconds
    if seconds >= 60:
        minutes = seconds // 60
        seconds -= minutes * 60
    else:
        minutes = 0
    if minutes >= 60:
        hours = minutes // 60
        minutes = minutes - hours * 60
    else:
        hours = 0
    microseconds = delta.microseconds
    return {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds, 'microseconds': microseconds}


def set_server_time():
    """ установка серверного времени """
    t = ServerTime().get_time()
    args_to_send = [t['year'], t['month'], t['day of week'], t['day'], t['hours'], t['minutes'],
                    t['seconds'], 0]
    with open('time.txt', 'w') as file:
        file.write(str(args_to_send)[1:-1])
    process = Popen('python system_time_setting.py', stdout=PIPE, shell=True)



class Alarm:
    def __init__(self, hours, minutes):
        self.minutes = minutes
        self.hours = hours
        self.tracked = False
        self.track = 0  # индекс мелодии
        self.process = None  # будущий процесс обработки звука

    def set(self, hours, minutes):
        """ изменение настроек будильника """
        self.minutes = minutes
        self.hours = hours

    def start(self):
        """ запуск будильника """
        self.tracked = True

    def stop(self):
        """ остановка будильника """
        self.tracked = False

    def is_working(self):
        """ возвращает текущее состояние будильника (bool)"""
        return self.tracked

    def check(self):
        """ проверяет, пора ли звонить. Возвращает True, если самое время (bool) """
        local_hours = get_local_time()['hours']
        local_minutes = get_local_time()['minutes']
        if local_hours == self.hours and local_minutes == local_minutes:
            return True
        else:
            return False

    def start_sound(self, *args):
        """ будильник начинает звонить """
        # лучше перепроверить
        self.tracked = False

        # если нужно проиграть другой звук будильника - подстраиваемся
        if args:
            self.track = args[0]

        self.process = Popen("python sound.py " + str(self.track), stdout=PIPE, shell=True)

    def stop_sound(self):
        """ остановка звонка будильника """
        check_call("TASKKILL /F /PID {pid} /T".format(pid=self.process.pid))
