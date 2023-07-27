from PyQt5 import QtWidgets, QtGui, QtCore
from Widgets.toolBar import ToolBar
from Widgets.imagePreview import ImagePreviewWidget, PreviewImage
from Widgets.camOpts import CamOptions
from Widgets.analytics import Analytics
from Utils import utils
import sys
import cv2
import os


class Recorder(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    scale = QtCore.pyqtSignal(float)
    doCapture = QtCore.pyqtSignal(bool)
    pause = QtCore.pyqtSignal(bool)
    projectPath = QtCore.pyqtSignal(str)

    # OpenCV capture device
    selectedCameraIndex = 0
    cap = cv2.VideoCapture(selectedCameraIndex)

    def __init__(self, parent=None, selectedPath='') -> None:
        QtCore.QThread.__init__(self, parent)
        print(selectedPath)

        self.scaleValue = 1
        self.scale.connect(self.scaleChanged)

        self.doCaptureValue = False
        self.doCapture.connect(self.onCapture)

        self.pauseValue = False
        self.pause.connect(self.pauseEmitted)

        self.selectedPath = selectedPath
        self.projectPath.connect(self.projectPathSelected)

    def scaleChanged(self, value):
        self.scaleValue = value
    
    def onCapture(self, signal):
        self.doCaptureValue = signal
    
    def pauseEmitted(self, value):
        self.pauseValue = value
    
    def projectPathSelected(self, path):
        self.selectedPath = path
        print(f'New selected path is: {self.selectedPath}')

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
    
    def onCamSelectedIndex(self, index):
        self.selectedCameraIndex = index
        self.pauseValue = True
        self.cap = cv2.VideoCapture(self.selectedCameraIndex)
        self.pauseValue = False
 
    def run(self):
        while True:
            ret, frame = self.cap.read()
            self.scaleValue = round(self.scaleValue, 2)

            if ret and not self.pauseValue:
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
                    # TODO: change to selectedPath
                    # make folder icon red as warning
                    # disable capture button if selectedPath not specified
                    self.saveImage(self.selectedPath, cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2RGB))
                    self.doCaptureValue = False
        

class UI(QtWidgets.QWidget):
    def __init__(self, parent=None, selectedPath:str='', hasFolderSelected=False):
        super(UI, self).__init__()
        cameras = CamOptions.get_available_cameras()
	
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setContentsMargins(5, 5, 5, 5)
        hbox.setSpacing(0)
        
        topleft = QtWidgets.QFrame()
        self.topleft_layout = QtWidgets.QVBoxLayout(topleft)
        self.videoCapture = QtWidgets.QLabel()

        if not(len(cameras) > 0 and hasFolderSelected):
            self.videoCapture = QtWidgets.QLabel("Select a project directory, the camera should start.")
            font = self.videoCapture.font()
            font.setFamily("Verdana")
            font.setPointSize(8)
            self.videoCapture.setFont(font)

        self.videoCapture.setAlignment(QtCore.Qt.AlignCenter)
        self.topleft_layout.addWidget(self.videoCapture)
        topleft.setFrameShape(QtWidgets.QFrame.StyledPanel)

        

        bottom = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QHBoxLayout(bottom)

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(60)
        
        self.black_sigatoka_label = QtWidgets.QLabel("Black Sigatoka")
        self.black_sigatoka_label.setAlignment(QtCore.Qt.AlignCenter)
        self.black_sigatoka_label.setFont(font)

        self.image_preview = ImagePreviewWidget()
        self.image_preview.clicked.connect(self.previewClicked) 
        
        self.yellow_sigatoka_label = QtWidgets.QLabel("Yellow Sigatoka")
        self.yellow_sigatoka_label.setAlignment(QtCore.Qt.AlignCenter)
        self.yellow_sigatoka_label.setFont(font)

        bottom_layout.addWidget(self.black_sigatoka_label)
        bottom_layout.addWidget(self.image_preview)
        bottom_layout.addWidget(self.yellow_sigatoka_label)
        bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.camera_group_box = QtWidgets.QGroupBox("Controls")
        self.camera_group_box.setFont(font)
        camera_layout_box = QtWidgets.QVBoxLayout()

        controlsLayout = QtWidgets.QGridLayout()
        for row in range(4):
            controlsLayout.setRowMinimumHeight(row, 50)

        font.setPointSize(9)

        # Brightness
        self.brightness_label = QtWidgets.QLabel("Brightness")
        self.brightness_label.setFont(font)
        controlsLayout.addWidget(self.brightness_label, 0, 0, 1, 1)

        self.brightnessSlider = QtWidgets.QSlider()
        self.brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        controlsLayout.addWidget(self.brightnessSlider, 0, 1, 1, 3)

        # Contrast
        self.contrast_label = QtWidgets.QLabel("Contrast")
        self.contrast_label.setFont(font)
        controlsLayout.addWidget(self.contrast_label, 1, 0, 1, 1)

        self.contrastSlider = QtWidgets.QSlider()
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        controlsLayout.addWidget(self.contrastSlider, 1, 1, 1, 3)

        # Zoom
        self.zoom_label = QtWidgets.QLabel("Zoom")
        self.zoom_label.setFont(font)
        controlsLayout.addWidget(self.zoom_label, 2, 0, 1, 1)
        
        self.zoomSlider = QtWidgets.QSlider()
        self.zoomSlider.setOrientation(QtCore.Qt.Horizontal)
        self.zoomSlider.setRange(0, 19)
        self.zoomSlider.valueChanged.connect(self.zoom)
        controlsLayout.addWidget(self.zoomSlider, 2, 1, 1, 3)

        camera_layout_box.addLayout(controlsLayout)

        # Capture
        topright = QtWidgets.QFrame()
        topright_layout = QtWidgets.QVBoxLayout(topright)
        topright_button = QtWidgets.QPushButton("Capture")
        font.setPointSize(11)
        topright_button.setFont(font)
        topright_button.clicked.connect(self.capture)
        camera_layout_box.addWidget(topright_button)


        self.camera_group_box.setLayout(camera_layout_box)
        topright_layout.addWidget(self.camera_group_box)
        topright.setFrameShape(QtWidgets.QFrame.StyledPanel)

        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)
        splitter1.setSizes([300, 100])
        
        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        splitter2.setSizes([2000, 100])
        
        hbox.addWidget(splitter2)
        
        self.setLayout(hbox)
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))

        # Start camera
        self.recorder = Recorder(parent=parent, selectedPath=selectedPath)
        self.recorder.changePixmap.connect(self.setImage)
        if len(cameras) > 0 and hasFolderSelected:
            self.camera_group_box.setEnabled(True)
            self.recorder.start()
    
    def capture(self):
        self.recorder.doCapture.emit(True)
        print('sds')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.videoCapture.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def zoom(self):
        sliderVal = self.zoomSlider.value()
        zoomValue = round(1-(sliderVal/20), 2)
        print(zoomValue)
        self.recorder.scale.emit(zoomValue)

    def previewClicked(self):
        image = QtGui.QPixmap('./Yanfei.jpg')
        self.second_ui = PreviewImage(image)
    
    




