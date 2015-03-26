# Introduction #
The main program runs on the PC and communicates with N hardware devices over a serial communication bus.  Each hardware device has a python counterpart ("model").  The model state is a representation of the hardware state.  Serial commands are issued to the hardware devices to change their hardware state, e.g. in response to GUI events. Responses received from the hardware devices contain new state information that is used to update the model state.  Change in the model state can be observed via the GUI.

# Code Structure #

Threading is used to decouple latencies of serial communication from the models and GUI.


## Serial Communication ##

### Overview ###

Serial communication is handled by three threads:

  * Transmission Thread (TX)
  * Receiver Thread (RX)
  * Dispatch Thread (DISP)

and two queues:

  * Outgoing Command Queue
  * Incoming Response Queue

We are assuming for now that all communication is initiated from the PC.  Commands are executed, and data is requested from the devices/modules.

### Outgoing Message Queue ###

TODO: Rename to Pending Command Queue?

The Outgoing Message Queue holds commands that have been issues by device models but that have not yet been transmitted on the serial bus.  Devices can push messages into the outgoing message queue at any time.

### Incoming Response Queue ###

TODO: Rename to Response Queue?

The Incoming Response queue contains messages that have been received (and arrival timestamp appended) from the serial bus, but that have not yet been processed.

### Transmission (TX) Thread ###

The TX thread continuously monitors the Outgoing Message Queue for new messages. It pops a message from the queue and sends it out on the bus via the connection object.  The sender thread then sets an "incoming message" event object that allows the receiver thread to monitor the bus for responses.  This "incoming message event" is the means by which the TX and RX(see below) threads communicate.

### Receiver (RX) Thread ###

When the "incoming message event" is set the receiver thread begins monitoring the connection for responses. Received messages are appended with a timestamp and then pushed into the response queue. There is a one second timeout that allows the receiver thread to periodically check (approx 1 sec) the serial buffer for new messages in case a device responds late regardless of whether the "incoming message event" has been set.  Upon timeout or receiving a response the receiver thread clears the "incoming message" event allowing the TX thread to send messages if available.

### Response Dispatch Thread ###

The Response Dispatch thread continually monitors the Response Queue for new received messages. It pops a response from the queue, checks the address, and looks up the device "model" instance from the "devices" dictionary using the address as a key. The dispatch then checks the last message from the device to determine if it is a correct response (possibly unnecessary can be removed -HH). The dispatch thread then passes the message to a response processing method on the device model object.  All devices have a lookup table of call back functions assigned to commands.  The response processing method checks each command in the message and passes the parameter into the appropriate callback method of the device.  It is the job of the callback method to update and/or change the state and data of the model device instance depending on the parameter it receives.

## Devices ##

### Devices Dictionary ###

All device instances will be stored in an object called "devices" which is a subclass of dictionary.  Devices can be retrieved from the dictionary using the address as a key.

### Device Model ###

A device object (of the appropriate type) will be instantiated for each physical device detected on the bus.

The device object has 'command' methods that causes messages to be sent to the device, either to update the device state, or to request information.

It also has 'receive' methods (callbacks) that process responses. Responses update state variables in the object.  These state variables will be used by the GUI (if applicable) to  generate a representation of the current device state.

Each state variable has an associated timestamp, indicating when its value was last updated.  State variables are **only** updated by receipt of messages from the device.

### GUI Devices ###
For applications that require a gui each "gui" device model instance is a subclass of a device object instance and also a subclass of a PyQt widget.

This is accomplished through multiple inheritance.  This allows gui device objects to have all the same methods, callbacks and interfaces but also allows for a gui device to be asked to "show itself" when necessary.

Additionally, a gui device can take advantage of the signal and slot concept from PyQt widget.  When the dispatch initiates a callback by passing a message into response processing method of the appropriate device a overloaded response processing method of the gui device instance can 'emit' a signal before returning, this signal tells the gui app that the device state has change and should refresh/update the ui to reflect.