import time

import pyautogui
import pyperclip


def get_clipboard_content():
    original_clipboard = pyperclip.paste()
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    selected_text = pyperclip.paste()
    pyperclip.copy(original_clipboard)
    return selected_text


# Function to apply transformations to the selected text
def apply_transformation(func, selected_text, callback):
    transformed_text = func(selected_text)
    if transformed_text is None:
        return
    callback()
    pyperclip.copy(transformed_text)
    pyautogui.hotkey('ctrl', 'v')
