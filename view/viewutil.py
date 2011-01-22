# Make widgets clickable.
# Borrowed from: http://diotavelli.net/PyQtWiki/Making%20non-clickable%20widgets%20clickable

from PyQt4.QtCore import *
from PyQt4.QtGui import *

def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    self.clicked.emit()
                    return True
                    
            return False
            
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
 