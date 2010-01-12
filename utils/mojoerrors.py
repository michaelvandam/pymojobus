
class MojoException(Exception): pass

class MojoBadCommand(MojoException): pass

class MojoInvalidMessage(MojoException): pass

class MojoInvalidAddress(MojoException): pass

class MojoBadAnnc(MojoException): pass

class MojoBadDevice(MojoException): pass

class MojoBadDeviceConfig(MojoException): pass

class MojoCallbackError(MojoException): pass

class MojoInvalidConfig(MojoException): pass