from colorama import Fore, Style
import colorama

colorama.init(autoreset=True)

PREFIXES = {
    "success": f"{Fore.GREEN}[+] {Style.RESET_ALL}",
    "fail":    f"{Fore.RED}[-] {Style.RESET_ALL}",
    "error":   f"{Fore.RED}[!] {Style.RESET_ALL}",
    "info":    f"{Fore.CYAN}[?] {Style.RESET_ALL}",
    "system":  f"{Fore.YELLOW}[/] {Style.RESET_ALL}"
}

def log(message, level="info"):
    prefix = PREFIXES.get(level, "")
    print(f"{prefix}{message}")
