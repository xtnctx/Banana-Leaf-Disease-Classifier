from PyQt5 import QtWidgets, QtGui, QtCore

class ImagePreviewWidget(QtWidgets.QLabel):
    clicked= QtCore.pyqtSignal()

    def __init__(self, imagePath:str='./Yanfei.jpg') -> None:
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.updateImage(imagePath)
    
    def updateImage(self, imagePath:str):
        self.setPixmap(
            QtGui.QPixmap(imagePath).scaled(
                70,
                70, 
                QtCore.Qt.KeepAspectRatio, 
                transformMode=QtCore.Qt.SmoothTransformation
            )
        )
    
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        return super().mousePressEvent(ev)


class PreviewImage(QtWidgets.QMainWindow):
    def __init__(self, image:QtGui.QPixmap):
        super().__init__()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        w = image.width()
        h = image.height()
        x = 500-w-((500-w)//2)
        y = 390-291-((390-291)//2)

        screen_resolution = QtWidgets.QDesktopWidget().availableGeometry()
        width = screen_resolution.width()
        height = screen_resolution.height()

        self.Group_job_table = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_job_table.setGeometry(QtCore.QRect(x, y, w, h))
        self.Group_job_table.setStyleSheet('QGroupBox:title {color: rgb(231, 118, 108);}')
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Group_job_table.setFont(font)
        self.Group_job_table.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Group_job_table.setTitle('I M A G E')
        self.Group_job_table.setCheckable(False)
        self.Group_job_table.setChecked(False)
        self.Group_job_table.setObjectName("Group_job_table")

        qr = self.Group_job_table.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.Group_job_table.move(qr.topLeft())

        self.close_btn = QtWidgets.QPushButton(self.centralwidget)
        self.close_btn.setText("x")
        self.close_btn.setGeometry(QtCore.QRect( (width)-35, 5, self.close_btn.width(), self.close_btn.height()))
        font = QtGui.QFont()
        font.setPixelSize(25)
        font.setBold(True)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet("color: white; border: 0px")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.hide)

        self.image = QtWidgets.QLabel(self.Group_job_table)
        self.image.setPixmap(image)

        # this will hide the title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # setting  the geometry of window
        self.setGeometry(100, 100, 400, 300)
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.showFullScreen()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.7)
        painter.setBrush(QtCore.Qt.black)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))   
        painter.drawRect(self.rect())