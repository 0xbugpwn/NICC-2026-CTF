from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock
)
from pymodbus.device import ModbusDeviceIdentification
import random

# -------------------------
# CONSTANTES
# -------------------------
XOR_KEY = 0x2020
FLAG = "NICCTF{MODBUS_PLC+PUMP_registers_cohrir0x0000000}"

def encode_flag(flag):
    regs = []
    for i in range(0, len(flag), 2):
        pair = flag[i:i+2].ljust(2, "\x00")
        val = int.from_bytes(pair.encode(), "little") ^ XOR_KEY
        regs.append(val)
    return regs

ENCODED = encode_flag(FLAG)

# -------------------------
# COILS (présents mais inutiles)
# -------------------------
coils = [0] * 10

# -------------------------
# INPUT REGISTERS (CAPTEURS)
# -------------------------
input_regs = [0] * 100
input_regs[0] = random.randint(120, 160)  # Pressure
input_regs[1] = random.randint(40, 60)    # Flow
input_regs[2] = random.randint(35, 45)    # Temp

# -------------------------
# HOLDING REGISTERS
# -------------------------
holding_regs = [0] * 200

# Bruit réaliste
for i in range(60):
    holding_regs[i] = (i * 17) & 0xFFFF

# Flag stocké à partir de 40120 (index 119)
FLAG_START = 119
for i, v in enumerate(ENCODED):
    holding_regs[FLAG_START + i] = v

# -------------------------
# DATASTORE
# -------------------------
store = ModbusSlaveContext(
    co=ModbusSequentialDataBlock(0, coils),
    hr=ModbusSequentialDataBlock(0, holding_regs),
    ir=ModbusSequentialDataBlock(0, input_regs),
    zero_mode=True
)

context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = "Nana Industries"
identity.ProductCode = "PLC-PUMP-X2"
identity.ProductName = "Water Pump Controller"
identity.MajorMinorRevision = "3.4.1"

print("[+] Modbus PLC running on port 502")
StartTcpServer(context, identity=identity, address=("0.0.0.0", 502))
