
###
# Author: Ramin Shirani
#
# Thanks to https://stackoverflow.com/
###
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient
from PyQt5.QtWidgets import QWidget

class VerticalGauge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0.0
        self._minimum = 0.0
        self._maximum = 1.0
        self.min = 0
        self.max = 1
        self.green_line = 0.5

    def setMinMax(self, value):
        ab = value[1] - value[0]
        self._minimum = 0
        self._maximum = ab
        self.min = value[0]
        self.max = value[1]
    def setGreenLine(self, value):
        self.green_line = value
    def setValue(self, value):
        if value > self.max:
            value = self._maximum
        elif value < self.min:
            value = self._maximum
        else:
            value = value - self.min
        self._value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        rect = QRectF(0, 0, self.width(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRect(rect)

        # Draw gauge
        gauge_rect = QRectF(0, 0, self.width(), self.height())
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        gauge_rect.setWidth(self.width())
        painter.drawRect(gauge_rect)

        # Draw degree markers
        marker_width = gauge_rect.width() - (gauge_rect.width()/2)
        marker_height = 2
        marker_count = int(self._maximum - self._minimum)
        marker_spacing = gauge_rect.height()//marker_count
        small_marker_spacing = marker_spacing/2
        num_list = [i for i in range(self.min,self.max+1)]
        num_list.reverse()
        for i in range(marker_count):
            if i  == 0:
                continue
            y = gauge_rect.y() + (i) * marker_spacing
            x = gauge_rect.width()/4
            painter.drawRect(x, y, marker_width, marker_height)
            t = QPointF(x-20,y+5)
            painter.drawText(t,str(num_list[i]))
        for i in range((marker_count*2)):
            if i == 0 or i%2 == 0:
                continue
            y = gauge_rect.y() + (i) * small_marker_spacing
            x = gauge_rect.width()/4
            painter.drawRect(x*1.5, y, marker_width/2, marker_height/2)
        
        # Draw progress bar
        progress_bar_rect = QRectF(
                gauge_rect.x() + (gauge_rect.width()/2 - ((gauge_rect.width()/6))/2),
                gauge_rect.y() + ((self._maximum - self._value) * gauge_rect.height())/self._maximum,
                gauge_rect.width()/6,
                (self._value * (gauge_rect.height()))
            )
        painter.setPen(Qt.NoPen)
        gradiant = QLinearGradient(QPointF(gauge_rect.width()/2, 0), QPointF(gauge_rect.width()/2, ((self.max - self.green_line)*gauge_rect.height())/self._maximum))
        gradiant.setColorAt(1,QColor(8,194,24))
        gradiant.setColorAt(0,QColor(8,85,194))
        painter.setBrush(QBrush(gradiant))
        painter.drawRect(progress_bar_rect)

        #Draw Green Line
        painter.setPen(QPen(QColor(0, 191, 22)))
        green_line = (self.max - self.green_line)
        y = (green_line*gauge_rect.height())/self._maximum
        p1 = QPointF(0,y)
        p2 = QPointF(gauge_rect.width(),y)
        l = QLineF(p1,p2)
        painter.drawLine(l)

