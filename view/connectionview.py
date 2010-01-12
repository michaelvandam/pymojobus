import os
import sys
import copy
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SerialConnectionView(QDialog):
    
    def __init__(self, config=None, parent=None):
        
        if config is None:
            self.config ={'SerialSettings':{'port':0,
              'baudrate':9600,
              'bytesize':8,
              'parity':'N',
              'stopbits':0}}
        else:
            self.config=config

        super(SerialConnectionView,self).__init__(parent)
        self.serialconfig = self.config["SerialSettings"]
        self.comport = self.serialconfig['port']
        self.baudrate =  self.serialconfig['baudrate']
        self.bytesize = self.serialconfig['bytesize']
        self.parity = self.serialconfig['parity']
        self.stopbits = self.serialconfig['stopbits']
        layout = QGridLayout()
        
        # PORT 
        self.portOpts = ["COM%d" % i for i in range(1,13)]
        portLabel = QLabel("&Port")
        self.portComboBox = QComboBox()
        portLabel.setBuddy(self.portComboBox)
        self.portComboBox.addItems(self.portOpts)
        self.portComboBox.setCurrentIndex(self.serialconfig['port'])
        
        # BAUDRATE
        self.baudOpts = [100, 300, 600, 1200, 2400,
                         4800, 9600, 14400, 19200, 
                         38400, 57600, 115200, 128000,
                         256000]
        baudoptstrs = [str(i) for i in self.baudOpts]
        baudLabel = QLabel("&Baudrate")
        self.baudrateComboBox = QComboBox()
        baudLabel.setBuddy(self.baudrateComboBox)
        self.baudrateComboBox.addItems(baudoptstrs)
        self.baudrateComboBox.setCurrentIndex(
                        self.baudOpts.index(self.serialconfig['baudrate']))
        
        # BYTESIZE
        self.byteszOpts = [5,6,7,8]
        byteszoptstr = [str(i) for i in self.byteszOpts]
        byteszLabel = QLabel("B&ytesize")
        self.byteszComboBox = QComboBox()
        byteszLabel.setBuddy(self.byteszComboBox)
        self.byteszComboBox.addItems(byteszoptstr)
        self.byteszComboBox.setCurrentIndex(
                        self.byteszOpts.index(self.serialconfig['bytesize']))
                        
        
        # PARITY
        self.parityOpts = ['None','Even', 'Odd']
        parityLabel = QLabel("Pa&rity")
        self.parityComboBox = QComboBox()
        parityLabel.setBuddy(self.parityComboBox)
        self.parityComboBox.addItems(self.parityOpts)
        for opt in self.parityOpts:
            if opt[0] == self.serialconfig['parity']:
                break
        self.parityComboBox.setCurrentIndex(self.parityOpts.index(opt))
        
        # STOPBITS    
        self.stopBitOpts=[0,1]
        stopbitoptstr = [str(i) for i in self.stopBitOpts]
        
        stopbitsLabel = QLabel("St&opbits")
        self.stopbitsComboBox = QComboBox()
        stopbitsLabel.setBuddy(self.stopbitsComboBox)
        self.stopbitsComboBox.addItems(stopbitoptstr)
        self.stopbitsComboBox.setCurrentIndex(self.stopBitOpts.index(self.serialconfig['stopbits']))
        
        # OK / CANCEL
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                    QDialogButtonBox.Cancel)
        
        
        
        # LAYOUT        
        layout.addWidget(portLabel, 0,0)
        layout.addWidget(self.portComboBox, 0,1)
        layout.addWidget(baudLabel,1,0)
        layout.addWidget(self.baudrateComboBox,1,1)
        layout.addWidget(byteszLabel,2,0)
        layout.addWidget(self.byteszComboBox,2,1)
        layout.addWidget(parityLabel,3,0)
        layout.addWidget(self.parityComboBox, 3,1)
        layout.addWidget(stopbitsLabel, 4, 0)
        layout.addWidget(self.stopbitsComboBox, 4, 1)
        layout.addWidget(buttonBox, 5,1)
        self.setLayout(layout)
        
        self.setWindowTitle("Serial Port Settings")

        self.connect(buttonBox, SIGNAL("accepted()"), self.connectSerial)
        self.connect(buttonBox, SIGNAL("rejected()"),self, SLOT("reject()"))
        
    def connectSerial(self):
        self.serialconfig['port'] = self.portComboBox.currentIndex()
        self.serialconfig['baudrate'] =  self.baudOpts[self.baudrateComboBox.currentIndex()]
        self.serialconfig['bytesize'] = self.byteszOpts[self.byteszComboBox.currentIndex()]
        self.serialconfig['parity'] = self.parityOpts[self.parityComboBox.currentIndex()][0]
        self.serialconfig['stopbits'] = self.stopBitOpts[self.stopbitsComboBox.currentIndex()]
        self.emit(SIGNAL("accepted()"))
        QDialog.accept(self)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = SerialConnectionView()
    form.show()
    app.exec_()