import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from utils.mojodeviceview import DeviceView


        
class CPMView(DeviceView):
    deviceType = "CPM"
    def __init__(self, cpmModel=None, parent=None, *args, **kwargs):
        DeviceView.__init__(self, parent=parent, deviceModel=cpmModel)            
        
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        
        #Fill Buttons
        self.fillGroup = QGroupBox("Fill")
        fillLayout = QHBoxLayout()
        self.fillButton = QPushButton("Fill")
        self.buttonGroup.addButton(self.fillButton)
        self.fillButton.setCheckable(True)
        self.fillButton.setAutoExclusive(True)
        self.fillDoneButton = QPushButton("Done")
        self.buttonGroup.addButton(self.fillDoneButton)
        self.fillDoneButton.setCheckable(True)
        self.fillDoneButton.setAutoExclusive(True)
        fillLayout.addWidget(self.fillButton)
        fillLayout.addWidget(self.fillDoneButton)
        self.fillGroup.setLayout(fillLayout)
        
        #Trap Buttons
        self.trapGroup = QGroupBox("Trap")
        trapLayout = QHBoxLayout()
        self.trapButton = QPushButton("Trap")
        self.buttonGroup.addButton(self.trapButton)
        self.trapButton.setCheckable(True)
        self.trapButton.setAutoExclusive(True)
        self.trapDoneButton = QPushButton("Done")
        self.buttonGroup.addButton(self.trapDoneButton)
        self.trapDoneButton.setCheckable(True)
        self.trapDoneButton.setAutoExclusive(True)
        trapLayout.addWidget(self.trapButton)
        trapLayout.addWidget(self.trapDoneButton)
        self.trapGroup.setLayout(trapLayout)
        
        #Wash Buttons
        self.washGroup = QGroupBox("Wash")
        washLayout = QHBoxLayout()
        self.washButton = QPushButton("Wash")
        self.buttonGroup.addButton(self.washButton)
        self.washButton.setCheckable(True)
        self.washButton.setAutoExclusive(True)
        self.washDoneButton = QPushButton("Done")
        self.buttonGroup.addButton(self.washDoneButton)
        self.washDoneButton.setCheckable(True)
        self.washDoneButton.setAutoExclusive(True)
        washLayout.addWidget(self.washButton)
        washLayout.addWidget(self.washDoneButton)
        self.washGroup.setLayout(washLayout)

        #Elute Buttons
        self.eluteGroup = QGroupBox("Elute")
        eluteLayout = QHBoxLayout()
        self.eluteButton = QPushButton("Elute")
        self.buttonGroup.addButton(self.eluteButton)
        self.eluteButton.setCheckable(True)
        self.eluteButton.setAutoExclusive(True)
        self.eluteDoneButton = QPushButton("Done")
        self.buttonGroup.addButton(self.eluteDoneButton)
        self.eluteDoneButton.setCheckable(True)
        self.eluteDoneButton.setAutoExclusive(True)
        eluteLayout.addWidget(self.eluteButton)
        eluteLayout.addWidget(self.eluteDoneButton)
        self.eluteGroup.setLayout(eluteLayout)
        
        layout = QGridLayout()
        layout.addWidget(self.fillGroup, 0, 0)
        layout.addWidget(self.trapGroup, 1, 0)
        layout.addWidget(self.washGroup, 2, 0)
        layout.addWidget(self.eluteGroup, 3, 0)

        self.setLayout(layout)


def main(argv):
    pass
            
if __name__ == '__main__':
    main(sys.argv)
    app = QApplication([])
    form = CPMView()
    form.show()
    app.exec_()