from colorama import Fore, Style
import colorama

colorama.init(autoreset=True)

DEBUG = False

PREFIXES = {
    "success": f"{Fore.GREEN}[+] {Style.RESET_ALL}",
    "fail":    f"{Fore.RED}[-] {Style.RESET_ALL}",
    "error":   f"{Fore.RED}[!] {Style.RESET_ALL}",
    "info":    f"{Fore.CYAN}[?] {Style.RESET_ALL}",
    "system":  f"{Fore.YELLOW}[/] {Style.RESET_ALL}",
    "debug":   f"{Fore.YELLOW}[DEBUG] {Style.RESET_ALL}"
}

def set_debug_mode(value: bool):
    global DEBUG
    DEBUG = value

def log(message, level="info"):
    if level == "debug" and not DEBUG:
        return
    prefix = PREFIXES.get(level, "")
    print(f"{prefix}{message}")
