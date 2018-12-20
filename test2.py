import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog, QHBoxLayout, QLabel, QMainWindow
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from math import fabs


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.unitUI()

    def unitUI(self):
        self.name_file = None
        self.color_frame = (0, 0, 0)
        self.old_pos = None

        # Генерация окна
        self.setWindowTitle('Clock')
        self.setGeometry(260, 160, 260, 160)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('MainWidget')
        self.setStyleSheet("#MainWidget {background-color: #272727;}")

        # Кнопка закрытие окна
        self.btn_close = QPushButton(self, clicked=self.close)
        self.btn_close.setIcon(QtGui.QIcon(QtGui.QPixmap('cross.png')))
        #self.btn_close.setFlat(True)
        self.btn_close.resize(17, 17)
        self.btn_close.move(242, 1)

        self.general()

    # Сцена часов
    def general(self):
        self.background_image()
        try:
            self.btn_palette.hide()
        except AttributeError:
            pass

        btn_run = QPushButton('S', self, clicked=self.settings)
        btn_run.setIcon(QtGui.QIcon(QtGui.QPixmap('sh.gif')))
        # self.btn_stngs.setFlat(True)
        btn_run.resize(20, 20)
        btn_run.move(1, 1)
        btn_run.show()

    # Сцена настроек
    def settings(self):
        # Кнопка вызова палитры
        self.btn_palette = QPushButton('Палитра', self, clicked=self.palette)
        self.btn_palette.resize(55, 20)
        self.btn_palette.move(60, 20)
        self.btn_palette.show()

        btn_run = QPushButton('G', self, clicked=self.general)
        btn_run.setIcon(QtGui.QIcon(QtGui.QPixmap('sh.gif')))
        # self.btn_run.setFlat(True)
        btn_run.resize(20, 20)
        btn_run.move(1, 1)
        btn_run.show()
        # добавить изменение картинки-фона окна QComboBox https://pythonworld.ru/gui/pyqt5-widgets2.html

    # Изменение фона окна
    def palette(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet("#MainWidget {background-color: %s;}" % color.name())
            self.paintEvent(self, clr=self.hex_to_rgb(color.name()), palette_call=True)

    # рисование окна
    def paintEvent(self, event: QtGui.QPaintEvent, clr=(255, 0, 0), palette_call=False):
        if palette_call:
            self.color_frame = clr
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(int(fabs(self.color_frame[0] - 75)),
                                               int(fabs(self.color_frame[1] - 75)),
                                               int(fabs(self.color_frame[2] - 75))), 2))
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

    # Установка фонового изображения
    def background_image(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Example()
    w.show()

    sys.exit(app.exec_())
