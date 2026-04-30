from scapy.all import *
from scapy.contrib.modbus import *

load_contrib("modbus")

PCAP_FILE = "Echoes2.pcap"
XOR_KEY = 0x37


def decrypt_custom(enc_bytes):
    """
    Reverse:
        (ord(pin) + 5) ^ i
    """
    out = []
    for i, b in enumerate(enc_bytes):
        val = (b ^ i) - 5
        out.append(val & 0xff)
    return bytes(out)


def extract_flag_registers(packets):
    candidates = []

    for pkt in packets:
        if pkt.haslayer(ModbusPDU03ReadHoldingRegistersResponse):
            pdu = pkt[ModbusPDU03ReadHoldingRegistersResponse]

            raw = bytes(pdu)

            # raw layout:
            # [ func_code | byte_count | data... ]
            if len(raw) < 3:
                continue

            byte_count = raw[1]
            data = raw[2:2 + byte_count]

            candidates.append(data)

    if not candidates:
        raise RuntimeError("No Modbus register payloads found")

    # The real flag payload is the largest one
    return max(candidates, key=len)


def main():
    packets = rdpcap(PCAP_FILE)
    print("[*] PCAP loaded")

    register_bytes = extract_flag_registers(packets)
    print(f"[*] Extracted {len(register_bytes)} bytes")

    # Reverse custom encryption
    decrypted = decrypt_custom(register_bytes)

    # Reverse byte order
    decrypted = decrypted[::-1]

    # Reverse XOR
    flag = bytes(b ^ XOR_KEY for b in decrypted)

    # Strip padding
    flag = flag.rstrip(b"\x00")

    print("\n[+] FLAG FOUND:")
    print(flag.decode(errors="ignore"))


if __name__ == "__main__":
    main()
