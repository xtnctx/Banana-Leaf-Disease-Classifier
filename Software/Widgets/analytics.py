from PyQt5 import QtWidgets, QtGui, QtCore

class Analytics(QtWidgets.QWidget):
    WIDTH = 900
    HEIGHT = 500

    def __init__(self):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout(self)

        # TITLE & DATE
        titleFrame = QtWidgets.QFrame()
        titleLayout = QtWidgets.QVBoxLayout(titleFrame)
        titleLayout.setSpacing(0)
        titleLayout.setContentsMargins(0, 0, 0, 0)

        titleLabel = QtWidgets.QLabel('Analytics')
        titleLabel.setFont(QtGui.QFont("Poppins", pointSize=16, weight=70))
        titleLayout.addWidget(titleLabel)

        dateLabel = QtWidgets.QLabel('April 20, 2023')
        dateLabel.setFont(QtGui.QFont("Poppins", pointSize=9, weight=60))
        titleLayout.addWidget(dateLabel)

        # TOP-LEFT
        topleftFrame = QtWidgets.QFrame()
        topleftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        topleftLayout = QtWidgets.QVBoxLayout(topleftFrame)

        test1 = QtWidgets.QLabel('Test1')
        topleftLayout.addWidget(test1)

        # BOTTOM-LEFT
        bottomleftFrame = QtWidgets.QFrame()
        bottomleftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        bottomleftLayout = QtWidgets.QVBoxLayout(bottomleftFrame)

        test2 = QtWidgets.QLabel('Test2')
        bottomleftLayout.addWidget(test2)

        # SPLITTER FOR TOP-LEFT & BOTTOM-LEFT
        splitterLeft = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitterLeft.addWidget(titleFrame)
        splitterLeft.addWidget(topleftFrame)
        splitterLeft.addWidget(bottomleftFrame)
        splitterLeft.setSizes([100, 500, 500])


        # RIGHT
        rightFrame = QtWidgets.QFrame()
        rightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        rightFrameLayout = QtWidgets.QVBoxLayout(rightFrame)

        self.table = ImagesResultTable()
        rightFrameLayout.addWidget(self.table)


        splitterRight = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitterRight.addWidget(splitterLeft)
        splitterRight.addWidget(rightFrame)
        splitterRight.setSizes([250, 600])

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

    def __init__(self):
        super().__init__()

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
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.setAutoScroll(True)
        self.setAlternatingRowColors(True)
        self.setObjectName("table")
        self.setColumnCount(len(self.COLUMNS))
        self.setRowCount(0)

        self.setupColumns()


    def setupColumns(self):
        font = QtGui.QFont("Poppins Medium", pointSize=8, weight=75)
        for i, c in enumerate(self.COLUMNS):
            item = QtWidgets.QTableWidgetItem(c)
            item.setFont(font)
            self.setHorizontalHeaderItem(i, item)
            self.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            self.setItemDelegateForColumn(i, AlignDelegate(self))
        self.verticalHeader().setDefaultSectionSize(44)
        