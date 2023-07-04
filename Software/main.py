from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path
import sys
import cv2
import os


class Recorder(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    scale = QtCore.pyqtSignal(float)
    doCapture = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.scaleValue = 1
        self.doCaptureValue = False
        self.scale.connect(self.scaleChanged)
        self.doCapture.connect(self.onCapture)

    def scaleChanged(self, value):
        self.scaleValue = value
    
    def onCapture(self, signal):
        self.doCaptureValue = signal

    def saveImage(self, imagePath, image):
        imageName = 'capture'
        f_extension = '.jpg'
        
        # Create folder if does not exist
        if not os.path.isdir(imagePath):
            os.mkdir(imagePath)
        
        # Generate new file name
        fileNextCount = len(os.listdir(imagePath)) + 1
        newFile = f'{imagePath}/{imageName+str(fileNextCount)+f_extension}'
        
        # Create a file
        if os.path.exists(newFile):
            print("image already exist.")
            return
        cv2.imwrite(newFile, image)

        ### !!!!!!!!!
        # DO NEXT !!!
        # make prediction then save to a specified folder


    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            self.scaleValue = round(self.scaleValue, 2)

            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.flip(rgbImage, 1)
                h, w, ch = rgbImage.shape

                 #prepare the crop
                centerX, centerY = int(h/2),int(w/2)
                radiusX, radiusY = int(centerX*self.scaleValue), int(centerY*self.scaleValue)

                minX, maxX = centerX-radiusX, centerX+radiusX
                minY, maxY = centerY-radiusY, centerY+radiusY

                cropped = rgbImage[minX:maxX, minY:maxY]
                resized_cropped = cv2.resize(cropped, (w, h)) 

                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(resized_cropped, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

                # Save current frame
                if self.doCaptureValue:
                    self.saveImage("./Unspecified", cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2RGB))
                    self.doCaptureValue = False
                

class UI(QtWidgets.QWidget):
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600

    def __init__(self):
        super(UI, self).__init__()
        self.initUI()
	
    def initUI(self):
        hbox = QtWidgets.QHBoxLayout(self)
        
        topleft = QtWidgets.QFrame()
        topleft_layout = QtWidgets.QVBoxLayout(topleft)
        self.topleft_label = QtWidgets.QLabel()
        topleft_layout.addWidget(self.topleft_label)
        topleft.setFrameShape(QtWidgets.QFrame.StyledPanel)

        bottom = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QHBoxLayout(bottom)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(60)
        
        self.black_sigatoka_label = QtWidgets.QLabel("Black Sigatoka")
        self.black_sigatoka_label.setAlignment(QtCore.Qt.AlignCenter)
        self.black_sigatoka_label.setFont(font)

        image_preview = ImagePreviewWidget()
        image_preview.clicked.connect(self.previewClicked) 
        
        self.yellow_sigatoka_label = QtWidgets.QLabel("Yellow Sigatoka")
        self.yellow_sigatoka_label.setAlignment(QtCore.Qt.AlignCenter)
        self.yellow_sigatoka_label.setFont(font)

        bottom_layout.addWidget(self.black_sigatoka_label)
        bottom_layout.addWidget(image_preview)
        bottom_layout.addWidget(self.yellow_sigatoka_label)
        bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        topright = QtWidgets.QFrame()
        topright_layout = QtWidgets.QVBoxLayout(topright)
        topright_button = QtWidgets.QPushButton("Capture")
        topright_button.setFont(font)
        topright_button.clicked.connect(self.capture)

        camera_group_box = QtWidgets.QGroupBox("Camera")
        camera_layout_box = QtWidgets.QVBoxLayout()

        zoom_layout = QtWidgets.QHBoxLayout()

        zoom_label = QtWidgets.QLabel("Zoom")
        zoom_label.setStyleSheet("margin: 5px")
        zoom_layout.addWidget(zoom_label)
        
        self.mySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.mySlider.valueChanged.connect(self.zoom)
        zoom_layout.addWidget(self.mySlider)

        camera_layout_box.addLayout(zoom_layout)
        camera_layout_box.addWidget(topright_button)
        camera_group_box.setLayout(camera_layout_box)

        topright_layout.addWidget(camera_group_box)
        topright.setFrameShape(QtWidgets.QFrame.StyledPanel)

        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)
        splitter1.setSizes([200,100])
        
        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        splitter2.setSizes([1000, 100])
        
        hbox.addWidget(splitter2)
        
        self.setLayout(hbox)
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))

        # Center window
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowTitle('QSplitter demo')

        # Start camera
        # self.recorder = Recorder(self)
        # self.recorder.changePixmap.connect(self.setImage)
        # self.recorder.start()

        self.show()
    
    def capture(self):
        self.recorder.doCapture.emit(True)
        print('sds')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.topleft_label.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def zoom(self):
        sliderVal = self.mySlider.value()
        zoomValue = round(1-(sliderVal/20), 2)
        self.recorder.scale.emit(zoomValue)

    def previewClicked(self):
        image = QtGui.QPixmap('./Yanfei.jpg')
        self.second_ui = PreviewImage(image)


class ImagePreviewWidget(QtWidgets.QLabel):
    clicked= QtCore.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPixmap(
            QtGui.QPixmap('./Yanfei.jpg').scaled(
                100,
                100, 
                QtCore.Qt.KeepAspectRatio, 
                transformMode=QtCore.Qt.SmoothTransformation
            )
        )
    
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        return super().mousePressEvent(ev)



class AlignDelegate(QtWidgets.QStyledItemDelegate): # Table.cell.alignCenter 
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


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


class MySlider(QtWidgets.QWidget):
    def __init__(self, name, maxi, mini, font_size, orientation, parent=None):
        super(MySlider, self).__init__(parent)
        self.setMinimumSize(100, 200)                                          # +++

#    def make_slider(self, name, posx, posy, maxi, mini, font_size, orientation):
#        """posx,posy,font_size,max,min = int orientation = Qt.Horizontal or Vertical,name = str name of slider"""

        self.label = QtWidgets.QLabel(name, self)
#        self.label.setGeometry(posx - 30, posy - 45, 100, 40)  # 210,60
        self.label.setFont(QtGui.QFont("Sanserif", font_size))
        self.sliderWidget = QtWidgets.QSlider(self)
        self.sliderWidget.setOrientation(orientation)
        self.sliderWidget.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderWidget.setMaximum(maxi)
        self.sliderWidget.setMinimum(mini)
        self.sliderWidget.setTickInterval(1)
#        self.slider.move(posx, posy)
        self.label2 = QtWidgets.QLabel(str(mini), self)
        self.label2.setFont(QtGui.QFont("Sanserif", font_size))
#        self.label2.setGeometry(posx, posy + 90, 50, 20)
        self.sliderWidget.valueChanged.connect(self.changed_value)

# ++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.sliderWidget, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label2, alignment = QtCore.Qt.AlignCenter)
        self.layout.addStretch()
# ++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def slider(self):
        return self.sliderWidget

    def value(self):
        return self.sliderWidget.value()

    def changed_value(self, val):                                             # + val
        print(val)
#        wartosc = self.slider.value()
#        self.label2.setText(str(wartosc))
        self.label2.setNum(val)                                               # + val

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()