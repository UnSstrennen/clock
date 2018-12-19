import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog, QMainWindow, QComboBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from math import fabs
import json


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        with open('cfg.json') as f:
            self.cfg_dict = json.loads(f.read())
        self.name_file = self.cfg_dict['background_image']
        self.color_frame = (0, 0, 0)
        self.old_pos = None

        # Генерация окна
        self.setWindowTitle('Clock')
        self.setGeometry(0, 740, 260, 160)
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

        # Комбобокс для стилизации
        self.combo = QComboBox(self)
        self.combo.setObjectName('Combo')
        self.combo.resize(75, 20)
        self.combo.addItems(["Stylization", "Color", "OLDS",
                             "Backdrop2", "Backdrop3", "Backdrop4"])
        self.combo.activated[str].connect(self.onActivated)
        self.combo.move(30, 30)

        self.general()

    # Сцена часов
    def general(self):
        self.background_image()
        try:
            self.btn_st.show()
            self.btn_gn.hide()
            self.combo.hide()
        except AttributeError:
            pass

    # Сцена настроек
    def settings(self):
        self.btn_gn.show()
        self.btn_st.hide()
        self.combo.show()

    # Изменение фона окна
    def palette(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet("#MainWidget {background-color: %s;}" % color.name())
            self.paintEvent(self, clr=self.hex_to_rgb(color.name()), palette_call=True)

    # рисование окна
    def paintEvent(self, event: QtGui.QPaintEvent, clr=(255, 255, 255), palette_call=False):
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

    def onActivated(self, val):
        backgrounds = {'OLDS': 'olds.jpg', 'Backdrop2': 'Фон.png', 'Backdrop3': '', 'Backdrop4': ''}
        if val == 'Color':
            self.palette()
        elif val not in ('Color', 'Stylization'):
            self.setStyleSheet("#MainWidget {background-image: url(%s);}" % backgrounds[val])
            self.paintEvent(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Example()
    w.show()

    sys.exit(app.exec_())
