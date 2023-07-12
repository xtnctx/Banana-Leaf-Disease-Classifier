from PyQt5 import QtWidgets, QtGui, QtCore

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__()

        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setPointSize(9)
        font.setWeight(50)

        self.setParent(parent)

        spacer = QtWidgets.QWidget()
        self.addWidget(spacer)

        self.setStyleSheet("QToolBar{spacing: 20px;}")
        self.setFont(font)
        
        self.setOrientation(QtCore.Qt.Vertical)
        self.setIconSize(QtCore.QSize(30, 25))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        # Folder
        self.actionFolder = QtWidgets.QAction(parent)
        self.actionFolder.setFont(font)
        self.actionFolder.setText("Folder")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./svgIcons/Nx5gxW0N_V1z/mbri-folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFolder.setIcon(icon)
        self.addAction(self.actionFolder)

        # Results
        self.actionResults = QtWidgets.QAction(parent)
        self.actionResults.setFont(font)
        self.actionResults.setText("Results")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./svgIcons/Nx5gxW0N_V1z/mbri-growing-chart.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionResults.setIcon(icon)
        self.addAction(self.actionResults)

        # Camera
        self.actionCamera = QtWidgets.QAction(parent)
        self.actionCamera.setFont(font)
        self.actionCamera.setText("Camera")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./svgIcons/Nx5gxW0N_V1z/mbri-camera.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCamera.setIcon(icon)
        self.addAction(self.actionCamera)
