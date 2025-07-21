__command__ = "scanip"
__description__ = "Modeme bağlı IP ağı tarar ve aktif IP'leri listeler."

import socket
import subprocess
import platform
import re
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
import multiprocessing
import os
from utils import log

def get_local_ip() -> Optional[str]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        log(f"Yerel IP alınamadı: {e}", "error")
        return None

def ping_ip(ip: str, timeout: int = 1000, system: str = "windows") -> Optional[tuple]:
    param = "-n" if system == "windows" else "-c"
    timeout_param = "-w" if system == "windows" else "-W"
    timeout_val = timeout if system == "windows" else int(timeout / 1000)
    command = ["ping", param, "1", timeout_param, str(timeout_val), ip]

    try:
        output = subprocess.check_output(
            command, stderr=subprocess.DEVNULL, universal_newlines=True
        )
        if system == "windows":
            if "TTL=" in output:
                match = re.search(r"time[=<]([0-9]+)ms", output)
                return (ip, match.group(1) if match else "?")
        else:
            if re.search(r"(1 received|1 packets received)", output):
                match = re.search(r"time=([\d\.]+) ms", output)
                return (ip, match.group(1) if match else "?")
    except:
        return None

def scan_network(base_ip: str, start=1, end=254, max_workers=None, verbose=True, no_color=False) -> List[tuple]:
    system = platform.system().lower()
    ips = [f"{base_ip}.{i}" for i in range(start, end + 1)]
    if max_workers is None:
        max_workers = min(32, multiprocessing.cpu_count() * 2)

    if verbose:
        log(f"Tarama başlatıldı: {base_ip}.{start}-{end}", "info")

    active_ips = []
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(ping_ip, ip, 1000, system): ip for ip in ips
            }
            for future in as_completed(futures, timeout=60):
                result = future.result(timeout=5)
                if result:
                    ip, ms = result
                    active_ips.append((ip, ms))
                    if verbose:
                        if no_color:
                            print(f"{ip} - {ms} ms")
                        else:
                            log(f"\033[0m{ip} - \033[32m{ms} ms\033[0m", "success")
        if verbose:
            log(f"Tarama tamamlandı. Aktif IP: {len(active_ips)}", "success")
        return active_ips
    except Exception as e:
        log(f"Tarama sırasında hata: {e}", "error")
        return []

def validate_ip_block(ip_block: str) -> bool:
    return bool(re.match(r"^(\d{1,3}\.){2}\d{1,3}$", ip_block))

def create_parser():
    default_workers = min(32, multiprocessing.cpu_count() * 2)
    parser = argparse.ArgumentParser(
        prog="scanip",
        description="Modeme bağlı IP ağı tarar ve aktif IP'leri listeler.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-i", "--ip", help="IP bloğu", type=str)
    parser.add_argument("--start", type=int, default=1, help="Başlangıç IP")
    parser.add_argument("--end", type=int, default=254, help="Bitiş IP")
    parser.add_argument("--workers", type=int, default=default_workers, help="İş parçacığı sayısı")
    parser.add_argument("--silent", action="store_true", help="Sessiz mod")
    parser.add_argument("--export", help="Sonuçları dosyaya yaz.", type=str)
    parser.add_argument("--no-color", action="store_true", help="ANSI renklerini kapat")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.ip:
        if not validate_ip_block(args.ip):
            log("Geçersiz IP bloğu formatı. Örnek: 192.168.1", "fail")
            return
        base_ip = args.ip
    else:
        local_ip = get_local_ip()
        if not local_ip:
            log("Yerel IP alınamadı. IP bloğu girin (örn: 192.168.1):", "info")
            while True:
                base_ip = input("> ").strip()
                if validate_ip_block(base_ip):
                    break
                else:
                    log("Geçersiz format.", "fail")
        else:
            base_ip = ".".join(local_ip.split(".")[:-1])
            log(f"Ağ bloğu: {base_ip}.x", "info")

    result = scan_network(
        base_ip=base_ip,
        start=args.start,
        end=args.end,
        max_workers=args.workers,
        verbose=not args.silent,
        no_color=args.no_color
    )

    if result:
        if not args.silent:
            log("Aktif IP'ler:", "info")
            ip_col_width = max(len(ip) for ip, _ in result)
            print()
            header_ip = "IP Adresi".ljust(ip_col_width)
            header_ms = "Ping (ms)"
            if not args.no_color:
                print(f"\033[1m{header_ip}    {header_ms}\033[0m")
            else:
                print(f"{header_ip}    {header_ms}")
            print("-" * (ip_col_width + 12))
    
            for ip, ms in result:
                if not args.no_color:
                    print(f"{ip.ljust(ip_col_width)}    \033[32m{ms}\033[0m")
                else:
                    print(f"{ip.ljust(ip_col_width)}    {ms}")
            print()
        else:
            for ip, _ in result:
                print(ip)
    
        if args.export:
            try:
                with open(args.export, "w", encoding="utf-8") as f:
                    f.write("\n".join(ip for ip, _ in result))
                if not args.silent:
                    log(f"Kayıt dosyası oluşturuldu: {args.export}", "success")
            except Exception as e:
                log(f"Dosyaya yazma hatası: {e}", "error")
    else:
        log("Aktif IP bulunamadı.", "fail")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("İşlem iptal edildi (Ctrl+C).", "system")
