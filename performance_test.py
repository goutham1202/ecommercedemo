# import psutil
# import time

# LOG_FILE = "logs/system_logs.txt"

# def log_system_metrics():
#     with open(LOG_FILE, "a") as f:
#         f.write(f"Processes: {len(psutil.pids())}\n")
#         f.write(f"CPU usage: {psutil.cpu_percent(interval=1)}%\n")
#         mem = psutil.virtual_memory()
#         f.write(f"Memory: total={mem.total/1e9:.2f}G, used={mem.used/1e9:.2f}G, free={mem.available/1e9:.2f}G\n")
#         disk = psutil.disk_io_counters()
#         f.write(f"Disk read/write: {disk.read_bytes/1e6:.2f}MB / {disk.write_bytes/1e6:.2f}MB\n")
#         net = psutil.net_io_counters()
#         f.write(f"Network packets: sent={net.packets_sent}, recv={net.packets_recv}\n")
#         f.write("-"*50 + "\n")

# if __name__ == "__main__":
#     # Simulate logging every 5 seconds for demo
#     for _ in range(5):
#         log_system_metrics()
#         time.sleep(5)

import time
import psutil  # for CPU/memory monitoring
import random

def check_cpu_usage(threshold=80):
    """Fail if CPU usage exceeds threshold"""
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"[CPU Test] Current CPU usage: {cpu_usage}% (Threshold: {threshold}%)")
    if cpu_usage > threshold:
        raise Exception(f"High CPU usage detected: {cpu_usage}% > {threshold}%")
    return True

def check_memory_usage(threshold=80):
    """Fail if memory usage exceeds threshold"""
    memory = psutil.virtual_memory()
    used_percent = memory.percent
    print(f"[Memory Test] Current memory usage: {used_percent}% (Threshold: {threshold}%)")
    if used_percent > threshold:
        raise Exception(f"High memory usage detected: {used_percent}% > {threshold}%")
    return True

def simulate_response_time(max_latency=2.0):
    """Fail if response time is too high"""
    response_time = random.uniform(0.5, 5.0)  # simulate latency between 0.5s and 5s
    print(f"[Latency Test] Simulated response time: {response_time:.2f}s (Threshold: {max_latency}s)")
    if response_time > max_latency:
        raise Exception(f"Slow response detected: {response_time:.2f}s > {max_latency}s")
    return True

def check_thread_count(threshold=1000):
    """Fail if too many threads are active"""
    thread_count = sum(p.num_threads() for p in psutil.process_iter())
    print(f"[Thread Test] Total thread count: {thread_count} (Threshold: {threshold})")
    if thread_count > threshold:
        raise Exception(f"Too many threads: {thread_count} > {threshold}")
    return True


if __name__ == "__main__":
    tests = [
        ("CPU Usage Test", check_cpu_usage),
        ("Memory Usage Test", check_memory_usage),
        ("Latency Simulation Test", simulate_response_time),
        ("Thread Count Test", check_thread_count)
    ]

    failed_tests = []

    for test_name, test_func in tests:
        print(f"\n=== Running {test_name} ===")
        try:
            test_func()
            print(f"[PASS] {test_name}")
        except Exception as e:
            print(f"[FAIL] {test_name}: {str(e)}")
            failed_tests.append((test_name, str(e)))

    print("\n=== Test Summary ===")
    if failed_tests:
        for name, reason in failed_tests:
            print(f"❌ {name} failed because: {reason}")
        exit(1)  # Fail pipeline if any test fails
    else:
        print("✅ All performance tests passed")
