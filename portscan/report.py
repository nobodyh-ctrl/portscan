import os
from datetime import datetime

from fpdf import FPDF

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


def save_results_pdf(ip, start, end, results):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(RESULTS_DIR, f"scan_{ip}_{timestamp}.pdf")

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "PortScan - Reporte de escaneo", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Target: {ip}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Ports: {start}-{end}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Date: {datetime.now().isoformat()}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(40, 8, "PORT", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    for port, status in results:
        pdf.cell(40, 8, str(port), new_x="RIGHT")
        pdf.cell(0, 8, status, new_x="LMARGIN", new_y="NEXT")

    pdf.output(filename)
    return filename
