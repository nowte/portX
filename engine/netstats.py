__command__ = "netstat"
__description__ = "Aktif ağ bağlantılarını tablo halinde listeler."

import platform
import subprocess
import argparse
import re
from utils import log

# ANSI renk kodları (Windows 10+ destekler)
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
    lines = output.strip().splitlines()
    results = []

    # Windows netstat kolon başlıkları farklı olabilir.
    # Basit mantık: Başlık satırını bul ve onun altındaki satırlara parse uygula.

    header_index = None
    headers = []
    for i, line in enumerate(lines):
        if system == "windows":
            # Windows'ta genellikle 'Proto  Local Address          Foreign Address        State'
            if re.search(r'^Proto\s+Local Address\s+Foreign Address\s+State', line, re.I):
                header_index = i
                headers = re.split(r'\s{2,}', line.strip())
                break
        else:
            # Unix benzeri: 'Proto Recv-Q Send-Q Local Address           Foreign Address         State'
            if re.search(r'^Proto\s+Recv-Q\s+Send-Q\s+Local Address\s+Foreign Address\s+State', line, re.I):
                header_index = i
                headers = re.split(r'\s+', line.strip())
                break

    if header_index is None:
        # Başlık bulunamadı, ham çıktı döndür
        return None

    data_lines = lines[header_index+1:]

    for line in data_lines:
        if not line.strip():
            continue
        parts = re.split(r'\s{2,}', line.strip())
        # Bazı satırlarda kolon sayısı eksik olabilir, ona göre ayarla
        if len(parts) < len(headers):
            # Eksik kolon varsa, daha ayrıntılı ayırma dene
            parts = re.split(r'\s+', line.strip())
        if len(parts) >= len(headers):
            row = dict(zip(headers, parts))
            results.append(row)
    return results

def print_table(rows, system):
    if not rows:
        log("Netstat çıktısı çözümlenemedi, ham çıktı gösteriliyor.", "fail")
        return

    # Tablo başlığı
    headers = rows[0].keys()
    col_widths = {h: max(len(h), max(len(str(r.get(h, ''))) for r in rows)) for h in headers}

    # Başlık yazdır
    header_line = "  ".join(h.ljust(col_widths[h]) for h in headers)
    print("\n" + header_line)
    print("-" * len(header_line))

    # Satırları yazdır
    for r in rows:
        line_parts = []
        for h in headers:
            val = r.get(h, "")
            # Durum kolonunu renklendir (Windows ve Unix farklı isim olabilir)
            if h.lower() in ("state", "st"):
                val = color_status(val)
            line_parts.append(val.ljust(col_widths[h]))
        print("  ".join(line_parts))
    print()

def netstat(show_all=False, protocol=None):
    system = platform.system().lower()
    cmd = ['netstat']

    if system == "windows":
        if show_all:
            cmd.append('-a')
        if protocol == "tcp":
            cmd.append('-p')
            cmd.append('tcp')
        elif protocol == "udp":
            cmd.append('-p')
            cmd.append('udp')
    else:
        # Linux, macOS
        if show_all:
            cmd.append('-a')
        if protocol == "tcp":
            cmd.append('-t')
        elif protocol == "udp":
            cmd.append('-u')

        # Daha detaylı çıktı için aşağıdakiler eklenebilir
        # cmd.append('-n')  # Sayısal adresler
        # cmd.append('-p')  # Process bilgisi (root gerekebilir)

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        rows = parse_netstat_output(output, system)
        if rows is None:
            log(output)
        else:
            print_table(rows, system)
            log(f"Netstat {len(rows)} bağlantı listelendi.", "success")
    except subprocess.CalledProcessError as e:
        log(f"Netstat komutu başarısız: {e}", "fail")
    except Exception as ex:
        log(f"Beklenmeyen hata: {ex}", "fail")

def create_parser():
    parser = argparse.ArgumentParser(
        prog="netstat",
        description="Aktif ağ bağlantılarını tablo halinde listeler.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument('-h', '--help', action='help', help='Kullanımı gösterir')
    parser.add_argument('-a', '--all', action='store_true', help='Tüm bağlantıları göster')
    parser.add_argument('-p', '--protocol', choices=['tcp','udp'], help='Belirli protokolü göster')
    return parser

def main():
    parser = create_parser()
    args, unknown = parser.parse_known_args()

    if unknown:
        log("Böyle bir biçim desteklenmemektedir. [-h, --help]", "fail")
        return  # Fonksiyonun devamını durdur

    netstat(show_all=args.all, protocol=args.protocol)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("İşlem kullanıcı tarafından iptal edildi (Ctrl+C).", "system")
