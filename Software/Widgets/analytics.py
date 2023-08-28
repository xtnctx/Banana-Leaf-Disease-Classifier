from PyQt5 import QtWidgets, QtGui, QtCore, QtChart
from Widgets.imagePreview import PreviewImage
from Utils import style
from Config import settings

class AnalyticsWindow(QtWidgets.QWidget):
    WIDTH = settings.ANALYTICS_WIDTH
    HEIGHT = settings.ANALYTICS_HEIGHT

    title = ''
    created = ''
    images = []
    image_count = 0
    blacksig = {}
    yellowsig = {}
    overall_confidence = 0.

    def __init__(self, data:dict):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout(self)

        self.title = data['title']
        self.created = data['created']
        self.images = data['images']
        self.image_count = data['image_count']
        self.blacksig = data['black_sigatoka']
        self.yellowsig = data['yellow_sigatoka']
        self.overall_confidence = data['overall_confidence']

        # TITLE & DATE
        titleFrame = QtWidgets.QFrame()
        titleLayout = QtWidgets.QVBoxLayout(titleFrame)
        titleLayout.setSpacing(0)
        titleLayout.setContentsMargins(0, 0, 0, 0)

        titleLabel = QtWidgets.QLabel(self.title)
        titleLabel.setFont(QtGui.QFont("Poppins", pointSize=12, weight=70))
        titleLayout.addWidget(titleLabel)

        dateLabel = QtWidgets.QLabel(', '.join(self.created.split(',')[1:3]))
        dateLabel.setToolTip(self.created)
        dateLabel.setFont(QtGui.QFont("Poppins", pointSize=8, weight=60))
        titleLayout.addWidget(dateLabel)

        # TOP-LEFT
        topleftFrame = QtWidgets.QFrame()
        topleftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        topleftLayout = QtWidgets.QVBoxLayout(topleftFrame)

        titleOverallLayout = QtWidgets.QVBoxLayout()
        titleOverallLayout.setSpacing(0)
        titleOverallLayout.setContentsMargins(0, 0, 0, 0)

        titleOverallLabel = QtWidgets.QLabel('Overall Confidence')
        titleOverallLabel.setFont(QtGui.QFont("Poppins Medium", pointSize=10, weight=60))
        titleOverallLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleOverallLayout.addWidget(titleOverallLabel)

        self.overallConfidenceLabel = QtWidgets.QLabel('{:.2f}%'.format(self.overall_confidence * 100))
        self.overallConfidenceLabel.setFont(QtGui.QFont("Poppins", pointSize=22, weight=75))
        self.overallConfidenceLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleOverallLayout.addWidget(self.overallConfidenceLabel)
        

        subTotalLayout = QtWidgets.QGridLayout()
        subTotalLayout.setContentsMargins(10, 0, 10, 0)
        subTotalFont = QtGui.QFont("Poppins Medium", pointSize=8, weight=60)

        yellowSigatokaTotalLabel = QtWidgets.QLabel(settings.y_sigatoka)
        yellowSigatokaTotalLabel.setFont(subTotalFont)
        subTotalLayout.addWidget(yellowSigatokaTotalLabel, 0, 0, 1, 1)

        if self.yellowsig.get('total_confidence') == None:
            self.yellowSigatokaTotalConfidence = QtWidgets.QLabel('--')
        else:
            self.yellowSigatokaTotalConfidence = QtWidgets.QLabel('{:.2f}%'.format(self.yellowsig['total_confidence'] * 100))
        self.yellowSigatokaTotalConfidence.setAlignment(QtCore.Qt.AlignCenter)
        self.yellowSigatokaTotalConfidence.setFont(subTotalFont)
        subTotalLayout.addWidget(self.yellowSigatokaTotalConfidence, 0, 1, 1, 3)


        blackSigatokaTotalLabel = QtWidgets.QLabel(settings.b_sigatoka)
        blackSigatokaTotalLabel.setFont(subTotalFont)
        subTotalLayout.addWidget(blackSigatokaTotalLabel, 1, 0, 1, 1)

        if self.blacksig.get('total_confidence') == None:
            self.blackSigatokaTotalConfidence = QtWidgets.QLabel('--')
        else:
            self.blackSigatokaTotalConfidence = QtWidgets.QLabel('{:.2f}%'.format(self.blacksig['total_confidence'] * 100))
        self.blackSigatokaTotalConfidence.setAlignment(QtCore.Qt.AlignCenter)
        self.blackSigatokaTotalConfidence.setFont(subTotalFont)
        subTotalLayout.addWidget(self.blackSigatokaTotalConfidence, 1, 1, 1, 3)

        topleftLayout.addLayout(titleOverallLayout)
        topleftLayout.addLayout(subTotalLayout)

        # BOTTOM-LEFT
        bottomleftFrame = QtWidgets.QFrame()
        bottomleftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        bottomleftLayout = QtWidgets.QVBoxLayout(bottomleftFrame)

        pieTitle = QtWidgets.QLabel('Detected Diseases')
        pieTitle.setAlignment(QtCore.Qt.AlignCenter)
        pieTitle.setFont(QtGui.QFont("Poppins Medium", pointSize=10, weight=60))

        self.pieSeries = QtChart.QPieSeries()
        if self.yellowsig.get('count') == None:
            self.pieSeries.append('Y', 0)
        else:
            self.pieSeries.append('Y', self.yellowsig['count'])

        if self.blacksig.get('count') == None:
            self.pieSeries.append('B', 0)
        else:
            self.pieSeries.append('B', self.blacksig['count'])
        self.pieSeries.setHoleSize(0.40)
        # pieSeries.setFont(QtGui.QFont("Poppins Medium", pointSize=7, weight=60))

        self.chart = QtChart.QChart()
        self.chart.addSeries(self.pieSeries)
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.chart.setContentsMargins(0, 0, 0, 0)
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setBackgroundRoundness(0)

        self.chart.legend().setAlignment(QtCore.Qt.AlignBottom)
        self.chart.legend().setFont(QtGui.QFont("Poppins Medium", pointSize=8, weight=60))
        

        self._chart_view = QtChart.QChartView(self.chart)
        self._chart_view.setAlignment(QtCore.Qt.AlignCenter)
        self._chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self._chart_view.setContentsMargins(0, 0, 0, 0)


        bottomleftLayout.addWidget(pieTitle)
        bottomleftLayout.addWidget(self._chart_view)

        

        # SPLITTER FOR TOP-LEFT & BOTTOM-LEFT
        splitterLeft = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitterLeft.addWidget(titleFrame)
        splitterLeft.addWidget(topleftFrame)
        splitterLeft.addWidget(bottomleftFrame)
        splitterLeft.setSizes([100, 400, 600])


        # RIGHT
        rightFrame = QtWidgets.QFrame()
        rightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        rightFrameLayout = QtWidgets.QVBoxLayout(rightFrame)

        self.table = ImagesResultTable(images=self.images)
        rightFrameLayout.addWidget(self.table)


        splitterRight = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitterRight.addWidget(splitterLeft)
        splitterRight.addWidget(rightFrame)
        splitterRight.setSizes([180, 600])

        vbox.addWidget(splitterRight)
        self.setLayout(vbox)

        # Center the window
        self.resize(self.WIDTH, self.HEIGHT)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class AlignDelegate(QtWidgets.QStyledItemDelegate): # Table.cell.alignCenter 
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter



