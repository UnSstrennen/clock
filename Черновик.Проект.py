import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QHBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from math import fabs
import json


class Example(QWidget):
    def __init__(self):
        super().__init__()
        with open('cfg.json') as f:
            self.cfg_dict = json.loads(f.read())
        self.name_file = self.cfg_dict['background_image']
        self.color_frame = [0, 0, 0]


        # Генерация окна
        self.setWindowTitle('Example')
        self.setGeometry(260, 160, 260, 160)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('MainWidget')
        self.setStyleSheet("#MainWidget {background-color: #272727;}")

        # Кнопка закрытие окна
        self.btn = QPushButton(self, clicked=self.close)
        self.btn.setIcon(QtGui.QIcon(QtGui.QPixmap('cross.png')))
        self.btn.setFlat(True)
        self.btn.resize(15, 15)
        self.btn.move(242, 3)

        # Кнопка в settings
        self.btn2 = QPushButton(self, clicked=self.settings)
        self.btn2.setIcon(QtGui.QIcon(QtGui.QPixmap('sh.gif')))
        self.btn2.setFlat(True)
        self.btn2.resize(20, 20)
        self.btn2.move(1, 1)
        self.btn2.show()

        #Кнопка возрата в general
        self.btn3 = QPushButton(self, clicked=self.general)
        self.btn3.setIcon(QtGui.QIcon(QtGui.QPixmap('st.gif')))
        self.btn3.setFlat(True)
        self.btn3.resize(20, 20)
        self.btn3.move(2, 2)

        self.general()

    def general(self):
        self.background_image()
        try:
            self.btn3.hide()
            self.label.hide()
        except:
            pass

    def settings(self):
        self.btn2.hide()
        self.btn3.show()
        self.label = QLabel('SETTINGS', self)
        self.label.setGeometry(10, 10, 100, 50)
        self.label.QColor(0, 255, 0)
        self.label.show()

    # Изменение фона окна
    def palette(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet("#MainWidget {background-color: %s;}" % color.name())
            self.paintEvent(self, clr=self.hex_to_rgb(color.name()), palette_call=True)

    # рисование окна
    def paintEvent(self, event: QtGui.QPaintEvent, clr=[255, 255, 255], palette_call=False):
        if palette_call:
            self.color_frame = clr
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(fabs(self.color_frame[0] - 70),
                                               fabs(self.color_frame[1] - 70),
                                               fabs(self.color_frame[2] - 70)), 2))
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
        return [int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]

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
