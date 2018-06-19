This Modbus Client SubModule is a modification of the Pymodbus3 library.

Changes made to library:

* Changed Base name to modbus_client in hopes to avoid global naming conflicts.
* Removed the Server Module because it is not needed.
* Removed all "sync" modules and files to remove "Twisted library" dependency.
* Removed the serial import to remove pyserial dependency, Connect function on serial always returns False.
