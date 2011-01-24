
# TODO:
# - Cleanup: be careful with parent/child relationships for view elements

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from connectionview import SerialConnectionView
from operationsview import OperationsView
from systemstateview import SystemStateView
        
class MainWindow(QMainWindow):

    """ Main application window
    @ivar config            obj     Application config info
    @ivar mojo              obj     Mojo object associated with application
    @ivar devices           dict    Dictionary of devices in system
                                    (indexed by address)
    @ivar activeDevice      str     Address of active device (or None)
    @ivar activeOperation   obj     Active operation (or None)
    @ivar selectedDevice    str     Address of selected device (or None)
    @ivar status            str     String representing system state
    @ivar systemView        obj     Sub-view of system state
    @ivar operationsView    obj     Sub-view of device operations
    """
    
    def __init__(self, mojo=None, config=None, parent=None):
        QMainWindow.__init__(self)
        self.config=config
        self.mojo = mojo
        self.devices = {}
        self.activeDevice = None
        self.activeOperation = None
        self.selectedDevice = None
        self.status = "Ready"

        # Dummy widget (required by PyQt)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        
        mainLayout = QVBoxLayout(centralWidget)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready",5000)
        self.setWindowTitle("ARC-P Modular Chemistry System")
        
        # System state view (containing device icons)
        self.systemView = SystemStateView()
        mainLayout.addWidget(self.systemView)
        self.connect(self.systemView, SIGNAL("deviceSelected(PyQt_PyObject)"), self.setSelectedDevice)
        self.connect(self, SIGNAL("statusChanged(PyQt_PyObject)"), self.systemView.slotStatusChanged)
        
        # Operations view
        self.operationsView = OperationsView()
        mainLayout.addWidget(self.operationsView)
        self.connect(self.operationsView, SIGNAL("startOperation(PyQt_PyObject)"), self.slotStartOperation)

        # Timer to periodically check completion of threads (i.e. for unit operations)
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL('timeout()'), self.slotCheckThreadCompletion)
        interval = 0.1 * 1000  # milliseconds
        self.timer.start(interval)
        
        # Define Menus

        fileMenu = self.menuBar().addMenu("&File")
        viewMenu = self.menuBar().addMenu("&View")
        connectionMenu = self.menuBar().addMenu("&Connection")
        helpMenu = self.menuBar().addMenu("&Help")
        
        # File Menu actions
        fileQuitAction = self.createAction("&Quit", self.close, "Ctrl+Q", None, "Close the Application")
        self.addActions(fileMenu, (fileQuitAction,))
        
        # Connection Menu actions
        connectionSetupAction = self.createAction("&Setup", self.configureSerial, None, None, "Setup connection ...")
        connectionConnectAction = self.createAction("&Connect", self.connectSerial, None, None, "Connect")
        connectionDisconnectAction = self.createAction("&Disconnect", self.disconnectSerial, None, None, "Disconnect")
        connectionScanModules = self.createAction("&Scan Modules", self.scanDevices, None, None, "Scan devices")
        connectionClearModules = self.createAction("&Clear Modules", self.clearDevices, None, None, "Clear device list")
        self.addActions(connectionMenu,(connectionSetupAction, connectionConnectAction, connectionDisconnectAction, connectionScanModules, connectionClearModules))
        
        # Help Menu actions
        helpAboutAction = self.createAction("A&bout", self.helpAbout, "Ctrl+~", None, "About ...")
        helpHelpAction = self.createAction("&Help", self.helpHelp, "Ctrl+?", None, "Help ...")
        self.addActions(helpMenu,(helpAboutAction, helpHelpAction))
        

    
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

    # Menu handlers
    
    def helpAbout(self):
        QMessageBox.about(self, "About ARC-P Software",
                          """<b>ARC-P Modular Chemistry System Controller</b>
                          <p> Copyright &copy; 2009-2011 UC Regents
                          All Rights Reserved.
                          """)
                          
    def helpHelp(self):
        QMessageBox.about(self, "Help", "Help not yet available in this version.")
    
    def configureSerial(self):
        form = SerialConnectionView(self.config)
        if form.exec_():
            self.config.write()
    
    def connectSerial(self):
        self.mojo.makeConnection(self.config)

    def disconnectSerial(self):
        self.mojo.closeConnection()

    def scanDevices(self):
        self.clearDevices()
        # Query for devices
        # Tempory Disable:
        # self.devices = self.mojo.getDevices()
        self.devices = {'a':{'deviceType':'RDM', 'address':'a'}, 'b':{'deviceType':'PRM', 'address':'b'}, 'c':{'deviceType':'PRM', 'address':'c'}}
        self.systemView.loadDevices(self.devices)
        self.operationsView.loadDevices(self.devices)

    def clearDevices(self):
        #self.mojo.stopMonitor()
        self.systemView.clearDevices()
        self.operationsView.clearDevices()
        self.devices.clear()
        self.activeDevice = None

    # Signal handlers
    
    def slotOperationStarted(self, operation):
        if self.activeOperation != None:
            # TODO: Raise exception
            print "ERROR(MainWindow): starting operation while operation is active"
        self.activeOperation = operation
        self.activeDevice = operation.device['address']
        self.systemView.slotOperationStarted(operation)
        self.operationsView.slotOperationStarted(operation)

    def slotOperationFinished(self, operation):
        if self.activeOperation != operation:
            # TODO: Raise exception
            print "ERROR(MainWindow): finished operation != started operation"
        self.systemView.slotOperationFinished(operation)
        self.operationsView.slotOperationFinished(operation)
        self.activeDevice = None
        self.activeOperation = None

    def setSelectedDevice(self, address=None):
        #if self.selectedDevice != address: # Removed to always force redraw
            self.selectedDevice = address
            self.systemView.setSelectedDevice(address)
            self.operationsView.setSelectedDevice(address)

    def slotCheckThreadCompletion(self):
        if self.activeOperation != None:
            msg = self.activeOperation.statusMessage
            # Check for updated status
            # TODO: think about how to do this with SIGNALs instead?
            if self.status != msg:
                self.status = msg
                self.emit(SIGNAL('statusChanged(PyQt_PyObject)'), self.status)
            if self.activeOperation.complete:
                self.endOperation(self.activeOperation)
        
    def slotStartOperation(self, operation):
        """ Begin executing a thread corresponding to a unit operation.
            Signaled from operationsView or sequenceView
        """
        abortInterval = 0.1     # Desired interval (seconds) that operation should check for abort
        if operation.execute(abortInterval):
            self.slotOperationStarted(operation)

    def endOperation(self, operation):
        operation.finish()
        self.slotOperationFinished(operation)
        self.status = "Ready"
        self.emit(SIGNAL('statusChanged(PyQt_PyObject)'), self.status)

        
        
def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("UCLA Crump Institute for Molecular Imaging")
    app.setOrganizationDomain("mednet.ucla.edu")
    app.setApplicationName("ARC-P Modular Chemistry System Controller")
    form = MainWindow()
    form.show()
    app.exec_() 
    return form


if __name__=='__main__':
    form = main()
    
