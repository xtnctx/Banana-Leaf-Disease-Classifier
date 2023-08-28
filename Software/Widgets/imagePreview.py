from PyQt5 import QtWidgets, QtGui, QtCore
from Config import settings

class ImagePreviewWidget(QtWidgets.QLabel):
    clicked= QtCore.pyqtSignal()
    imagePath = ''
    WIDTH = HEIGHT = 70 

    def __init__(self, imagePath:str='') -> None:
        super().__init__()
        if imagePath == '':
            self.imagePath = settings.default_image_preview
        else:
            self.imagePath = imagePath

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.updateImage(self.imagePath)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
    
    def updateImage(self, imagePath:str):
        self.setPixmap(
            QtGui.QPixmap(imagePath).scaled(
                self.WIDTH,
                self.HEIGHT, 
                QtCore.Qt.KeepAspectRatio, 
                transformMode=QtCore.Qt.SmoothTransformation
            )
        )
        self.imagePath = imagePath
    
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        return super().mousePressEvent(ev)


class PreviewImage(QtWidgets.QMainWindow):
    def __init__(self, image:QtGui.QPixmap):
        super().__init__()
        self.centralwidget = QtWidgets.QWidget(self)
        screen_resolution = QtWidgets.QDesktopWidget().availableGeometry()
        screen_width = screen_resolution.width()
        screen_height = screen_resolution.height()

        imw = image.width()
        imh = image.height()
        imx = (screen_width - imw) // 2
        imy = (screen_height - imh) // 2

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.move(imx, imy)
        self.image.setPixmap(image)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setCentralWidget(self.centralwidget)
        self.installEventFilter(self)
        self.showFullScreen()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.7)
        painter.setBrush(QtCore.Qt.black)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))   
        painter.drawRect(self.rect())
    
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.close()
        return super(PreviewImage, self).eventFilter(object, event)