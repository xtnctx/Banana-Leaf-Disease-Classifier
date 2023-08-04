from PyQt5 import QtCore
from Utils.utils import AppStyle

#                    W I N D O W                    #
# Main window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# Analytics window size
ANALYTICS_WIDTH = 720
ANALYTICS_HEIGHT = 420

# Window and toolbar title name
WINDOW_TITLE = 'SimbiSU'
TOOLBAR_TITLE = 'ToolBar'

# Styles:
#   windows
#   fusion
#   windowsvista
appStyle = AppStyle.fusion


#                    C A M E R A                    #
# Classification names
b_sigatoka = 'Black Sigatoka'
y_sigatoka = 'Yellow Sigatoka'
class_names = [b_sigatoka, y_sigatoka] # alphabetical order

# Camera<Stream> image size
camera_scale = (
    640, # width
    480, # height
    QtCore.Qt.KeepAspectRatio # aspect ratio mode
)

# IMAGE_SIZE = (256, 256) # from tensor model
# IMAGE_SHAPE = (256, 256, 3)
IMAGE_SIZE = (224, 224) # from tensor model
IMAGE_SHAPE = (224, 224, 3)

# Output file name
imageName = 'capture'
f_extension = '.jpg'




#>_>_>_>_>_>_>_>_>_>_>_>_DEV: P R O J E C T  F I L E>_>_>_>_>_>_>_>_>_>_>_>_#
class Dev:
    pref_file = 'user-preferences.json'
    analytics_file = 'analytics.json'