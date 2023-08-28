from PyQt5 import QtWidgets, QtGui, QtCore
from Widgets.toolBar import ToolBar
from Widgets.camOpts import CamOptions
from Widgets.analytics import AnalyticsWindow
from Widgets.ui import UI
from Utils.utils import Project, Analytics
from Config import settings
import sys
import time


class Root(QtWidgets.QMainWindow):
    WINDOW_WIDTH = settings.WINDOW_WIDTH
    WINDOW_HEIGHT = settings.WINDOW_HEIGHT

    selectedPath = ''
    availableCameras = {}

    def __init__(self) -> None:
        super().__init__()
        hasFolderSelected = True

        self.project = Project()
        self.analytics = Analytics(path=self.project.path)

        self.centralwidget = QtWidgets.QWidget(self)
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setCentralWidget(self.centralwidget)
        
        # ToolBar
        self.toolBar = ToolBar(self)
        if self.project.path == "":
            self.toolBar.askFolderIcon()
            hasFolderSelected = False
        else:
            self.toolBar.actionFolder.setToolTip(self.project.path)

        self.toolBar.actionFolder.triggered.connect(self.selectPath)
        self.toolBar.actionAnalytics.triggered.connect(self.showAnalytics)
        self.toolBar.actionCamera.triggered.connect(self.selectCamera)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        
        self.ui = UI(
            parent = self,
            hasFolderSelected = hasFolderSelected
        )
        self.ui.analytics = self.analytics

        if not hasFolderSelected:
            self.ui.camera_group_box.setDisabled(True)
            self.toolBar.actionAnalytics.setDisabled(True)
            self.toolBar.actionCamera.setDisabled(True)
        self.mainLayout.addWidget(self.ui)

        # Center the main window
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", settings.WINDOW_TITLE))
        self.toolBar.setWindowTitle(_translate("MainWindow", settings.TOOLBAR_TITLE))
    
    # ToolBar
    def selectPath(self):
        ''' Folder '''
        self.ui.recorder.pause.emit(True)

        self.project.path = str(QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QWidget(), "Select Directory"))
        self.setWindowTitle(self.project.path)

        # Create new or load project
        if self.project.path != '': 
            if not Project.is_project(self.project.path):
                analytics_read = Project.mkNewProject(self.project.path)
                self.analytics.path = self.project.path
                self.analytics.data = analytics_read
                self.toolBar.update()
            self.toolBar.setFolderIconToNormal()
            self.toolBar.actionAnalytics.setEnabled(True)
            self.toolBar.actionCamera.setEnabled(True)

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
        self.analyticsWidget = AnalyticsWindow(data=self.analytics.data)
        self.analyticsWidget.show()
    
    def selectCamera(self):
        ''' Camera'''
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
            self.toolBar.actionCamera.setToolTip(self.camOption.comboBox.currentText())
            self.camOption.show()
    
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.ui.recorder.isRunning():
            self.ui.recorder.isOpened = False
            print('Closing ...')
            time.sleep(2)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(settings.appStyle)
    root = Root()
    root.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()