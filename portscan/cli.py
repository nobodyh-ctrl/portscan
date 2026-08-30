import argparse

from portscan.scanner import scan_range
from portscan.display import print_header, print_result, print_summary
from portscan.banner import print_banner
from portscan.report import save_results


def main():
    parser = argparse.ArgumentParser(description="Escaneo básico de puertos TCP.")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-s", "--start", required=True, type=int, help="Start port")
    parser.add_argument("-e", "--end", required=True, type=int, help="End port")
    args = parser.parse_args()

    print_banner()
    print_header()

    results = []
    for port, status in scan_range(args.target, args.start, args.end):
        print_result(port, status)
        results.append((port, status))

    print_summary(results)

    filename = save_results(args.target, args.start, args.end, results)
    print(f"\nResultados guardados en: {filename}")


if __name__ == "__main__":
    main()
