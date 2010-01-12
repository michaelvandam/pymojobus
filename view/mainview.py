import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qrc_resources
from connectionview import SerialConnectionView

class DeviceWidgetItem(QListWidgetItem):

    def __init__(self, deviceView, parent=None):
        super(DeviceWidgetItem,self).__init__(parent)
        self.deviceView = deviceView
        self.name = self.deviceView.name
        self.setText(self.name)
    def getDevice(self):
        return self.deviceView
    
    device = property(getDevice)
    
class DeviceList(QListWidget):
    
    def __init__(self, devices = None ,parent=None):
        super(DeviceList,self).__init__(parent)
        self.devices = None
        
        if devices is not None:
            self.loadDevices(devices)
            
    def loadDevices(self,devices):
        self.clear()
        self.devices = devices
        for device in self.devices:
            widget = DeviceWidgetItem(device)
            self.addItem(widget)
        
class TabbedDeviceWidget(QTabWidget):
    
    def __init__(self, parent=None):
        super(TabbedDeviceWidget,self).__init__(parent)
        #self.setMovable(True)
    
    def loadDevices(self,devices):
        for device in devices:
            self.addTab(device, device.name)
    
class MainWindow(QMainWindow):
    
    def __init__(self, mojo=None, config=None, parent=None):
        super(MainWindow,self).__init__(parent)
        self.config=config
        self.mojo = mojo
        self.dockWidget = QDockWidget("Devices", self)
        self.dockWidget.setObjectName("DeviceDock")
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.deviceTabs = TabbedDeviceWidget()
        self.setCentralWidget(self.deviceTabs)
        self.deviceList = DeviceList()
        self.dockWidget.setWidget(self.deviceList)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
        
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready",5000)
        self.selectedModuleName = QLabel("None")
        self.selectedModuleName.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status.addPermanentWidget(self.selectedModuleName)
        self.setWindowTitle("ARC-P Modular Chemistry System")
        
        fileNewAction = self.createAction("&New", None, "Ctrl+N", None, "Create a new experiment")
        fileSaveAction = self.createAction("&Save", None, "Ctrl+S", None, "Save current experiment")
        fileSaveAsAction = self.createAction("S&ave As", None, None, None, "Save experiment as ...")
        fileQuitAction = self.createAction("&Quit", self.close, "Ctrl+Q", None, "Close the Application")
        moduleSearchAction = self.createAction("Sear&ch", self.searchForDevices, "Ctrl+H", None, "Search for devices")
        moduleClearAction = self.createAction("C&lear", self.clearDevices, "Ctrl+L", None, "Clear Modules")
        #moduleRefreshAction = self.createAction("&Refresh", None, "Ctrl+R", None, "Load module configuration")
        viewDeviceList = self.createAction("&View Device list", self.viewDeviceList, "Ctrl+D", None, "View Device List")
        connectionSetupAction = self.createAction("&Setup", self.configureSerial, None, None, "Setup connection ...")
        connectionConnectAction = self.createAction("&Connect", self.connectSerial, None, None, "Connect")
        connectionDisconnectAction = self.createAction("&Disconnect", self.disconnectSerial, None, None, "Disconnect")
        helpAboutAction = self.createAction("A&bout", self.helpAbout, "Ctrl+~", None, "About ...")
        helpHelpAction = self.createAction("&Help", None, "Ctrl+?", None, "Help ...")
        
        
        fileMenu = self.menuBar().addMenu("&File")
        moduleMenu = self.menuBar().addMenu("&Module")
        viewMenu = self.menuBar().addMenu("&View")
        connectionMenu = self.menuBar().addMenu("&Connection")
        helpMenu = self.menuBar().addMenu("&Help")
        
        self.addActions(fileMenu, (fileNewAction, fileSaveAction, fileSaveAsAction, fileQuitAction))
        self.addActions(moduleMenu, (moduleSearchAction, moduleClearAction))
        self.addActions(viewMenu, (viewDeviceList,))
        self.addActions(connectionMenu, (connectionSetupAction, connectionConnectAction, connectionDisconnectAction))
        self.addActions(helpMenu,(helpAboutAction, helpHelpAction))
        
        self.connect(self.deviceList, SIGNAL("clicked(QModelIndex)"), self.selectModule)
        
    
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
        
    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        
    def helpAbout(self):
        QMessageBox.about(self, "About ARC-P System",
                          """<b>ARC-P Modular Chemistry System</b>
                          <p> Copyright &copy; 2009 UC Regents
                          All Rights Reserved.
                          """)

    def selectModule(self):
        selecteDeviceWidgetItem = self.sender().currentItem()
        self.deviceTabs.setCurrentWidget(selecteDeviceWidgetItem.device)
    
    def loadDevices(self, devices):
        self.deviceTabs.loadDevices(devices)
        self.deviceList.loadDevices(devices)

    def viewDeviceList(self):
        self.dockWidget.show()

    def configureSerial(self):
        form = SerialConnectionView(self.config)
        if form.exec_():
            self.config.write()
    
    def connectSerial(self):
        self.mojo.makeConnection(self.config)

    def disconnectSerial(self):
        self.mojo.closeConnection()

    def searchForDevices(self):
        self.mojo.getDevices()
        devices = self.mojo.devices.values()
        self.mojo.getDeviceViews()
        self.loadDevices(self.mojo.deviceViews.values())

    def clearDevices(self):
        self.mojo.stopMonitor()
        self.deviceList.clear()
        self.deviceTabs.clear()
        
        
        
def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("UCLA Pharmacology")
    app.setOrganizationDomain("mednet.ucla.edu")
    app.setApplicationName("ARC-P Modular Chemistry System")
    devices = (PRMView(),RDMView(),CPMView())
    form = MainWindow()
    form.loadDevices(devices)
    form.show()
    app.exec_() 
    return form


if __name__=='__main__':
    form = main()
    