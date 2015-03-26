# Introduction to MojoBus Protocol #

MojoBus is a human-readable serial communication protocol that was developed by Brian Dean of [BDMICRO LLC](http://www.bdmicro.com). The basic protocol is extremely simple and intuitive, and easily extensible. Basic overview of the protocol can be found here:
  * [SERVO Magazine 03.2007 pg 63](http://servo.texterity.com/servo/200703/?pg=63)
  * [Linux Robotics: programming smarter robots](http://books.google.com/books?id=mxHKcqfdESUC&pg=PA56&dq=mojobus)

MojoBus can be used to communicate with multiple addressable devices over a serial bus such as RS-485.

NOTE: The ideas about custom commands based on meeting between MV and HH 2009-08-14.

# Basic Protocol: #
## Addressing: ##
  * Every module has alphanumerical single character address. The address “0” means ‘broadcast’

## Messages: ##
**Format:
```
>>SLAVE_ADDR,MASTER_ADDR:COMMAND[=X][,COMMAND[=X]…];*
```
Responses:
> Every command message causes an immediate response.  Important because delayed response will mean Master will wait till timeout.
> Response uses same notation, except that it returns**`*`COMMAND=X**for all commands listed**

> QUESTION: what do we do about actions that take longer to complete (e.g. motion, temperature change, etc.)
> ANSWER: Polling.  Device will respond with sometype of busy message till task/state change is complete


## Error Responses: ##

Certain error conditions are detected and a special error response is returned. The format of error responses is:
```
?ERROR_MESSAGE
```

The use of error messages is illustrated in the following command / response conversation:
```
>>a,b:PORTM=FF
>>b,a:?BADCOMMAND
```

The following error messages are supported in the basic protocol:

| **Error Message String** | **Error Description** |
|:-------------------------|:----------------------|
| BADADDR         | Missing Sender Address |
| BADMESSAGE      | Message too long |
| BADCOMMAND      | Unknown command |
| BADPARAM        | Invalid command value (e.g. out of range, wrong data type, etc.) |
| BUS\_COLLISION   | Collision detected on serial bus |

NOTE: Slaves will not do collision detection.  Master devices (i.e. PC) will need to monitor for collisions and deal with incomplete messages.


## Commands: ##
### Standard MojoBus commands: ###
  * ID
> > Set / read the ID in EEPROM (QUESTION: how to use this? ANSWER:Plug one slave at a time and have master broadcast this?).
  * BAUD
> > Set the baud rate (QUESTION: how to receive msg if this is not known? ANSWER default to 9600bps till we need to go faster)
  * SAVEBAUD
> > Saves the current baud rate in EEPROM (see QUESTION above)
  * WHO
> > Returns software info.  We could use this for module type, hardware version, and software version.
  * ANNC
> > Return WHO but delayed proportionally to ID. Master broadcast this and receive response sequentially from all slaves
  * RESET
> > Reset device.


## Custom Commands Overview: ##
### Module Device Specific Commands ###
There are several ways that slave modules could be operated:
  1. Master can set the state of the slave.
  1. Master can trigger state transitions.
  1. Devices may have substates as they as the attempt to transition to the requested
> > state.


> Ex 1.
```
      Sent: >>a,b:LOAD=GO; 
      Reply: >>b,a:*LOAD=DONE;
```

> Ex.
```
      Sent: >>a,b:MVHOME=GO; 
      Reply: >>b,a:*MVHOME=BUSY;
      Sent: >>a,b:MVHOME=?;
      Reply: >>b,a:*MVHOME=BUSY;
      Sent: >>a,b:MVHOME=?;
      Reply: >>b,a:*MVHOME=DONE;
```

  1. Master can query for current state (required for polling)
> > Device responds with current state or substate

### Custom Command Examples: ###
Manual Control messages (to manually override module functions):
  * Read / write particular ports of PIC.  (Standardized to hex)
> > Ex.
```
        Sent: >>a,b:PORTB=AA;
        Reply: >>b,a:*PORTB=aa;
        Sent: >>a,b:PORTA;
        Reply: >>b,a:*PORTA=aa;
        Sent: >>a,b:TRISA=00;
        Reply: >>b,a:*TRISA=00;
        Sent: >>a,b:PORTA;
        Reply: >>b,a:*PORTA=01;

```