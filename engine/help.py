import os
import sys
import importlib.util
import uuid
import argparse

DEBUG = False  # utils.py içinde

def set_debug_mode(value: bool):
    global DEBUG
    DEBUG = value

def log(message, level="info"):
    if level == "debug" and not DEBUG:
        return
    print(f"[{level.upper()}] {message}")

def create_parser():
    parser = argparse.ArgumentParser(
        description="Lists all available commands.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    return parser

def main():
    from utils import log, set_debug_mode

    parser = create_parser()
    args = parser.parse_args()

    set_debug_mode(args.debug)
    log("Available Commands:", "info")

    engine_dir = os.path.dirname(__file__)
    files = [f for f in os.listdir(engine_dir) if f.endswith('.py') and f != 'help.py']

    for file in files:
        path = os.path.join(engine_dir, file)
        unique_module_name = f"mod_{file[:-3]}_{uuid.uuid4().hex}"

        try:
            if DEBUG:
                log(f"Loading file: {file}", "debug")

            spec = importlib.util.spec_from_file_location(unique_module_name, path)
            mod = importlib.util.module_from_spec(spec)

            mod.__name__ = unique_module_name
            sys.modules[unique_module_name] = mod

            spec.loader.exec_module(mod)

            if not hasattr(mod, "__command__"):
                log(f"Skipping {file} - __command__ not found.", "debug")
                continue

            cmd = getattr(mod, "__command__")
            desc = getattr(mod, "__description__", "No description available.")
            print(f"  {cmd:<15} :: {desc}")

        except Exception as e:
            log(f"Failed to load '{file}': {e}", "fail")

if __name__ == "__main__":
    main()
