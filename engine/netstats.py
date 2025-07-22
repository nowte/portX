__command__ = "netstat"
__description__ = "Displays active network connections in a table."

import platform
import subprocess
import argparse
import re
from utils import log, set_debug_mode  # utils'de debug kontrol fonksiyonu olduğunu varsayıyorum

COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"

def color_status(status):
    status = status.upper()
    if status == "ESTABLISHED":
        return COLOR_GREEN + status + COLOR_RESET
    elif status in ["TIME_WAIT", "CLOSE_WAIT"]:
        return COLOR_YELLOW + status + COLOR_RESET
    elif status in ["LISTEN", "SYN_SENT", "SYN_RECEIVED"]:
        return COLOR_CYAN + status + COLOR_RESET
    else:
        return status

def parse_netstat_output(output, system):
    log("Parsing netstat output...", "debug")
    lines = output.strip().splitlines()
    results = []

    header_index = None
    headers = []
    for i, line in enumerate(lines):
        if system == "windows":
            if re.search(r'^Proto\s+Local Address\s+Foreign Address\s+State', line, re.I):
                header_index = i
                headers = re.split(r'\s{2,}', line.strip())
                log(f"Found headers on line {i}: {headers}", "debug")
                break
        else:
            if re.search(r'^Proto\s+Recv-Q\s+Send-Q\s+Local Address\s+Foreign Address\s+State', line, re.I):
                header_index = i
                headers = re.split(r'\s+', line.strip())
                log(f"Found headers on line {i}: {headers}", "debug")
                break

    if header_index is None:
        log("Failed to find header line in netstat output.", "fail")
        return None

    data_lines = lines[header_index + 1:]

    for line in data_lines:
        if not line.strip():
            continue
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) < len(headers):
            parts = re.split(r'\s+', line.strip())
        if len(parts) >= len(headers):
            row = dict(zip(headers, parts))
            results.append(row)

    log(f"Parsed {len(results)} connection entries.", "debug")
    return results

def print_table(rows, system):
    if not rows:
        log("Failed to parse netstat output. Showing raw output instead.", "fail")
        return

    headers = rows[0].keys()
    col_widths = {h: max(len(h), max(len(str(r.get(h, ''))) for r in rows)) for h in headers}

    header_line = "  ".join(h.ljust(col_widths[h]) for h in headers)
    print("\n" + header_line)
    print("-" * len(header_line))

    for r in rows:
        line_parts = []
        for h in headers:
            val = r.get(h, "")
            if h.lower() in ("state", "st"):
                val = color_status(val)
            line_parts.append(val.ljust(col_widths[h]))
        print("  ".join(line_parts))
    print()

def netstat(show_all=False, protocol=None):
    system = platform.system().lower()
    log(f"Detected OS: {system}", "debug")

    cmd = ['netstat']

    if system == "windows":
        if show_all:
            cmd.append('-a')
        if protocol == "tcp":
            cmd.extend(['-p', 'tcp'])
        elif protocol == "udp":
            cmd.extend(['-p', 'udp'])
    else:
        if show_all:
            cmd.append('-a')
        if protocol == "tcp":
            cmd.append('-t')
        elif protocol == "udp":
            cmd.append('-u')

    log(f"Executing command: {' '.join(cmd)}", "debug")

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        log(f"Command executed successfully, length of output: {len(output)} characters", "debug")
        rows = parse_netstat_output(output, system)
        if rows is None:
            log(output)
        else:
            print_table(rows, system)
            log(f"Netstat listed {len(rows)} connections.", "success")
    except subprocess.CalledProcessError as e:
        log(f"Netstat command failed: {e}", "fail")
    except Exception as ex:
        log(f"Unexpected error: {ex}", "fail")

def create_parser():
    parser = argparse.ArgumentParser(
        prog="netstat",
        description="Displays active network connections in a table.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument('-h', '--help', action='help', help='Show usage information')
    parser.add_argument('-p', '--protocol', choices=['tcp', 'udp'], help='Filter by protocol')
    parser.add_argument('-a', '--all', action='store_true', help='Show all connections')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    return parser

def main():
    parser = create_parser()
    args, unknown = parser.parse_known_args()

    if unknown:
        log("Unsupported argument format. Use [-h, --help]", "fail")
        return

    set_debug_mode(args.debug)  # utils içindeki debug modu ayarlama fonksiyonu

    log(f"Debug mode is {'enabled' if args.debug else 'disabled'}.", "debug")

    netstat(show_all=args.all, protocol=args.protocol)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Operation cancelled by user (Ctrl+C).", "system")
