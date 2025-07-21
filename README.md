<div align="center">
 
```
8 888888888o       ,o888888o.     8 888888888o. 8888888 8888888888 `8.`8888.      ,8' 
8 8888    `88.  . 8888     `88.   8 8888    `88.      8 8888        `8.`8888.    ,8'  
8 8888     `88 ,8 8888       `8b  8 8888     `88      8 8888         `8.`8888.  ,8'   
8 8888     ,88 88 8888        `8b 8 8888     ,88      8 8888          `8.`8888.,8'    
8 8888.   ,88' 88 8888         88 8 8888.   ,88'      8 8888           `8.`88888'     
8 888888888P'  88 8888         88 8 888888888P'       8 8888           .88.`8888.     
8 8888         88 8888        ,8P 8 8888`8b           8 8888          .8'`8.`8888.    
8 8888         `8 8888       ,8P  8 8888 `8b.         8 8888         .8'  `8.`8888.   
8 8888          ` 8888     ,88'   8 8888   `8b.       8 8888        .8'    `8.`8888.  
8 8888             `8888888P'     8 8888     `88.     8 8888       .8'      `8.`8888. 
```
 
*Empowering Seamless Network Control and Insight*

![last commit](https://img.shields.io/badge/last%20commit-today-blue)
![python](https://img.shields.io/badge/python-79.9%25-blue)
![languages](https://img.shields.io/badge/languages-2-orange)

**Built with the tools and technologies:**

![JSON](https://img.shields.io/badge/-JSON-000000?style=flat-square&logo=json)
![Markdown](https://img.shields.io/badge/-Markdown-000000?style=flat-square&logo=markdown)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Bat](https://img.shields.io/badge/-Bat-4EAA25?style=flat-square)

</div>

---

**PortX** is a Batch-based terminal interface that dynamically executes Python `(.py)` scripts to process and manage commands. It also features a PowerShell-integrated logging system that provides structured, colorized output for better readability and debugging.
This architecture ensures high performance even on low-end systems and offers a modular, easily extensible design.

---

### 🔍 About This Project

**portX Console** is a lightweight, fast, and platform-independent terminal interface for advanced network diagnostics and IP-based utilities. It provides a modular structure with native Python and Batch integration, making it ideal for both scripting and real-time inspection of connected network devices.

### ✨ Features

- 🔎 `scanip`: Scan the local network and identify active IP addresses.
- 📶 `netstat`: Display active TCP/UDP connections in a color-coded table.
- 📄 `help`: Automatically list available commands with descriptions.
- 🧩 Dynamic command loader (`build_command_index.py`)
- 🧠 Structured logging system with color support (`logmsg`, `utils.py`)
- ⚙️ Compatible with **Windows**, **Linux**, and **macOS**
- 🔒 No external dependencies required except `colorama`

### 📁 Directory Structure
```
├── engine/
│ ├── scanip.py
│ ├── netstat.py
│ ├── help.py
│ ├── utils.py
│ └── logmsg.py
├── build_command_index.py
├── commandmap.json
├── console.bat
├── requirements.txt
├── LICENSE
├── CONTRIBUTING.md
└── CHANGELOG.md
```

### 🚀 Quick Start

```
git clone https://github.com/yourusername/portx-console.git
cd portx-console
pip install -r requirements.txt
```

Then, just run:
```
console.bat
```

ℹ️ For `Unix/macOS`, replace `console.bat` with a compatible shell script (e.g. console.sh if provided).

📦 Dependencies
`colorama` - For colored terminal output
