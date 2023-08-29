from PyQt5 import QtGui
from . import system

color = system.getAccentColor()
table_item_selected_color = f'rgb({color[0]}, {color[1]}, {color[2]})'
windowsAccentColor =  QtGui.QColor(color[0], color[1], color[2])

right_box = f'border: 1px solid {table_item_selected_color}; color: #000000'
wrong_box = 'border: 1px solid #C5C5C5; color: #C5C5C5'

slider = '''
    QSlider::handle:horizontal:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff, stop:1 #ddd);
        border: 1px solid #444;
        border-radius: 4px;
    }
'''

table = '''
    QToolTip {
        color: black;
        background: white;
    }

    QTableWidget::item:selected {
        border: 1px solid %s;
        background-color: rgba(255, 255, 255, 128);
    }
''' % (table_item_selected_color)