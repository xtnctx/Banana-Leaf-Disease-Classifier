from PyQt5 import QtWidgets, QtGui, QtCore
from Widgets.imagePreview import ImagePreviewWidget, PreviewImage
from Widgets.rect import ResizableRect
from Camera.recorder import Recorder
from Widgets.camOpts import CamOptions
from Utils.utils import Analytics
from Utils import style
from Utils.system import getAccentColor
from Config import settings


class UI(QtWidgets.QWidget):
    analytics:Analytics = None
    recorder_results = QtCore.pyqtSignal(dict)

    color = getAccentColor()
    qcolor = f'rgb({color[0]}, {color[1]}, {color[2]})'
    windowsAccentColor =  QtGui.QColor(color[0], color[1], color[2])

    def get_results(self, results):
        classification = results['classification']
        confidence = results['confidence']
        image_path = results['image_path']

        if classification == settings.b_sigatoka:
            self.black_sigatoka_label.setText('{} ({:.2f}%)'.format(classification, confidence*100))
            self.black_sigatoka_label.setStyleSheet(f'border: 1px solid {self.qcolor}; color: #000000')

            self.yellow_sigatoka_label.setText(settings.y_sigatoka)
            self.yellow_sigatoka_label.setStyleSheet('border: 1px solid #C5C5C5; color: #C5C5C5')

        elif classification == settings.y_sigatoka:
            self.yellow_sigatoka_label.setText('{} ({:.2f}%)'.format(classification, confidence*100))
            self.yellow_sigatoka_label.setStyleSheet(f'border: 1px solid {self.qcolor}; color: #000000')

            self.black_sigatoka_label.setText(settings.b_sigatoka)
            self.black_sigatoka_label.setStyleSheet('border: 1px solid #C5C5C5; color: #C5C5C5')
        
        self.image_preview.updateImage(imagePath=image_path)

    def __init__(self, parent, hasFolderSelected=False):
        super(UI, self).__init__()
        self.availableCameras = CamOptions.get_available_cameras()

        self.scaleValue = 1
        self.recorder_results.connect(self.get_results)

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
            x = (settings.camera_scale[0] - initialWidth) / 2,
            y = (settings.camera_scale[1] - initialHeight) / 2,
            width = initialWidth,
            height = initialHeight,
            onCenter = False
        )

        if not(len(self.availableCameras) > 0 and hasFolderSelected):
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

        self.image_preview = ImagePreviewWidget(
            imagePath = self.parent.analytics.get_latest_image()['path'] if hasFolderSelected else ''
        )
        self.image_preview.clicked.connect(self.previewClicked) 
        
        self.yellow_sigatoka_label = QtWidgets.QLabel(settings.y_sigatoka)
        self.yellow_sigatoka_label.setAlignment(QtCore.Qt.AlignCenter)
        self.yellow_sigatoka_label.setFont(font)

        if hasFolderSelected:
            classification = self.parent.analytics.get_latest_image()['classification']
            if classification == settings.b_sigatoka:
                self.black_sigatoka_label.setStyleSheet(f'border: 1px solid {self.qcolor}; color: #000000')
                self.yellow_sigatoka_label.setStyleSheet('border: 1px solid #C5C5C5; color: #C5C5C5')
            elif classification == settings.y_sigatoka:
                self.yellow_sigatoka_label.setStyleSheet(f'border: 1px solid {self.qcolor}; color: #000000')
                self.black_sigatoka_label.setStyleSheet('border: 1px solid #C5C5C5; color: #C5C5C5')
        else:
            self.black_sigatoka_label.setStyleSheet('border: 1px solid #C5C5C5; color: #C5C5C5')
            self.yellow_sigatoka_label.setStyleSheet('border: 1px solid #C5C5C5; color: #C5C5C5')

        bottom_layout.addWidget(self.black_sigatoka_label)
        bottom_layout.addWidget(self.image_preview)
        bottom_layout.addWidget(self.yellow_sigatoka_label)
        bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.camera_group_box = QtWidgets.QGroupBox("Controls")
        self.camera_group_box.setFont(font)
        camera_layout_box = QtWidgets.QVBoxLayout()

        controlsLayout = QtWidgets.QGridLayout()
        for row in range(5):
            controlsLayout.setRowMinimumHeight(row, 60)

        font.setPointSize(9)

        sliderPalette = QtGui.QPalette()
        sliderPalette.setColor(QtGui.QPalette.Highlight,self.windowsAccentColor)

        # Brightness
        self.brightness_label = QtWidgets.QLabel("Brightness")
        self.brightness_label.setFont(font)
        controlsLayout.addWidget(self.brightness_label, 0, 0, 1, 1)

        self.brightnessSlider = QtWidgets.QSlider()
        self.brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brightnessSlider.setStyleSheet(style.slider)
        self.brightnessSlider.setPalette(sliderPalette)
        self.brightnessSlider.setRange(-64, 64)
        self.brightnessSlider.valueChanged.connect(self.set_brightness)
        controlsLayout.addWidget(self.brightnessSlider, 0, 1, 1, 1)

        self.brightness_valuelabel = QtWidgets.QLabel()
        self.brightness_valuelabel.setFont(font)
        self.brightness_valuelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_valuelabel.setFixedWidth(20)
        controlsLayout.addWidget(self.brightness_valuelabel, 0, 2, 1, 1)


        # Contrast
        self.contrast_label = QtWidgets.QLabel("Contrast")
        self.contrast_label.setFont(font)
        controlsLayout.addWidget(self.contrast_label, 1, 0, 1, 1)

        self.contrastSlider = QtWidgets.QSlider()
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.contrastSlider.setStyleSheet(style.slider)
        self.contrastSlider.setPalette(sliderPalette)
        self.contrastSlider.setRange(0, 100)
        self.contrastSlider.valueChanged.connect(self.set_contrast)
        controlsLayout.addWidget(self.contrastSlider, 1, 1, 1, 1)

        self.contrast_valuelabel = QtWidgets.QLabel()
        self.contrast_valuelabel.setFont(font)
        self.contrast_valuelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.contrast_valuelabel.setFixedWidth(20)
        controlsLayout.addWidget(self.contrast_valuelabel, 1, 2, 1, 1)

        # Sharpness
        self.sharpness_label = QtWidgets.QLabel("Sharpness")
        self.sharpness_label.setFont(font)
        controlsLayout.addWidget(self.sharpness_label, 2, 0, 1, 1)
        
        self.sharpnessSlider = QtWidgets.QSlider()
        self.sharpnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sharpnessSlider.setStyleSheet(style.slider)
        self.sharpnessSlider.setPalette(sliderPalette)
        self.sharpnessSlider.setRange(0, 100)
        self.sharpnessSlider.valueChanged.connect(self.set_sharpness)
        controlsLayout.addWidget(self.sharpnessSlider, 2, 1, 1, 1)

        self.sharpness_valuelabel = QtWidgets.QLabel()
        self.sharpness_valuelabel.setFont(font)
        self.sharpness_valuelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sharpness_valuelabel.setFixedWidth(20)
        controlsLayout.addWidget(self.sharpness_valuelabel, 2, 2, 1, 1)

        # Zoom
        self.zoom_label = QtWidgets.QLabel("Zoom")
        self.zoom_label.setFont(font)
        controlsLayout.addWidget(self.zoom_label, 3, 0, 1, 1)
        
        self.zoomSlider = QtWidgets.QSlider()
        self.zoomSlider.setOrientation(QtCore.Qt.Horizontal)
        self.zoomSlider.setStyleSheet(style.slider)
        self.zoomSlider.setPalette(sliderPalette)
        self.zoomSlider.setRange(0, 19)
        self.zoomSlider.valueChanged.connect(self.zoom)
        controlsLayout.addWidget(self.zoomSlider, 3, 1, 1, 1)

        self.zoom_valuelabel = QtWidgets.QLabel()
        self.zoom_valuelabel.setFont(font)
        self.zoom_valuelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.zoom_valuelabel.setFixedWidth(20)
        controlsLayout.addWidget(self.zoom_valuelabel, 3, 2, 1, 1)

        # GrabCut
        self.grabcut_label = QtWidgets.QLabel("GrabCut")
        self.grabcut_label.setFont(font)
        controlsLayout.addWidget(self.grabcut_label, 4, 0, 1, 1)
        
        self.grabcut_checkbox = QtWidgets.QCheckBox()
        self.grabcut_checkbox.clicked.connect(self.grabcut_bool)
        controlsLayout.addWidget(self.grabcut_checkbox, 4, 1, 1, 3)

        camera_layout_box.addLayout(controlsLayout)

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
        self.recorder = Recorder(
            parent = self,
            selectedPath = self.parent.project.path
        )
        self.recorder.on_classify.connect(self.on_classify_emitted)
        self.recorder.changePixmap.connect(self.setImage)
        if len(self.availableCameras) > 0 and hasFolderSelected:
            self.camera_group_box.setEnabled(True)
            self.parent.toolBar.actionCamera.setToolTip(self.availableCameras[0])
            self.recorder.start()

        # Context Menu
        self.contextMenu = QtWidgets.QMenu(self)
        self.setControlsToDefault = self.contextMenu.addAction("Default controls")
        self.defisheye = self.contextMenu.addAction("Defisheye")
        self.contextMenu.addSeparator()
        self.save_controls = self.contextMenu.addAction("Save controls")
        self.defisheye.setCheckable(True)

        self.set_userpref_controls()
    
    def on_classify_emitted(self, value):
        self.analytics.add_image(image=self.recorder.image)
        self.on_classify_value = value

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        action = self.contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == self.save_controls:
            self.parent.project.save_controls(
                brightness = self.brightnessSlider.value(),
                contrast = self.contrastSlider.value(),
                sharpness = self.sharpnessSlider.value(),
                zoom = self.zoomSlider.value(),
                isDefisheye = self.defisheye.isChecked(),
                isGrabCut = self.grabcut_checkbox.isChecked()
            )
            
        elif action == self.defisheye:
            self.defisheye.setChecked(self.defisheye.isChecked())

        elif action == self.setControlsToDefault:
            self.set_controls_to_default()

    def capture(self):
        self.recorder.doCapture.emit(True)

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.videoCapture.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def set_brightness(self, value):
        self.recorder.brightness.emit(value)
        self.brightness_valuelabel.setText(str(value))

    def set_contrast(self, value):
        self.recorder.contrast.emit(value)
        self.contrast_valuelabel.setText(str(value))


    def set_sharpness(self, value):
        self.recorder.sharpness.emit(value)
        self.sharpness_valuelabel.setText(str(value))


    def zoom(self, value):
        zoomValue = round(1-(value/20), 2)
        self.recorder.scale.emit(zoomValue)
        self.zoom_valuelabel.setText(str(value))

    
    def set_controls_to_default(self):
        self.brightnessSlider.setValue(0)
        self.brightness_valuelabel.setText(str(0))
        self.recorder.brightness.emit(0)

        self.contrastSlider.setValue(50)
        self.contrast_valuelabel.setText(str(50))
        self.recorder.contrast.emit(50)

        self.sharpnessSlider.setValue(50)
        self.sharpness_valuelabel.setText(str(50))
        self.recorder.sharpness.emit(50)

        self.zoomSlider.setValue(0)
        self.zoom_valuelabel.setText(str(0))
        self.recorder.scale.emit(1.0)

        self.defisheye.setChecked(False)

        self.grabcut_checkbox.setChecked(False)
        self.resizableRect.hide()
    
    def set_userpref_controls(self):
        self.brightnessSlider.setValue(self.parent.project.brightness)
        self.brightness_valuelabel.setText(str(self.parent.project.brightness))
        self.recorder.brightness.emit(self.parent.project.brightness)

        self.contrastSlider.setValue(self.parent.project.contrast)
        self.contrast_valuelabel.setText(str(self.parent.project.contrast))
        self.recorder.contrast.emit(self.parent.project.contrast)

        self.sharpnessSlider.setValue(self.parent.project.sharpness)
        self.sharpness_valuelabel.setText(str(self.parent.project.sharpness))
        self.recorder.sharpness.emit(self.parent.project.sharpness)

        self.zoomSlider.setValue(self.parent.project.zoom)
        self.zoom_valuelabel.setText(str(self.parent.project.zoom))
        self.recorder.scale.emit(round(1-(self.parent.project.zoom/20), 2))

        self.defisheye.setChecked(self.parent.project.isDefisheye)

        self.grabcut_checkbox.setChecked(self.parent.project.isGrabCut)
        self.grabcut_bool(self.parent.project.isGrabCut)

    def previewClicked(self):
        if not self.image_preview.imagePath == settings.default_image_preview:
            self.second_ui = PreviewImage(QtGui.QPixmap(self.image_preview.imagePath))

    def grabcut_bool(self, value):
        if value:
            self.resizableRect.show()
        else:
            self.resizableRect.hide()