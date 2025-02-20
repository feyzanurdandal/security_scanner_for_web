import socket
import threading
def scan_port(target, port):
    """Belirtilen hedef IP/domain üzerindeki portu tarar."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[+] Açık Port: {port}")
        s.close()
    except Exception as e:
        print(f"Hata: {e}")

def port_scanner(target, ports):
    """Belirtilen port aralığını tarar (multi-threaded hızlandırma)."""
    print(f"\n[Taranıyor: {target}]")
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()