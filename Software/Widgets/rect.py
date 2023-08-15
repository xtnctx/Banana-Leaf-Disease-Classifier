from PyQt5 import QtWidgets, QtGui, QtCore

class ResizableRect(QtWidgets.QGraphicsRectItem):
    selected_edge = None
    def __init__(self, x, y, width, height, onCenter=False):
        # :param onCenter: "is simply an anchor point"
        if onCenter:
            super().__init__(-width / 2, -height / 2, width, height)
        else:
            super().__init__(0, 0, width, height)
        self.setPos(x, y)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 5))

        # a child item that shows the current position; note that this is only
        # provided for explanation purposes, a *proper* implementation should
        # use the ItemSendsGeometryChanges flag for *this* item and then
        # update the value within an itemChange() override that checks for
        # ItemPositionHasChanged changes.
        self.posItem = QtWidgets.QGraphicsSimpleTextItem(
            '{}, {}'.format(self.x(), self.y()), parent=self)
        self.posItem.setPos(
            self.boundingRect().x(), 
            self.boundingRect().y() - self.posItem.boundingRect().height()
        )

    def getEdges(self, pos):
        # return a proper Qt.Edges flag that reflects the possible edge(s) at
        # the given position; note that this only works properly as long as the
        # shape() override is consistent and for *pure* rectangle items; if you
        # are using other shapes (like QGraphicsEllipseItem) or items that have
        # a different boundingRect or different implementation of shape(), the
        # result might be unexpected.
        # Finally, a simple edges = 0 could suffice, but considering the new
        # support for Enums in PyQt6, it's usually better to use the empty flag
        # as default value.

        edges = QtCore.Qt.Edges()
        rect = self.rect()
        border = self.pen().width() / 2

        if pos.x() < rect.x() + border:
            edges |= QtCore.Qt.LeftEdge
        elif pos.x() > rect.right() - border:
            edges |= QtCore.Qt.RightEdge
        if pos.y() < rect.y() + border:
            edges |= QtCore.Qt.TopEdge
        elif pos.y() > rect.bottom() - border:
            edges |= QtCore.Qt.BottomEdge

        return edges

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.selected_edge = self.getEdges(event.pos())
            self.offset = QtCore.QPointF()
        else:
            self.selected_edge = QtCore.Qt.Edges()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selected_edge:
            mouse_delta = event.pos() - event.buttonDownPos(QtCore.Qt.LeftButton)
            rect = self.rect()
            pos_delta = QtCore.QPointF()
            border = self.pen().width()

            if self.selected_edge & QtCore.Qt.LeftEdge:
                # ensure that the width is *always* positive, otherwise limit
                # both the delta position and width, based on the border size
                diff = min(mouse_delta.x() - self.offset.x(), rect.width() - border)
                if rect.x() < 0:
                    offset = diff / 2
                    self.offset.setX(self.offset.x() + offset)
                    pos_delta.setX(offset)
                    rect.adjust(offset, 0, -offset, 0)
                else:
                    pos_delta.setX(diff)
                    rect.setWidth(rect.width() - diff)
            elif self.selected_edge & QtCore.Qt.RightEdge:
                if rect.x() < 0:
                    diff = max(mouse_delta.x() - self.offset.x(), border - rect.width())
                    offset = diff / 2
                    self.offset.setX(self.offset.x() + offset)
                    pos_delta.setX(offset)
                    rect.adjust(-offset, 0, offset, 0)
                else:
                    rect.setWidth(max(border, event.pos().x() - rect.x()))

            if self.selected_edge & QtCore.Qt.TopEdge:
                # similarly to what done for LeftEdge, but for the height
                diff = min(mouse_delta.y() - self.offset.y(), rect.height() - border)
                if rect.y() < 0:
                    offset = diff / 2
                    self.offset.setY(self.offset.y() + offset)
                    pos_delta.setY(offset)
                    rect.adjust(0, offset, 0, -offset)
                else:
                    pos_delta.setY(diff)
                    rect.setHeight(rect.height() - diff)
            elif self.selected_edge & QtCore.Qt.BottomEdge:
                if rect.y() < 0:
                    diff = max(mouse_delta.y() - self.offset.y(), border - rect.height())
                    offset = diff / 2
                    self.offset.setY(self.offset.y() + offset)
                    pos_delta.setY(offset)
                    rect.adjust(0, -offset, 0, offset)
                else:
                    rect.setHeight(max(border, event.pos().y() - rect.y()))

            if rect != self.rect():
                self.setRect(rect)
                if pos_delta:
                    self.setPos(self.pos() + pos_delta)
        else:
            # use the default implementation for ItemIsMovable
            super().mouseMoveEvent(event)

        self.posItem.setText('{},{} ({})'.format(
            self.x(), self.y(), self.rect().getRect()))
        self.posItem.setPos(
            self.boundingRect().x(), 
            self.boundingRect().y() - self.posItem.boundingRect().height()
        )

    def mouseReleaseEvent(self, event):
        self.selected_edge = QtCore.Qt.Edges()
        super().mouseReleaseEvent(event)

    def hoverMoveEvent(self, event):
        edges = self.getEdges(event.pos())
        if not edges:
            self.unsetCursor()
        elif edges in (QtCore.Qt.TopEdge | QtCore.Qt.LeftEdge, QtCore.Qt.BottomEdge | QtCore.Qt.RightEdge):
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif edges in (QtCore.Qt.BottomEdge | QtCore.Qt.LeftEdge, QtCore.Qt.TopEdge | QtCore.Qt.RightEdge):
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif edges in (QtCore.Qt.LeftEdge, QtCore.Qt.RightEdge):
            self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)