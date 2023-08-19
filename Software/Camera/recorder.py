from PyQt5 import QtGui, QtCore
from Utils.utils import Analytics, Image
from Config import settings

import cv2
import os

import tensorflow as tf
import numpy as np

class Recorder(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    scale = QtCore.pyqtSignal(float)
    doCapture = QtCore.pyqtSignal(bool)
    pause = QtCore.pyqtSignal(bool)
    projectPath = QtCore.pyqtSignal(str)
    on_classify = QtCore.pyqtSignal(bool)

    # OpenCV capture device
    selectedCameraIndex = 0
    cap = cv2.VideoCapture(selectedCameraIndex)
    isOpened = cap.isOpened()

    # Tensorflow model
    loaded_model =  tf.keras.models.load_model('./models/keras_model.h5')

    # Latest output
    image:Image = None
    image_path = ''

    def __init__(self, parent=None, selectedPath='') -> None:
        QtCore.QThread.__init__(self, parent)
        self.parent = parent

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
        imageName = settings.imageName
        f_extension = settings.f_extension
        
        # Create folder if does not exist
        if not os.path.isdir(imagePath):
            os.mkdir(imagePath)
        
        # Generate new file name
        fileNextCount = len(os.listdir(imagePath)) + 1
        self.image_path = f'{imagePath}/{imageName+str(fileNextCount)+f_extension}'
        
        # Create a file
        if os.path.exists(self.image_path):
            print("image already exist.")
            return
        cv2.imwrite(self.image_path, image)

    def classify(self, img_array:np.ndarray) -> list:
        ### !!!!!!!!!
        # TODO: make prediction then save to a specified folder
        # Rebuild model

        img_array_batch = tf.expand_dims(img_array, 0) # create a batch

        yhat = self.loaded_model.predict(img_array_batch)
        score = tf.nn.softmax(yhat[0]) # use only when softmax included in model

        print(yhat)
        print(type(score))

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(settings.class_names[np.argmax(score)], 100 * np.max(score))
        )

        today = Analytics.get_clock()
        self.image = Image(
            id = Analytics.create_new_id(),
            path = self.image_path,
            classification = settings.class_names[np.argmax(score)],
            confidence = float(np.max(score)),
            shape = img_array.shape,
            type = settings.f_extension,
            created = today,
            modified = today
        )

        self.on_classify.emit(True)
        return score # Confidence

    def onCamSelectedIndex(self, index):
        self.selectedCameraIndex = index
        self.pauseValue = True
        self.cap = cv2.VideoCapture(self.selectedCameraIndex)
        self.pauseValue = False
 
    def run(self):
        while self.isOpened:
            # print(self.parent.resizableRect.getRect())
            ret, frame = self.cap.read()
            self.scaleValue = round(self.scaleValue, 2)

            if ret and not self.pauseValue:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.flip(rgbImage, 1)
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
                    # Classify resized image based on model's input_shape
                    img_array = cv2.cvtColor(
                        cv2.resize(
                            src = resized_cropped,
                            dsize = settings.IMAGE_SIZE,
                            interpolation = cv2.INTER_AREA
                        ),
                        cv2.COLOR_BGR2RGB
                    ).astype(np.float32)
                    result = self.classify(img_array)

                    classification = settings.class_names[np.argmax(result)]
                    confidence = 100 * np.max(result)

                    for cnames in settings.class_names:
                        if cnames == classification:
                            print(f'saving to {classification}')

                            # Save original image
                            self.saveImage(
                                f'{self.selectedPath}/{cnames}',
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