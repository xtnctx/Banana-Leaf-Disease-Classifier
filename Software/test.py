import sys

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MySlider(QWidget):
    def __init__(self, name, maxi, mini, font_size, orientation, parent=None):
        super(MySlider, self).__init__(parent)
        self.setMinimumSize(100, 200)                                          # +++

#    def make_slider(self, name, posx, posy, maxi, mini, font_size, orientation):
#        """posx,posy,font_size,max,min = int orientation = Qt.Horizontal or Vertical,name = str name of slider"""

        self.label = QLabel(name, self)
#        self.label.setGeometry(posx - 30, posy - 45, 100, 40)  # 210,60
        self.label.setFont(QtGui.QFont("Sanserif", font_size))
        self.slider = QSlider(self)
        self.slider.setOrientation(orientation)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMaximum(maxi)
        self.slider.setMinimum(mini)
        self.slider.setTickInterval(1)
#        self.slider.move(posx, posy)
        self.label2 = QLabel(str(mini), self)
        self.label2.setFont(QtGui.QFont("Sanserif", font_size))
#        self.label2.setGeometry(posx, posy + 90, 50, 20)
        self.slider.valueChanged.connect(self.changed_value)
# ++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv        
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label, alignment = Qt.AlignCenter)
        self.layout.addWidget(self.slider, alignment = Qt.AlignCenter)
        self.layout.addWidget(self.label2, alignment = Qt.AlignCenter)
        self.layout.addStretch()
# ++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def changed_value(self, val):                                             # + val
        print(val)
#        wartosc = self.slider.value()
#        self.label2.setText(str(wartosc))
        self.label2.setNum(val)                                               # + val


class Window(QWidget):
#    """kreowanie klasy okna"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator liczby kombinacji")
#        self.setGeometry(100, 60, 750, 320)
        self.resize(750, 300)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.layout = QHBoxLayout(self)                                              # +++
        self.layout.addStretch()

        self.test_slider2 = MySlider("Zoom", 6, 1, 12, Qt.Horizontal, self)
#        self.test_slider2.make_slider(("   Liczba\n   czegos"), 140, 95, 6, 1, 12, Qt.Vertical)
        self.layout.addWidget(self.test_slider2)                                      # +++

        self.layout.addStretch()


if __name__ == '__main__': 
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Window()
    window.show()
    sys.exit(app.exec())