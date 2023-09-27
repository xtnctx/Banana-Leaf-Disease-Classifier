from PyQt5 import QtGui, QtCore
from Utils.utils import Analytics, Image
from Config import settings
from . import foreground_extraction as forex

import cv2
import os

import tensorflow as tf
import numpy as np

class Recorder(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    doCapture = QtCore.pyqtSignal(bool)
    pause = QtCore.pyqtSignal(bool)
    projectPath = QtCore.pyqtSignal(str)
    on_classify = QtCore.pyqtSignal(bool)

    # Camera properties
    brightness = QtCore.pyqtSignal(int)
    contrast = QtCore.pyqtSignal(float)
    sharpness = QtCore.pyqtSignal(float)
    scale = QtCore.pyqtSignal(float)

    # OpenCV capture device
    selectedCameraIndex = 0
    cap = cv2.VideoCapture(selectedCameraIndex)
    isOpened = cap.isOpened()

    # Tensorflow model
    loaded_model =  tf.keras.models.load_model('./models/keras_model.h5')

    # Latest output
    image:Image = None
    image_path = ''

    # Foreground Extraction
    grabcut = forex.GrabCut()

    def __init__(self, parent=None, selectedPath='') -> None:
        QtCore.QThread.__init__(self, parent)
        self.parent = parent

        self.brightnessValue = 0
        self.brightness.connect(self.brightnessChanged)

        self.contrastValue = 0
        self.contrast.connect(self.contrastChanged)

        self.sharpnessValue = 0
        self.sharpness.connect(self.sharpnessChanged)

        self.scaleValue = 1
        self.scale.connect(self.scaleChanged)

        self.doCaptureValue = False
        self.doCapture.connect(self.onCapture)

        self.pauseValue = False
        self.pause.connect(self.pauseEmitted)

        self.selectedPath = selectedPath
        self.projectPath.connect(self.projectPathSelected)

    def brightnessChanged(self, value):
        self.brightnessValue = value
        # self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)
        print(f'Brightness: {value}')
    
    def contrastChanged(self, value):
        self.contrastValue = value
        # self.cap.set(cv2.CAP_PROP_CONTRAST, value)
        print(f'Contrast: {value}')
    
    def sharpnessChanged(self, value):
        self.sharpnessValue = value
        # self.cap.set(cv2.CAP_PROP_SHARPNESS, value)
        print(f'Sharpness: {value}')

    def scaleChanged(self, value):
        self.scaleValue = value
        print(f'Zoom: {value}')
    
    def onCapture(self, signal):
        self.doCaptureValue = signal
    
    def pauseEmitted(self, value):
        self.pauseValue = value
    
    def projectPathSelected(self, path):
        self.selectedPath = path
        print(f'New selected path is: {self.selectedPath}')

    def saveImage(self, imagePath, image):
        # Create folder if does not exist
        if not os.path.isdir(imagePath):
            os.mkdir(imagePath)

        # Create a file
        if os.path.exists(self.image_path):
            print("image already exist.")
            return
        cv2.imwrite(self.image_path, image)
    
    def sharp_mask(self, image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened
    
    def contrast_brightness(self, image, contrastValue, brightnessValue):
        return cv2.convertScaleAbs(image, alpha=contrastValue, beta=brightnessValue)

    def classify(self, img_array:np.ndarray) -> list:
        ### !!!!!!!!!
        # TODO: make prediction then save to a specified folder
        # Rebuild model

        img_array_batch = tf.expand_dims(img_array, 0) # create a batch

        yhat = self.loaded_model.predict(img_array_batch)
        score = tf.nn.softmax(yhat[0]) # use only when softmax included in model

        print(yhat)
        print(type(score))

        classification = settings.class_names[np.argmax(score)]
        confidence = np.max(score)

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(classification, confidence)
        )

        imagePath = f'{self.selectedPath}/{classification}'
        imageName = settings.imageName
        f_extension = settings.f_extension

        # Generate new file name
        fileNextCount = len(os.listdir(imagePath)) + 1
        self.image_path = f'{imagePath}/{imageName+str(fileNextCount)+f_extension}'

        today = Analytics.get_clock()
        self.image = Image(
            id = Analytics.create_new_id(),
            path = self.image_path,
            classification = classification,
            confidence = float(confidence),
            tensor_shape = img_array.shape,
            type = f_extension,
            created = today,
            modified = today
        )

        self.on_classify.emit(True)
        return (classification, confidence)

    def onCamSelectedIndex(self, index):
        self.selectedCameraIndex = index
        self.pauseValue = True
        self.cap = cv2.VideoCapture(self.selectedCameraIndex)
        self.isOpened = self.cap.isOpened()
        self.pauseValue = False
 
    def run(self):
        while not self.isOpened:
            self.parent.videoCapture.setText('Trying to open the camera, please wait.')
            self.cap = cv2.VideoCapture(self.selectedCameraIndex)
            self.isOpened = self.cap.isOpened()

        while self.isOpened:
            ret, frame = self.cap.read()
            self.scaleValue = round(self.scaleValue, 2)

            if ret and not self.pauseValue:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.flip(rgbImage, 1)
                rgbImage = self.contrast_brightness(rgbImage, contrastValue=self.contrastValue, brightnessValue=self.brightnessValue)
                rgbImage = self.sharp_mask(rgbImage, amount=self.sharpnessValue)
                h, w, ch = rgbImage.shape

                #prepare the crop
                centerX, centerY = int(h/2), int(w/2)
                radiusX, radiusY = int(centerX*self.scaleValue), int(centerY*self.scaleValue)

                minX, maxX = centerX-radiusX, centerX+radiusX
                minY, maxY = centerY-radiusY, centerY+radiusY

                cropped = rgbImage[minX:maxX, minY:maxY]
                resized_cropped = cv2.resize(cropped, (w, h))

                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(resized_cropped, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(*settings.camera_scale)
                self.changePixmap.emit(p)

                # Save current frame
                if self.doCaptureValue:
                    if self.parent.grabcut_checkbox.isChecked():
                        resized_cropped = self.grabcut.extract(image=resized_cropped, rect=self.parent.resizableRect.getRect())

                    # Classify resized image based on model's input_shape
                    img_array = cv2.cvtColor(
                        cv2.resize(
                            src = resized_cropped,
                            dsize = settings.IMAGE_SIZE,
                            interpolation = cv2.INTER_AREA
                        ),
                        cv2.COLOR_BGR2RGB
                    )

                    classification, confidence = self.classify(img_array.astype(np.float32))

                    for cname in settings.class_names:
                        if cname == classification:
                            # Save original image
                            self.saveImage(
                                f'{self.selectedPath}/{cname}',
                                cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2RGB)
                            )
                    
                    self.parent.recorder_results.emit(
                        {
                            'classification': classification,
                            'confidence': confidence,
                            'image_path': self.image_path
                        }
                    )
                    
                    self.doCaptureValue = False
        self.cap.release()
        cv2.destroyAllWindows()