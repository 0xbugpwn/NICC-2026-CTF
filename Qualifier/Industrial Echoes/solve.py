from scapy.all import *
from scapy.contrib.modbus import *

load_contrib("modbus")

PCAP_FILE = "IndustrialEchoes.pcap"
XOR_KEY = 0x37 # Bruteforce

def extract_flag_from_pcap(pcap_file):
    packets = rdpcap(pcap_file)

    best_payload = b""

    for pkt in packets:
        if pkt.haslayer(ModbusPDU03ReadHoldingRegistersResponse):
            pdu = pkt[ModbusPDU03ReadHoldingRegistersResponse]

            # registerVal is a LIST of 16-bit integers
            if not hasattr(pdu, "registerVal"):
                continue

            regs = pdu.registerVal
            if not isinstance(regs, list):
                continue

            data = b"".join(r.to_bytes(2, "big") for r in regs)

            # Heuristic: flag packet is the longest coherent payload
            if len(data) > len(best_payload):
                best_payload = data

    if not best_payload:
        print("[-] No Modbus register payload found")
        return

    print(f"[+] Extracted {len(best_payload)} bytes")

    # === Reverse encoding ===
    # 1. reverse
    reversed_bytes = best_payload[::-1]

    # 2. XOR decode
    decoded = bytes(b ^ XOR_KEY for b in reversed_bytes)

    # 3. remove padding
    decoded = decoded.rstrip(b"\x00")

    print("[+] Extracted Flag:")
    print(decoded.decode(errors="ignore")[1:])

if __name__ == "__main__":
    extract_flag_from_pcap(PCAP_FILE)
