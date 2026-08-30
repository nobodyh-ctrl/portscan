import socket
import errno


def scan_port(ip, port, timeout=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    result = sock.connect_ex((ip, port))
    sock.close()

    if result == 0:
        return "OPEN"
    elif result == errno.ECONNREFUSED:
        return "CLOSED"
    else:
        return "FILTERED"


def scan_range(ip, start, end, timeout=3):
    for port in range(start, end + 1):
        status = scan_port(ip, port, timeout)
        yield port, status
