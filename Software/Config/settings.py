from PyQt5 import QtCore
from Utils.utils import AppStyle

#                    W I N D O W                    #
# Main window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# Analytics window size
ANLYTCS_WIDTH = 720
ANLYTCS_HEIGHT = 420

# Window and toolbar title name
WINDOW_TITLE = 'SimbiSU'
TOOLBAR_TITLE = 'ToolBar'

# Styles:
#   windows
#   fusion
#   windowsvista
appStyle = AppStyle.fusion


#                    C A M E R A                    #
# Classification names and path
b_sigatoka = 'Black Sigatoka'
y_sigatoka = 'Yellow Sigatoka'

# Camera image size
camera_scale = (
    640, # width
    480, # height
    QtCore.Qt.KeepAspectRatio # aspect ratio mode
)

# Output file name
imageName = 'capture'
f_extension = '.jpg'




#>_>_>_>_>_>_>_>_>_>_>_>_DEV: P R O J E C T  F I L E>_>_>_>_>_>_>_>_>_>_>_>_#
class Dev:
    pref_file = 'user-preferences.json'
    anlytcs_file = 'analytics.json'