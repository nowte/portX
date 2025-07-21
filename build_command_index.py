import os
import json
import re

base_dir = os.path.dirname(__file__)
engine_dir = os.path.join(base_dir, "engine")
command_map_path = os.path.join(base_dir, "commandmap.json")

commands = {}

for filename in os.listdir(engine_dir):
    if not filename.endswith(".py"):
        continue

    filepath = os.path.join(engine_dir, filename)

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "__command__" in line:
                match = re.search(r'__command__\s*=\s*["\'](.+?)["\']', line)
                if match:
                    commands[match.group(1)] = filename
                    break
        else:
            commands[filename[:-3]] = filename

if "help" not in commands:
    commands["help"] = "help.py"

with open(command_map_path, "w", encoding="utf-8") as f:
    json.dump(commands, f, indent=2, ensure_ascii=False)
