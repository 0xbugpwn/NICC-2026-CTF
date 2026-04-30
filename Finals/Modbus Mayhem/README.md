*Category* : pwn

*Info* :  ``` An industrial water treatment is controlled by an industrial PLC communicating over Modbus TCP.
The system appears to operate normally: **pressure, flow, and temperature** values are continuously updated, and no alarms are raised.
However, engineers suspect the PLC firmware contains hidden maintenance logic left behind during development.
Your mission is to investigate the Modbus registers and recover the hidden information. ```

*points* : 400

*Flag* : NICCTF26{MODBUS_PLC+PUMP_registers_cohrir0x0000000}

*Connection Info* : IP: 72.61.200.187  Port: 502  Unit ID: 1
