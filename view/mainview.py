
# TODO:
# - Cleanup: be careful with parent/child relationships for view elements

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from connectionview import SerialConnectionView
from operationsview import OperationsView
from systemstateview import SystemStateView
        
from operation.unitoperation import WrapperThread

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
    @ivar workerThread      obj     Thread to manage a unit operation
    @ivar worker            obj     Object that actually performs the unit operation
    @ivar threadRunning     bool    True if unit operation thread is running
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
        
        # Abort button
        # Keep disabled unless inside a unit operation
        self.abortButton = QPushButton("Abort")
        self.abortButton.setEnabled(False)
        mainLayout.addWidget(self.abortButton)
        self.connect(self.abortButton, SIGNAL("clicked()"), self._slotAbortThread)
        
        # Operations view
        self.operationsView = OperationsView()
        mainLayout.addWidget(self.operationsView)
        self.connect(self.operationsView, SIGNAL("startOperation(PyQt_PyObject)"), self.slotStartOperation)

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
        self.devices = self.mojo.getDevices()
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
        self.abortButton.setEnabled(True)
        self.activeOperation = operation
        self.activeDevice = operation.device.address
        self.systemView.slotOperationStarted(operation)
        self.operationsView.slotOperationStarted(operation)

    def slotOperationFinished(self, operation):
        if self.activeOperation != operation:
            # TODO: Raise exception
            print "ERROR(MainWindow): finished operation != started operation"
        self.abortButton.setEnabled(False)
        self.systemView.slotOperationFinished(operation)
        self.operationsView.slotOperationFinished(operation)
        self.activeDevice = None
        self.activeOperation = None

    def setSelectedDevice(self, address=None):
        #if self.selectedDevice != address: # Removed to always force redraw
            self.selectedDevice = address
            self.systemView.setSelectedDevice(address)
            self.operationsView.setSelectedDevice(address)

    def _slotAbortThread(self):
        if self.threadRunning:
            print "MainWindow: sending ABORT signal"
            self.emit(SIGNAL('abortRequest()'))
                
    def slotAbortAck(self):
        """ Public slot for signal from thread acknowledging ready to abort.
            When received, terminate thread.  Cleanup of GUI occurs when thread
            emits 'terminated()' signal.
            """
        self.workerThread.terminate()
        
    def slotStartOperation(self, operation):
        """ Begin executing a thread corresponding to a unit operation.
            Signaled from operationsView or sequenceView
        """
        self.slotOperationStarted(operation)
        pollInterval = 100     # Desired interval (msec) that operation should check for abort
        self.worker = operation.getThread(pollInterval)
        self.workerThread = WrapperThread()
        self.worker.moveToThread(self.workerThread)
        # Connect thread-level signals and slots
        self.workerThread.started.connect(self.worker.run)
        self.workerThread.finished.connect(self.slotThreadFinished)
        self.workerThread.terminated.connect(self.slotThreadTerminated)  # seems unneeded; finished() also called on termination
        # Connect worker-level signals and slots
        self.worker.connect(self.worker, SIGNAL('status(PyQt_PyObject)'), self.slotThreadStatusChanged)
        self.worker.connect(self.worker, SIGNAL('requestInput(PyQt_PyObject)'), self.slotThreadInputRequest)
        self.worker.connect(self, SIGNAL('abortRequest()'), self.worker.slotAbort)
        self.worker.connect(self.worker, SIGNAL('abortAck()'), self.slotAbortAck)
        self.worker.connect(self, SIGNAL('inputReceived()'), self.worker.slotInputReceived)
        self.threadRunning = True
        self.workerThread.start()

    def slotThreadInputRequest(self, message):
        print "MainWindow: INPUTREQUEST"
        self.popup = QMessageBox()
        self.popup.setWindowTitle("ARC-P Modular Chemistry System Controller")
        self.popup.setText(message + "  Press OK to continue.")
        self.popup.connect(self.popup, SIGNAL('finished(int)'), self._slotPopupClosed)
        self.popup.show()

    def _slotPopupClosed(self, returnval):
        # Send signal to the thread that input was received
        # TODO: we may want to send data with this signal in the general case
        self.emit(SIGNAL('inputReceived()'))
    
    def slotThreadStatusChanged(self, message):
        self.status = message
        self.emit(SIGNAL('statusChanged(PyQt_PyObject)'), message)
    
    def slotThreadFinished(self):
        if self.threadRunning: # prevent duplicate call (finished() emitted after terminated())
            self.threadRunning = False
            self.workerThread.wait()
            self.status = "Ready"
            self.slotOperationFinished(self.activeOperation)
            self.emit(SIGNAL('statusChanged(PyQt_PyObject)'), self.status)

    def slotThreadTerminated(self):
        # Same as slotThreadFinished, except no call to QThread.wait() (hangs after terminate())
        self.threadRunning = False
        self.status = "Ready"
        self.slotOperationFinished(self.activeOperation)
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
    