class ImagesResultTable(QtWidgets.QTableWidget):
    COLUMNS = ['Image', 'Classification', 'Confidence']
    selected_item = () # row, column

    def __init__(self, images:list):
        super().__init__()

        # keys: ['id', 'path', 'classification', 'confidence', 'shape', 'type', 'created', 'modified']
        self.images:list[dict] = images

        self.setGeometry(QtCore.QRect(10, 27, 432, 251))
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSortIndicatorShown(False)

        font = QtGui.QFont("Poppins", pointSize=9, weight=50)
        self.setFont(font)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False) # Row Index
        self.setFocusPolicy(QtCore.Qt.FocusPolicy(False)) # Cell Highlighting
        self.horizontalHeader().setStyleSheet('QHeaderView::section { border: none; border-bottom: 2px solid green;}')
        self.setStyleSheet(style.table)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.cellClicked.connect(self.cell_item_clicked)

        self.setAutoScroll(True)
        self.setAlternatingRowColors(True)
        self.setColumnCount(len(self.COLUMNS))
        self.setRowCount(0)
        self.setupColumns()
        self.loadRows(images=self.images)

        # Item Context Menu
        self.contextMenu = QtWidgets.QMenu(self)
        self.save_controls = self.contextMenu.addAction("Id")
        self.defisheye = self.contextMenu.addAction("Path")
        self.stopRecorder = self.contextMenu.addAction("Date created")

    def cell_item_clicked(self, row, column):
        self.selected_item = (row, column)

        if column == 0:
            self.second_ui = PreviewImage(QtGui.QPixmap(self.images[row]['path']))
        # print("Row %d and Column %d was clicked" % (row, column))
    

    def setupColumns(self):
        font = QtGui.QFont("Poppins Medium", pointSize=7, weight=75)
        for i, c in enumerate(self.COLUMNS):
            item = QtWidgets.QTableWidgetItem(c)
            item.setFont(font)
            self.setHorizontalHeaderItem(i, item)
            self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            self.setItemDelegateForColumn(i, AlignDelegate(self))
        self.verticalHeader().setDefaultSectionSize(44)
    
    def loadRows(self, images:list):
        images:list[dict] = images
        row_count = len(images)
        self.setRowCount(row_count)

        for row in range(row_count):
            print(images[row]['path'])
            image = QtWidgets.QTableWidgetItem(str(row+1))
            image.setToolTip(
            """
                <ul style='margin: 0px; padding: 0px; list-style: none;'> 
                    <li style='margin-bottom: 0.5em;'> <b>id:</b> {id}</li> 
                    <li style='margin-bottom: 0.5em;'> <b>path:</b> {path}</li> 
                    <li style='margin-bottom: 0.5em;'> <b>tensor_shape:</b> {width} x {height}</li> 
                    <li style='margin-bottom: 0.5em;'> <b>created:</b> {created}</li> 
                </ul> 
            """.format(
                    id=images[row]['id'],
                    path=images[row]['path'],
                    width=images[row]['tensor_shape'][0],
                    height=images[row]['tensor_shape'][1],
                    created=images[row]['created']
                )
            )
 
            self.setItem(row, 0, image)
            self.setItem(row, 1, QtWidgets.QTableWidgetItem(images[row]['classification']))
            self.setItem(row, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(images[row]['confidence']*100)))