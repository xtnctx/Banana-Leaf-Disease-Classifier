from . import system

color = system.getAccentColor()
table_item_selected_color = f'rgb({color[0]}, {color[1]}, {color[2]})'

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


