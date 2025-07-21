# Contributing to This Project

First off, thank you for considering contributing to this project — your help is greatly appreciated!

This document provides guidelines to help make the contribution process smooth, structured, and productive for everyone involved.

---

## 📌 Before You Start

- **Familiarize yourself with the project**: Understand how the `console.bat`, Python scripts, and command system work.
- **Check for existing issues or feature requests** before submitting a new one.
- Make sure your environment includes Python 3.7+ and the required dependencies (`colorama`, etc.).

---

## 🧩 How to Contribute

### 1. Fork the Repository
Click the **Fork** button at the top right of the GitHub page to create your own copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/your-username/your-fork.git
cd your-fork
```

### 3. Create a Feature Branch
Always work on a new branch rather than the main branch.

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
Follow the existing coding style. All new command modules should:

- Define `__command__` and `__description__` at the top of the file
- Use the utils.log() function for logging
- Be compatible with both Windows and Unix systems if possible

### 5. Test Your Changes
- Test locally before pushing. Ensure that:
- The command runs correctly using `console.bat`
- No existing functionality is broken
- `build_command_index.py` successfully indexes the command

### 6. Commit & Push
```bash
git add .
git commit -m "Add: new command [your-feature-name]"
git push origin feature/your-feature-name
```

### 7. Open a Pull Request
- Go to your fork on GitHub and click New Pull Request. Clearly describe:
- What you changed
- Why the change is needed
- Any known issues or limitations

### 🧪 Code Style & Guidelines
- Use Python 3.7+
- Follow PEP 8 where applicable
- Keep code clean, modular, and commented
- Use `argparse` for command-line arguments
- Use `utils.log()` for standardized output with log levels

### 🛡️ Code of Conduct
We expect all contributors to adhere to respectful and inclusive communication. Be kind, collaborative, and constructive.

### 🙋‍♂️ Need Help?
If you're unsure about anything — open an issue or start a discussion. I'm happy to help!