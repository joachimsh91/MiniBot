# MiniBot v2.0.0

MiniBot is a lightweight automation tool with a built-in GUI for managing browser-based MMO gameplay features such as auto fishing, auto food, auto tab switching, and safety logout detection.

This project is based on the browser MMO game **"Minibia"**, but the code is designed to be reusable as a foundation for other MMO automation tools.

> ⚠️ This project is intended for educational purposes only. Use at your own risk.

---

# ✨ Features

## 🍗 AutoFood
Automatically presses a selected hotkey at a defined interval.

## 🔮 RuneMaker
Automatically presses a selected hotkey at a defined interval.

## 🎣 AutoFish
Automates fishing by selecting a screen region and running a fishing cycle inside it.

## 🔄 AutoTab
Automatically switches between game/browser tabs at a set interval.

## 🛑 AutoLogout
Uses OpenCV-based detection to monitor the screen and detect danger (e.g. nearby players).  
Triggers automatic logout when a threat is detected.

---

# 📦 How to setup

1. Clone the project
2. Download the Python dependencies

# ▶️ Running the Project 

Option 1 - IDE:

Open in:

VS Code

Run:

main.py

Option 2 - Terminal:

python main.py

# 🧪 Running Tests

MiniBot uses pytest.

Run all tests:
pytest

Verbose mode:
pytest -v

Run specific test:
pytest tests/test_feature_manager.py

# 🖥️ Usage Guide
1. Configure features

Inside GUI:

Set hotkeys
Set intervals
Save settings

2. Setup regions

🎣 Fishing Area
Open AutoFish tab
Click Setup Fishing Area
Click TOP-LEFT corner
Click BOTTOM-RIGHT corner

🛑 AutoLogout Area
Open AutoLogout tab
Click Setup Battlelist
Click TOP-LEFT corner
Click BOTTOM-RIGHT corner

3. Start bot

Enable features
Click Start Bot
Switch to game window before timer finishes

4. Stop bot

Click Stop Bot

# 💾 Configuration System

All settings are stored in:

setup.json

Includes:

hotkeys
intervals
region coordinates

# 🚀 Build & Release (PyInstaller)
Build executable
pyinstaller --windowed --name MiniBot main.py
Output location
dist/MiniBot/
