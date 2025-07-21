__command__ = "help"
__description__ = "Lists all available commands."

import os
import importlib.util
from utils import log

def get_parser_help(mod):
    if hasattr(mod, 'create_parser'):
        parser = mod.create_parser()
        return parser.format_help()
    return "No parameter information available."

def main():
    log("Available Commands:", "info")
    engine_dir = os.path.dirname(__file__)
    files = [f for f in os.listdir(engine_dir) if f.endswith('.py') and f != 'help.py']

    for file in files:
        path = os.path.join(engine_dir, file)
        try:
            spec = importlib.util.spec_from_file_location("mod", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cmd = getattr(mod, "__command__", file[:-3])
            desc = getattr(mod, "__description__", "No description available.")
            print(f"\n  {cmd:<15} :: {desc}\n")
            for line in get_parser_help(mod).splitlines():
                print(f"    {line}")
        except Exception as e:
            print(f"  [!] Failed to read {file}: {e}")

if __name__ == "__main__":
    main()
