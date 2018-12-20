import sys
from PyQt5.QtWidgets import (QApplication, QPushButton, QColorDialog,
                             QMainWindow, QComboBox, QLCDNumber, QSlider)
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from math import fabs


from functions import ServerTime, get_local_time, Alarm


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()

        self.check_time_timer = QTimer()
        self.check_time_timer.timeout.connect(self.check_time)

        self.alarm = Alarm(0, 0)  #alarm exemplar
        self.initUI()

    def initUI(self):
        self.color_frame = (0, 0, 0)
        self.old_pos = None
        self.text = ['00', '00']

        # Генерация окна
        self.setWindowTitle('Clock')
        self.setGeometry(0, 0, 260, 160)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('MainWidget')
        self.setStyleSheet("#MainWidget {background-color: #272727;}")

        # Кнопка закрытие окна
        self.btn_close = QPushButton(self, clicked=self.close)
        self.btn_close.setIcon(QtGui.QIcon(QtGui.QPixmap('cross.png')))
        self.btn_close.setFlat(True)
        self.btn_close.resize(17, 17)
        self.btn_close.move(242, 1)
        self.btn_close.show()

        # Кнопка возрата в general
        self.btn_gn = QPushButton(self, clicked=self.general)
        self.btn_gn.setIcon(QtGui.QIcon(QtGui.QPixmap('back.png')))
        self.btn_gn.setFlat(True)
        self.btn_gn.resize(20, 20)
        self.btn_gn.move(1, 1)
        self.btn_gn.show()

        # Кнопка входа в settings
        self.btn_st = QPushButton(self, clicked=self.settings)
        self.btn_st.setIcon(QtGui.QIcon(QtGui.QPixmap("gear.png")))
        self.btn_st.setFlat(True)
        self.btn_st.resize(15, 15)
        self.btn_st.move(3, 3)
        self.btn_st.show()

        # Кнопка будильника
        self.alarm = QPushButton(self, clicked=self.alarm_st)
        self.alarm.setIcon(QtGui.QIcon(QtGui.QPixmap("alarmN.png")))
        self.alarm.setFlat(True)
        self.alarm.resize(25, 25)
        self.alarm.move(204, 39)
        self.alarm.show()

        # Дисплей для будильника
        self.lcdA = QLCDNumber(self)
        self.lcdA.resize(150, 75)
        self.lcdA.move(55, 30)
        self.lcdA.setSegmentStyle(QLCDNumber.Flat)
        self.lcdA.setObjectName("LCDA")
        self.lcdA.setStyleSheet("#LCDA {background-image: url(фон.png); border: 2px solid #4c4c4c;}")
        self.lcdA.display(':'.join(self.text))

        # Слайдер выбора часа
        self.sldH = QSlider(Qt.Vertical, self)
        self.sldH.setMaximum(23)
        self.sldH.move(46, 30)
        self.sldH.resize(9, 75)
        self.sldH.valueChanged.connect(self.slider)

        # Слайдер выбора минут
        self.sldM = QSlider(Qt.Vertical, self)
        self.sldM.setMaximum(59)
        self.sldM.move(206, 30)
        self.sldM.resize(9, 75)
        self.sldM.valueChanged.connect(self.slider2)

        # Дисплей часов
        self.lcd = QLCDNumber(self)
        self.lcd.resize(150, 75)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.move(55, 40)
        self.lcd.display(make_time_for_lcd())
        self.lcd.setObjectName("LCD")
        self.lcd.setStyleSheet("#LCD {background-image: url(фон.png); border: 2px solid #4c4c4c;}")

        # Комбобокс для стилизации
        self.combo = QComboBox(self)
        self.combo.setObjectName('Combo')
        self.combo.resize(75, 20)
        self.combo.addItems(["Stylization", "Color", "Olds",
                             "Backdrop2", "Backdrop3", "Backdrop4"])
        self.combo.activated[str].connect(self.onActivated)
        self.combo.move(30, 30)

        self.general()

    # Сцена часов
    def general(self):
        try:
            self.btn_st.show()
            self.btn_gn.hide()
            self.combo.hide()
            self.alarm.show()
            self.lcd.show()
            self.sldH.hide()
            self.sldM.hide()
            self.lcdA.hide()
        except AttributeError:
            pass


    # Сцена настроек
    def settings(self):
        self.btn_gn.show()
        self.btn_st.hide()
        self.combo.show()
        self.alarm.hide()
        self.lcd.hide()
        self.sldH.hide()
        self.sldM.hide()
        self.lcdA.hide()

    def alarm_st(self):
        self.btn_gn.show()
        self.btn_st.hide()
        self.alarm.hide()
        self.lcd.hide()
        self.sldH.show()
        self.sldM.show()
        self.lcdA.show()

    # Изменение фона окна
    def palette(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet("#MainWidget {background-color: %s;}" % color.name())
            self.paintEvent(self, clr=self.hex_to_rgb(color.name()))

    # рисование окна
    def paintEvent(self, event: QtGui.QPaintEvent, clr=(0, 0, 0)):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(int(fabs(clr[0] - 75)),
                                               int(fabs(clr[1] - 75)),
                                               int(fabs(clr[2] - 75))), 2))
        painter.drawRect(self.rect())

    # нужна для перемещёния окна
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    # вызывается всякий раз, когда мышь перемещается
    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)

    # перевод их hex в rgb
    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def onActivated(self, val):
        backgrounds = {'Stylization': '#272727', 'Olds': 'olds.png', 'Backdrop2': 'matrix.png',
                       'Backdrop3': '', 'Backdrop4': ''}
        if val == 'Color':
            self.palette()
        elif val == 'Stylization':
            self.setStyleSheet("#MainWidget {background-color: #272727;}")
        elif val != 'Color':
            self.setStyleSheet("#MainWidget {background-image: url(%s);}" % backgrounds[val])
            self.paintEvent(self)

    def slider(self, n):
        if len(str(n)) == 1:
            n = '0' + str(n)
        self.text[0] = str(n)
        self.lcdA.display(':'.join(self.text))

    def slider2(self, n):
        if len(str(n)) == 1:
            n = '0' + str(n)
        self.text[1] = str(n)
        self.lcdA.display(':'.join(self.text))

    def check_time(self):
        """ compares the time by the timer command """
        if 'lcd' in dir(self):
            self.lcd.display(make_time_for_lcd())
        self.check_alarm()

    def check_alarm(self):
        """ alarm handler called by timer """
        print(1)

    def change_alarm_status(self):
        """ changes alarm status """
        self.alarm.tracked = not self.alarm.tracked


def make_time_for_lcd():
    """ makes the time data compatible for lcd widget """
    time = get_local_time()
    hours = str(time['hours'])
    minutes = str(time['minutes'])
    if len(hours) == 1:
        hours = '0' + hours
    if len(minutes) == 1:
        minutes = '0' + minutes
    return hours + ':' + minutes


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Example()

    TIME_TIMER_PERIOD = 1000  # period in milliseconds
    w.check_time_timer.start(TIME_TIMER_PERIOD)
    w.show()

    sys.exit(app.exec_())
