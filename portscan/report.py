import os
from datetime import datetime

RESULTS_DIR = os.path.join(os.path.expanduser("~"), "portscan_results")


def save_results(ip, start, end, results):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(RESULTS_DIR, f"scan_{ip}_{timestamp}.txt")

    with open(filename, "w") as f:
        f.write(f"Target: {ip}\n")
        f.write(f"Ports: {start}-{end}\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        for port, status in results:
            f.write(f"{port} -> {status}\n")

    return filename
