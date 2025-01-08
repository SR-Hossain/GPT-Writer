import tkinter as tk
from tkinter import simpledialog

from clients import Gemini
from custom_actions import ai_prompt, rephrase
from utils import get_clipboard_content, apply_transformation


def custom_ai_prompt(text):
    prompt = simpledialog.askstring("Custom AI Prompt", "Enter your custom prompt:", parent=root)
    if prompt:
        return Gemini().generate_response(f"{prompt}\n\n{text}")
    return text


class PopupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("GPT Writer")
        self.configure(bg='#2C3E50')
        self.geometry("400x300")
        self.resizable(False, False)
        self.selected_text = get_clipboard_content()

        # Define available transformations (buttons)
        self.transformations = [
            ("AI Prompt", ai_prompt),
            ("Custom Prompt", custom_ai_prompt),
            ("Rephrase", rephrase),
            ("Search AI", self.search_ai),
            ("Advanced Search AI", self.advanced_search_ai),
        ]

        self.selected_index = 0
        self.buttons = []

        # Set up status label
        self.status_label = tk.Label(self, text="Select a transformation:", background='#2C3E50', foreground='white',
                                     font=('Helvetica', 10))
        self.status_label.pack(pady=10)

        # Create transformation buttons
        self._create_buttons()

        # Set initial focus and highlight the first button
        self.buttons[0].focus_set()
        self.buttons[0].config(bg='#2980B9')

        # Bind keyboard events
        self._bind_keyboard_events()

        # Grab focus and ensure the window closes when focus is lost
        self.grab_set()
        self.focus_force()
        self.after(100, self.check_focus)

    def _create_buttons(self):
        """Create transformation buttons and add them to the window."""
        for i, (name, func) in enumerate(self.transformations):
            btn = tk.Button(self, text=name, command=lambda f=func: self.apply_and_close(f),
                            bg='#34495E', fg='white', font=('Helvetica', 12, 'bold'), relief='flat')
            btn.pack(pady=10, padx=20, fill=tk.X)
            self.buttons.append(btn)

    def _bind_keyboard_events(self):
        """Bind keyboard events to navigate and select transformations."""
        self.bind('<Up>', self.move_up)
        self.bind('<Down>', self.move_down)
        self.bind('<Return>', self.apply_selected)
        self.bind('<Escape>', self.close)
        self.protocol("WM_DELETE_WINDOW", self.close)

    def check_focus(self):
        """Check if the window still has focus, close if not."""
        if not self.focus_get():
            self.close()
        else:
            self.after(100, self.check_focus)

    def move_up(self, event):
        """Move up the list of buttons, highlighting the selected one."""
        self._update_button_color(self.selected_index)
        self.selected_index = (self.selected_index - 1) % len(self.buttons)
        self._highlight_button(self.selected_index)

    def move_down(self, event):
        """Move down the list of buttons, highlighting the selected one."""
        self._update_button_color(self.selected_index)
        self.selected_index = (self.selected_index + 1) % len(self.buttons)
        self._highlight_button(self.selected_index)

    def _update_button_color(self, index):
        """Reset the background color of the previously selected button."""
        self.buttons[index].config(bg='#34495E')

    def _highlight_button(self, index):
        """Highlight the newly selected button."""
        self.buttons[index].focus_set()
        self.buttons[index].config(bg='#2980B9')

    def search_ai(self, text=None):
        """Generate a concise response and display it as plain text in the dialog."""
        if text is None:
            text = self.selected_text

        # Generate the AI response
        response = Gemini().generate_response(
            f'N.B: Return response as raw form without any markdown formatting\n\nprompt: {text}')

        # Clear all widgets in the window
        for widget in self.winfo_children():
            widget.destroy()

        # Create a frame to hold the canvas and text widget
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas widget for scrollable area
        canvas = tk.Canvas(frame, bg='#2C3E50')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas for vertical scrolling only
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Text widget to display the AI response
        text_widget = tk.Text(canvas, wrap=tk.WORD, font=('Helvetica', 14), bg='#2C3E50', fg='white', relief='flat',
                              padx=20, pady=20, width=40)
        text_widget.insert(tk.END, response)
        text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
        text_widget.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Create a window inside the canvas to hold the text widget
        canvas.create_window((0, 0), window=text_widget, anchor=tk.NW)

        # Update the scroll region of the canvas to fit the text widget
        text_widget.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Update the window size based on the content
        self.update_idletasks()
        content_height = canvas.bbox("all")[3]  # Height of the text content
        content_width = canvas.bbox("all")[2]  # Width of the text content

        # Adjust window size to fit content, adding some padding for better readability
        self.geometry(f"{max(content_width + 50, 400)}x{content_height + 100}")

        # Add a close button
        close_button = tk.Button(self, text="Close", command=self.close, bg='#2980B9', fg='white',
                                 font=('Helvetica', 12, 'bold'), relief='flat')
        close_button.pack(pady=10)

        # Ensure mouse/touchpad scrolling works by associating scrollbar with canvas
        scrollbar.config(command=canvas.yview)

    def advanced_search_ai(self, text=None):
        """Generate a response from a custom AI prompt and display it as plain text in the dialog."""
        if text is None:
            text = self.selected_text

        # Ask for custom prompt input
        custom_prompt = simpledialog.askstring("Custom AI Prompt", "Enter your custom prompt:", parent=self)

        if custom_prompt:
            # Generate the AI response using the custom prompt
            response = Gemini().generate_response(
                f'N.B: Return response as raw form without any markdown formatting\n\ncontext/input: {text}\n\nprompt: {custom_prompt}')

            # Clear all widgets in the window
            for widget in self.winfo_children():
                widget.destroy()

            # Create a frame to hold the canvas and text widget
            frame = tk.Frame(self)
            frame.pack(fill=tk.BOTH, expand=True)

            # Create a canvas widget for scrollable area
            canvas = tk.Canvas(frame, bg='#2C3E50')
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Add a scrollbar to the canvas for vertical scrolling only
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Create a Text widget to display the AI response
            text_widget = tk.Text(canvas, wrap=tk.WORD, font=('Helvetica', 14), bg='#2C3E50', fg='white', relief='flat',
                                  padx=20, pady=20, width=40)
            text_widget.insert(tk.END, response)
            text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
            text_widget.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            text_widget.configure(yscrollcommand=scrollbar.set)

            # Create a window inside the canvas to hold the text widget
            canvas.create_window((0, 0), window=text_widget, anchor=tk.NW)

            # Update the scroll region of the canvas to fit the text widget
            text_widget.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

            # Update the window size based on the content
            self.update_idletasks()
            content_height = canvas.bbox("all")[3]  # Height of the text content
            content_width = canvas.bbox("all")[2]  # Width of the text content

            # Adjust window size to fit content, adding some padding for better readability
            self.geometry(f"{max(content_width + 50, 400)}x{content_height + 100}")

            # Add a close button
            close_button = tk.Button(self, text="Close", command=self.close, bg='#2980B9', fg='white',
                                     font=('Helvetica', 12, 'bold'), relief='flat')
            close_button.pack(pady=10)

            # Ensure mouse/touchpad scrolling works by associating scrollbar with canvas
            scrollbar.config(command=canvas.yview)

        return None

    def apply_selected(self, event):
        """Invoke the transformation function of the selected button."""
        self.buttons[self.selected_index].invoke()

    def apply_and_close(self, func):
        """Apply the selected transformation and close the popup."""
        self.buttons[self.selected_index].config(bg='#F39C12', text="Loading...")
        self.master.after(100, lambda: apply_transformation(func, self.selected_text, self.close_popup))

    def close_popup(self):
        self.close()
        self.master.after(200, self.master.quit)

    def close(self, event=None):
        """Close the popup window."""
        self.after_cancel(self.after(100, self.check_focus))
        self.grab_release()
        self.destroy()
        self.quit()


# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    popup = PopupWindow(root)
    root.mainloop()