class Root:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600

    selectedPath = ''
    availableCameras = {}

    project = utils.Project()

    def __init__(self, MainWindow: QtWidgets.QMainWindow) -> None:
        hasFolderSelected = True

        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.MainWindow.setCentralWidget(self.centralwidget)

        
        # ToolBar
        self.toolBar = ToolBar(self.MainWindow)
        if self.project.path == "":
            self.toolBar.askFolderIcon()
            hasFolderSelected = False
        self.toolBar.actionFolder.triggered.connect(self.selectPath)
        self.toolBar.actionAnalytics.triggered.connect(self.showAnalytics)
        self.toolBar.actionCamera.triggered.connect(self.selectCamera)
        self.MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        
        self.ui = UI(parent=self.MainWindow, selectedPath=self.project.path, hasFolderSelected=hasFolderSelected)
        if not hasFolderSelected:
            self.ui.camera_group_box.setDisabled(True)
        self.mainLayout.addWidget(self.ui)

        # Center the main window
        self.MainWindow.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        qr = self.MainWindow.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.MainWindow.move(qr.topLeft())

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SimbiApp"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "ToolBar"))
    
    # ToolBar
    def selectPath(self):
        ''' Folder '''
        self.ui.recorder.pause.emit(True)

        self.project.path = str(QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QWidget(), "Select Directory"))
        self.MainWindow.setWindowTitle(self.project.path)

        # Create new or load project
        if self.project.path != '': 
            if not utils.isProject(self.project.path):
                utils.mkNewProject(self.project.path)
                self.toolBar.update()
            self.toolBar.setFolderIconToNormal()

            if not self.ui.recorder.isRunning():
                self.ui.videoCapture.setText('')
                self.ui.recorder.start()
        
            self.toolBar.actionFolder.setToolTip(self.project.path)
            self.ui.recorder.projectPath.emit(self.project.path)
            self.ui.camera_group_box.setEnabled(True)
            
        self.ui.recorder.pause.emit(False)
        print(self.ui.videoCapture.text())
    
    def showAnalytics(self):
        ''' Analytics'''
        self.analyticsWidget = Analytics()
        self.analyticsWidget.show()
    
    def selectCamera(self):
        ''' Camera'''
        if self.project.path == '':
            return
        self.ui.recorder.pause.emit(True)
        self.availableCameras = CamOptions.get_available_cameras()
        self.ui.recorder.pause.emit(False)

        if not self.ui.recorder.isRunning() and len(self.availableCameras) > 0:
            self.ui.camera_group_box.setEnabled(True)
            self.ui.recorder.start()
        else:
            self.ui.recorder.pause.emit(True)
            self.camOption = CamOptions(devices=list(self.availableCameras.values()))
            self.camOption.camUsed.connect(self.ui.recorder.onCamSelectedIndex)
            self.ui.recorder.pause.emit(False)
            self.camOption.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Root(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()