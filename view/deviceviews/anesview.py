import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from utils.mojodeviceview import DeviceView
import logging
        
errlog = logging.getLogger("mojo.error")
log = logging.getLogger()

class ANESView(DeviceView):
    deviceType = "ANES"
    MAX = 1000
    
    def __init__(self, anesModel=None, parent=None, *args, **kwargs):
        DeviceView.__init__(self, parent=parent, deviceModel=anesModel)            
        
        
        #anes Controls
        anesGroup = QGroupBox("Anesthesia")
        #anesGroup.setCheckable(True)
        anesLayout = QHBoxLayout()
        anesGroup.setLayout(anesLayout)
        anesDial = QDial()
        anesDial.setNotchesVisible(True)
        anesDial.setNotchTarget(50)
        self.anesSpeedSpinBox= QSpinBox()
        self.anesSpeedSpinBox.setSuffix("sccm")
        anesDial.setRange(0,self.MAX)
        self.anesSpeedSpinBox.setRange(0,self.MAX)
        anesLayout.addWidget(anesDial)
        anesLayout.addWidget(self.anesSpeedSpinBox)
        self.connect(anesDial, SIGNAL('valueChanged(int)'), self.anesSpeedSpinBox.setValue)
        self.connect(self.anesSpeedSpinBox, SIGNAL('valueChanged(int)'), anesDial.setValue)

        
        
        #ox Controls
        oxGroup = QGroupBox("Oxygen")
        #oxGroup.setCheckable(True)
        oxLayout = QHBoxLayout()
        oxGroup.setLayout(oxLayout)
        oxDial = QDial()
        oxDial.setNotchesVisible(True)
        oxDial.setNotchTarget(50)
        self.oxSpeedSpinBox = QSpinBox()
        self.oxSpeedSpinBox.setSuffix("sccm")
        oxDial.setRange(0,self.MAX)
        self.oxSpeedSpinBox.setRange(0,self.MAX)
        oxLayout.addWidget(oxDial)
        oxLayout.addWidget(self.oxSpeedSpinBox)
        self.connect(oxDial, SIGNAL('valueChanged(int)'), self.oxSpeedSpinBox.setValue)
        self.connect(self.oxSpeedSpinBox, SIGNAL('valueChanged(int)'), oxDial.setValue)
        
        flowLayout = QGridLayout()
        flowGroup = QGroupBox("Flow Rates")
        flowGroup.setLayout(flowLayout)
        oxLabel = QLabel("Oxygen")
        anesLabel = QLabel("Anesthesia")
        self.oxFlowValue = QLabel("0")
        self.anesFlowValue = QLabel("0")
        flowLayout.addWidget(oxLabel, 0,0)
        flowLayout.addWidget(self.oxFlowValue, 1,0)
        flowLayout.addWidget(anesLabel, 0,1)
        flowLayout.addWidget(self.anesFlowValue, 1,1)
        
        
        setLayout = QGridLayout()
        setGroup = QGroupBox("Set Points")
        setGroup.setLayout(setLayout)
        setOxLabel = QLabel("Oxygen")
        setAnesLabel = QLabel("Anesthesia")
        self.setOxFlowValue = QLabel("0")
        self.setAnesFlowValue = QLabel("0")
        setLayout.addWidget(setOxLabel, 0,0)
        setLayout.addWidget(self.setOxFlowValue, 1,0)
        setLayout.addWidget(setAnesLabel, 0,1)
        setLayout.addWidget(self.setAnesFlowValue, 1,1)
        
        
        maxLayout = QGridLayout()
        maxGroup = QGroupBox("Percentage")
        #maxGroup.setCheckable(True)
        #maxGroup.setChecked(False)
        maxGroup.setLayout(maxLayout)
        maxLabel = QLabel("Max Flowrate")
        self.maxValue = QLabel()
        perAnesLabel = QLabel("Percent Anesthesia")
        self.perAnesValue = QLabel()
        self.perDial = QDial()
        self.perDial.setNotchesVisible(True)
        self.perDial.setNotchTarget(25)
        self.perDial.setRange(0,100)
        
        
        maxLayout.addWidget(self.perDial)
        maxLayout.addWidget(maxLabel,0,0)
        maxLayout.addWidget(self.maxValue, 1,0)
        maxLayout.addWidget(perAnesLabel, 0,1)
        maxLayout.addWidget(self.perAnesValue, 1,1)
        maxLayout.addWidget(self.perDial, 2,0,1,2)


        resetButton = QPushButton("Reset")
        
        
        
        layout = QGridLayout()
        layout.addWidget(oxGroup,0,0)
        layout.addWidget(anesGroup,0,1)
        layout.addWidget(flowGroup,1,0)
        layout.addWidget(setGroup,1,1)
        layout.addWidget(maxGroup,2,0)
        layout.addWidget(resetButton,3,0)
        self.setLayout(layout)
        self.connect(oxDial, SIGNAL("valueChanged(int)"), self.setOx)
        self.connect(anesDial, SIGNAL("valueChanged(int)"), self.setAnes)
        self.connect(resetButton, SIGNAL("clicked()"), self.reset)
        self.connect(self.perDial, SIGNAL('valueChanged(int)'), self.setPerAnes)
        
    def setMax(self):
        pass
    
    def setPerAnes(self):
        self.model.perAnes = self.perDial.value()
    
    def reset(self):
        self.model.goReset()
    
    
    def setOx(self):
        log.debug("Set Oxygen %d" % self.oxSpeedSpinBox.value())
        self.model.oxLevel = self.oxSpeedSpinBox.value()
        
        
    
    def setAnes(self):
        log.debug("Set Anesthesia %d" % self.anesSpeedSpinBox.value())
        self.model.anesLevel = self.anesSpeedSpinBox.value()
        
        
    
    def updateView(self):
        log.debug("Update view %s" % self.model.name)
        self.anesFlowValue.setText(self.model.anesActualFlow)
        self.oxFlowValue.setText(self.model.oxActualFlow)
        self.setAnesFlowValue.setText(self.model.anesSetFlow)
        self.setOxFlowValue.setText(self.model.oxSetFlow)
        self.oxSpeedSpinBox.setValue(self.model.oxLevel)
        self.anesSpeedSpinBox.setValue(self.model.anesLevel)
        self.maxValue.setText("%d sccm" % self.model.maxLevel)
        self.perAnesValue.setText("%4.2f %%" % self.model.perAnes)

def main(argv):
    pass
            
if __name__ == '__main__':
    main(sys.argv)
    app = QApplication([])
    form = ANESView()
    form.show()
    app.exec_()