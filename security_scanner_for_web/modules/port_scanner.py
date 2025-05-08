import socket
import threading
from queue import Queue
from datetime import datetime

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, thread_count=100):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.thread_count = thread_count
        self.q = Queue()
        self.open_ports = []
        self.lock = threading.Lock()

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    with self.lock:
                        print(f"[+] Port {port} is OPEN")
                        self.open_ports.append(port)
        except Exception:
            pass

    def worker(self):
        while not self.q.empty():
            port = self.q.get()
            self.scan_port(port)
            self.q.task_done()

    def run(self):
        print(f"\n🔍 Scanning {self.target} from port {self.start_port} to {self.end_port}")
        print(f"⏱️ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Kuyruğa portları ekle
        for port in range(self.start_port, self.end_port + 1):
            self.q.put(port)

        # Thread’leri başlat
        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        self.q.join()  # Tüm işler bitene kadar bekle

        print(f"\n✅ Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.open_ports:
            print(f"\n🎯 Open Ports: {self.open_ports}")
            with open("open_ports.txt", "w") as f:
                for port in self.open_ports:
                    f.write(f"{port}\n")
            print("[💾] Results saved to open_ports.txt")
        else:
            print("❌ No open ports found.")

if __name__ == "__main__":
    target_input = input("Enter target IP/domain: ")
    scanner = PortScanner(target_input, start_port=1, end_port=1024, thread_count=150)
    scanner.run()
