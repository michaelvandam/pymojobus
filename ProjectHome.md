Python code to communicate with serial devices implementing the Mojobus protocol.  Mojobus is a protocol created by Brian Dean of BDMICRO LLC.  More details can be found under our ProtocolDescription.

The goal:

1) To have a library to communicate and control devices over a serial bus such as RS485, RS422, RS232.

2) Auto enumeration of devices on the bus,

3) dynamic loading of associated code to communicate with device and,

4) the ability to synchronize actual device states with the "device models in the device library".

5) The protocol will be ASCII text based so it is easier to debug.

6) Adding devices should/is/will be as simple as possible. One new module file and a config/ini file.

7)Written in Python, because I like it, till we need speed (probably never).

4)Asynchronous responses, a response automatically is passed from the device to its object and to call back function with can update the device state.

5)Will be wrapped in a GUI