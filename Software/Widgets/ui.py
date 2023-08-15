from PyQt5 import QtWidgets, QtGui, QtCore
from Widgets.imagePreview import ImagePreviewWidget, PreviewImage
from Widgets.rect import ResizableRect
from Camera.recorder import Recorder
from Widgets.camOpts import CamOptions
from Utils.utils import Analytics
from Config import settings


class UI(QtWidgets.QWidget):
    analytics:Analytics = None

    def __init__(self, parent, hasFolderSelected=False):
        super(UI, self).__init__()
        cameras = CamOptions.get_available_cameras()

        self.on_classify_value = False
        self.parent = parent
	
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setContentsMargins(5, 5, 5, 5)
        hbox.setSpacing(0)
        
        topleft = QtWidgets.QFrame()
        self.topleft_layout = QtWidgets.QVBoxLayout(topleft)
        self.topleft_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.scene = QtWidgets.QGraphicsScene(0, 0, settings.camera_scale[0], settings.camera_scale[1])
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setAlignment(QtCore.Qt.AlignCenter)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.videoCapture = QtWidgets.QLabel()
        self.videoCapture.resize(settings.camera_scale[0], settings.camera_scale[1])
        self.videoCapture.setAlignment(QtCore.Qt.AlignCenter)


        initialWidth = 350
        initialHeight = 200
        self.resizableRect = ResizableRect(
            x = settings.camera_scale[0]/2,
            y = settings.camera_scale[1]/2,
            width = initialWidth,
            height = initialHeight,
            onCenter = True
        )

        if not(len(cameras) > 0 and hasFolderSelected):
            self.videoCapture = QtWidgets.QLabel("Select a project directory, the camera should start.")
            self.videoCapture.resize(settings.camera_scale[0], settings.camera_scale[1])
            self.videoCapture.setAlignment(QtCore.Qt.AlignCenter)
            font = self.videoCapture.font()
            font.setFamily("Verdana")
            font.setPointSize(8)
            self.videoCapture.setFont(font)

        self.scene.addWidget(self.videoCapture)
        self.scene.addItem(self.resizableRect)
        self.resizableRect.hide()

        self.topleft_layout.addWidget(self.view)
        topleft.setFrameShape(QtWidgets.QFrame.StyledPanel)

        bottom = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QHBoxLayout(bottom)

        font = QtGui.QFont("Poppins Medium", pointSize=11, weight=60)
        
        self.black_sigatoka_label = QtWidgets.QLabel(settings.b_sigatoka)
        self.black_sigatoka_label.setAlignment(QtCore.Qt.AlignCenter)
        self.black_sigatoka_label.setFont(font)

        self.image_preview = ImagePreviewWidget()
        self.image_preview.clicked.connect(self.previewClicked) 
        
        self.yellow_sigatoka_label = QtWidgets.QLabel(settings.y_sigatoka)
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
            controlsLayout.setRowMinimumHeight(row, 60)

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

        # GrabCut
        self.grabcut_label = QtWidgets.QLabel("GrabCut")
        self.grabcut_label.setFont(font)
        controlsLayout.addWidget(self.grabcut_label, 3, 0, 1, 1)
        
        self.grabcut_checkbox = QtWidgets.QCheckBox()
        self.grabcut_checkbox.clicked.connect(self.grabcut_bool)
        controlsLayout.addWidget(self.grabcut_checkbox, 3, 1, 1, 3)

        camera_layout_box.addLayout(controlsLayout)

        # grabcut_layout = QtWidgets.QHBoxLayout()
        # grabcut_label = QtWidgets.QLabel("GrabCut")
        # grabcut_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        # grabcut_layout.addWidget(grabcut_label)
        
        # camera_layout_box.addLayout(grabcut_layout)


        # Capture
        capture_button = QtWidgets.QPushButton("Capture")
        font.setPointSize(11)
        capture_button.setFont(font)
        capture_button.clicked.connect(self.capture)

        camera_layout_box.addWidget(capture_button)


        self.camera_group_box.setLayout(camera_layout_box)

        topright = QtWidgets.QFrame()
        topright_layout = QtWidgets.QVBoxLayout(topright)
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

        # Start camera
        self.recorder = Recorder(parent=parent, selectedPath=self.parent.project.path)
        self.recorder.on_classify.connect(self.on_classify_emitted)
        self.recorder.changePixmap.connect(self.setImage)
        if len(cameras) > 0 and hasFolderSelected:
            self.camera_group_box.setEnabled(True)
            self.recorder.start()

        # Context Menu
        self.contextMenu = QtWidgets.QMenu(self)
        self.save_controls = self.contextMenu.addAction("Save controls")
        self.defisheye = self.contextMenu.addAction("Defisheye")
        self.stopRecorder = self.contextMenu.addAction("Stop recorder")
        self.defisheye.setCheckable(True)
    
    def on_classify_emitted(self, value):
        self.analytics.add_image(image=self.recorder.image)
        self.on_classify_value = value

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        action = self.contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == self.save_controls:
            self.parent.project.save_controls(
                brightness = self.brightnessSlider.value(),
                contrast = self.contrastSlider.value(),
                zoom = self.zoomSlider.value(),
                isDefisheye = self.defisheye.isChecked(),
                isGrabCut = self.grabcut_checkbox.isChecked()
            )
            
        elif action == self.defisheye:
            self.defisheye.setChecked(self.defisheye.isChecked())

        elif action == self.stopRecorder:
            self.recorder.isOpened = False

    def capture(self):
        self.recorder.doCapture.emit(True)

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

    def grabcut_bool(self, value):
        if value:
            self.resizableRect.show()
        else:
            self.resizableRect.hide()