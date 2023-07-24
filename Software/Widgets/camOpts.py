from PyQt5 import QtWidgets, QtCore
from pygrabber.dshow_graph import FilterGraph

def get_available_cameras():

    devices = FilterGraph().get_input_devices()

    available_cameras = {}

    for device_index, device_name in enumerate(devices):
        available_cameras[device_index] = device_name

    return available_cameras

class CamOptions(QtWidgets.QWidget):
    camUsed = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout(self)

        self.name = QtWidgets.QLabel('Choose camera')
        vbox.addWidget(self.name)

        self.comboBox = QtWidgets.QComboBox()
        cam_list = ["Cam1", "Cam2", "Cam3", "Cam4"]
        self.comboBox.addItems(cam_list)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        vbox.addWidget(self.comboBox)

        self.setLayout(vbox)

        # Center the window
        self.resize(200, 80)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def on_combobox_changed(self, index):
        self.camUsed.emit(index)