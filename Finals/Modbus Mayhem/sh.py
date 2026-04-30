from pymodbus.client.sync import ModbusTcpClient

IP = "72.61.200.187"
UNIT = 1
START = 119      # 40120
COUNT = 49       # suffisant pour le flag
XOR_KEY = 0x2020

client = ModbusTcpClient(IP)
client.connect()

resp = client.read_holding_registers(START, COUNT, unit=UNIT)

if resp.isError():
    print("Modbus error")
    exit(1)

flag = ""

for reg in resp.registers:
    val = reg ^ XOR_KEY
    flag += val.to_bytes(2, "little").decode("ascii", errors="ignore")

client.close()

print("FLAG:", flag.strip("\x00"))
