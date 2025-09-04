import psutil
import time

LOG_FILE = "logs/system_logs.txt"

def log_system_metrics():
    with open(LOG_FILE, "a") as f:
        f.write(f"Processes: {len(psutil.pids())}\n")
        f.write(f"CPU usage: {psutil.cpu_percent(interval=1)}%\n")
        mem = psutil.virtual_memory()
        f.write(f"Memory: total={mem.total/1e9:.2f}G, used={mem.used/1e9:.2f}G, free={mem.available/1e9:.2f}G\n")
        disk = psutil.disk_io_counters()
        f.write(f"Disk read/write: {disk.read_bytes/1e6:.2f}MB / {disk.write_bytes/1e6:.2f}MB\n")
        net = psutil.net_io_counters()
        f.write(f"Network packets: sent={net.packets_sent}, recv={net.packets_recv}\n")
        f.write("-"*50 + "\n")

if __name__ == "__main__":
    # Simulate logging every 5 seconds for demo
    for _ in range(5):
        log_system_metrics()
        time.sleep(5)
