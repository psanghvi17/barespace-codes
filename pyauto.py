import pyautogui
import time

# Short pause between each command to give the system time to process
pyautogui.PAUSE = 1
time.sleep(1)
# Step 1: Open a new tab using Ctrl + t (works on Windows and Linux; on macOS use 'command')
pyautogui.hotkey('ctrl', 't')

# Step 2: Give it a moment for the tab to open
time.sleep(1)

# Step 3: Type the URL for Gmail
pyautogui.write('https://www.gmail.com', interval=0.1)  # Interval to simulate typing

# Step 4: Press Enter to navigate to Gmail
pyautogui.press('enter')
