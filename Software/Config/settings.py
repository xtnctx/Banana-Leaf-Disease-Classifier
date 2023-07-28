from PyQt5 import QtCore
from Utils.utils import AppStyle
from Utils import objTypes

#                    W I N D O W                    #
# Main window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# Analytics window size
ANLYTCS_WIDTH = 720
ANLYTCS_HEIGHT = 420

# Window and toolbar title name
WINDOW_TITLE = 'SimbiApp'
TOOLBAR_TITLE = 'ToolBar'

# Styles:
#   windows
#   fusion
#   macintosh
appStyle = AppStyle.fusion


#                    C A M E R A                    #
# Classification names and path
b_sigatoka:objTypes.strName = 'Black Sigatoka'
y_sigatoka:objTypes.strName = 'Yellow Sigatoka'

b_sigatokaP:objTypes.strPath = f'/{b_sigatoka}'
y_sigatokaP:objTypes.strPath = f'/{y_sigatoka}'

# Camera image size
camera_scale = (
    640, # width
    480, # height
    QtCore.Qt.KeepAspectRatio # aspect ratio mode
)

# Output file name
imageName = 'capture'
f_extension = '.jpg'

