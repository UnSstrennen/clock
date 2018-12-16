import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QHBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from math import fabs
import json


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.unitUI()

    def unitUI(self):
        with open('cfg.json') as f:
            self.cfg_dict = json.loads(f.read())
        self.name_file = self.cfg_dict['background_image']
        self.color_frame = (0, 0, 0)
        self.old_pos = None

        # Генерация окна
        self.setWindowTitle('Clock')
        self.setGeometry(260, 160, 260, 160)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('MainWidget')
        self.setStyleSheet("#MainWidget {background-color: #272727;} QLabel {color: white}")

        # Кнопка закрытие окна
        self.btn_close = QPushButton(self, clicked=self.close)
        self.btn_close.setIcon(QtGui.QIcon(QtGui.QPixmap('cross.png')))
        self.btn_close.setFlat(True)
        self.btn_close.resize(17, 17)
        self.btn_close.move(242, 1)

        # Кнопка в settings
        self.btn_stngs = QPushButton(self, clicked=self.settings)
        self.btn_stngs.setIcon(QtGui.QIcon(QtGui.QPixmap('sh.gif')))
        self.btn_stngs.setFlat(True)
        self.btn_stngs.resize(20, 20)
        self.btn_stngs.move(1, 1)
        self.btn_stngs.show()

        # Кнопка возрата в general
        self.btn_in_gen = QPushButton(self, clicked=self.general)
        self.btn_in_gen.setIcon(QtGui.QIcon(QtGui.QPixmap('st.gif')))
        self.btn_in_gen.setFlat(True)
        self.btn_in_gen.resize(18, 18)
        self.btn_in_gen.move(1, 1)

        # Надпись SETTINGS
        self.label = QLabel('SETTINGS', self)
        self.label.setGeometry(10, 10, 100, 50)

        self.general()

    # Сцена часов
    def general(self):
        self.background_image()
        try:
            self.btn_in_gen.hide()
            self.label.hide()
            self.btn_palette.hide()
            self.btn_stngs.show()
        except AttributeError:
            pass

    # Сцена настроек
    def settings(self):
        self.btn_stngs.hide()
        self.btn_in_gen.show()
        # Кнопка вызова палитры
        self.btn_palette = QPushButton('Палитра', self, clicked=self.palette)
        self.btn_palette.resize(55, 20)
        self.btn_palette.move(60, 20)
        self.btn_palette.show()
        self.label.show()

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
        hbox = QHBoxLayout(self)
        pixmap = QtGui.QPixmap(self.name_file)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.setLayout(hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Example()
    w.show()

    sys.exit(app.exec_())
