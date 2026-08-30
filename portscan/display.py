COLORS = {
    "OPEN": "\033[92m",     # verde
    "CLOSED": "\033[91m",   # rojo
    "FILTERED": "\033[93m",  # amarillo
}
RESET = "\033[0m"


def print_header():
    print(f"{'PORT':<8}{'STATUS':<10}")
    print("-" * 18)


def print_result(port, status):
    color = COLORS.get(status, "")
    print(f"{port:<8}{color}{status:<10}{RESET}")


def print_summary(results):
    open_ports = [port for port, status in results if status == "OPEN"]
    print("-" * 18)
    if open_ports:
        ports_str = ", ".join(str(p) for p in open_ports)
        print(f"Puertos abiertos: {ports_str}")
    else:
        print("No se encontraron puertos abiertos.")
