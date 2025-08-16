import tkinter as tk
from tkinter import ttk
import math


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Variables
        self.current_number = tk.StringVar()
        self.current_number.set("0")
        self.stored_number = 0
        self.operation = None
        self.new_number = True

        self.create_widgets()

    def create_widgets(self):
        # Display frame
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.pack(fill="x", padx=10, pady=10)

        # Display label
        self.display = ttk.Label(
            display_frame,
            textvariable=self.current_number,
            font=("Arial", 24, "bold"),
            anchor="e",
            background="#f0f0f0",
            relief="sunken",
            padding="10"
        )
        self.display.pack(fill="x")

        # Buttons frame
        buttons_frame = ttk.Frame(self.root, padding="10")
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Button configurations
        button_configs = [
            ("C", 0, 0, 2, 1, "#ff6b6b"),
            ("±", 0, 2, 1, 1, "#4ecdc4"),
            ("÷", 0, 3, 1, 1, "#45b7d1"),
            ("7", 1, 0, 1, 1, "#f7f7f7"),
            ("8", 1, 1, 1, 1, "#f7f7f7"),
            ("9", 1, 2, 1, 1, "#f7f7f7"),
            ("×", 1, 3, 1, 1, "#45b7d1"),
            ("4", 2, 0, 1, 1, "#f7f7f7"),
            ("5", 2, 1, 1, 1, "#f7f7f7"),
            ("6", 2, 2, 1, 1, "#f7f7f7"),
            ("-", 2, 3, 1, 1, "#45b7d1"),
            ("1", 3, 0, 1, 1, "#f7f7f7"),
            ("2", 3, 1, 1, 1, "#f7f7f7"),
            ("3", 3, 2, 1, 1, "#f7f7f7"),
            ("+", 3, 3, 1, 1, "#45b7d1"),
            ("0", 4, 0, 2, 1, "#f7f7f7"),
            (".", 4, 2, 1, 1, "#f7f7f7"),
            ("=", 4, 3, 1, 1, "#ffa726"),
            ("√", 5, 0, 1, 1, "#4ecdc4"),
            ("x²", 5, 1, 1, 1, "#4ecdc4"),
            ("1/x", 5, 2, 1, 1, "#4ecdc4"),
            ("%", 5, 3, 1, 1, "#4ecdc4")
        ]

        # Configure grid weights
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

        # Create buttons
        self.buttons = {}
        for text, row, col, rowspan, colspan, color in button_configs:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Arial", 16, "bold"),
                bg=color,
                fg="black" if color == "#f7f7f7" else "white",
                relief="flat",
                borderwidth=0,
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                     padx=2, pady=2, sticky="nsew")
            self.buttons[text] = btn

    def button_click(self, button_text):
        if button_text.isdigit():
            self.handle_number(button_text)
        elif button_text == ".":
            self.handle_decimal()
        elif button_text in ["+", "-", "×", "÷"]:
            self.handle_operator(button_text)
        elif button_text == "=":
            self.calculate()
        elif button_text == "C":
            self.clear()
        elif button_text == "±":
            self.negate()
        elif button_text == "√":
            self.square_root()
        elif button_text == "x²":
            self.square()
        elif button_text == "1/x":
            self.reciprocal()
        elif button_text == "%":
            self.percentage()

    def handle_number(self, number):
        if self.new_number:
            self.current_number.set(number)
            self.new_number = False
        else:
            current = self.current_number.get()
            if current == "0":
                self.current_number.set(number)
            else:
                self.current_number.set(current + number)

    def handle_decimal(self):
        current = self.current_number.get()
        if "." not in current:
            self.current_number.set(current + ".")
            self.new_number = False

    def handle_operator(self, operator):
        if self.operation and not self.new_number:
            self.calculate()

        self.stored_number = float(self.current_number.get())
        self.operation = operator
        self.new_number = True

    def calculate(self):
        if self.operation and not self.new_number:
            current = float(self.current_number.get())
            if self.operation == "+":
                result = self.stored_number + current
            elif self.operation == "-":
                result = self.stored_number - current
            elif self.operation == "×":
                result = self.stored_number * current
            elif self.operation == "÷":
                if current != 0:
                    result = self.stored_number / current
                else:
                    self.current_number.set("Error")
                    return

            self.current_number.set(str(result))
            self.operation = None
            self.new_number = True

    def clear(self):
        self.current_number.set("0")
        self.stored_number = 0
        self.operation = None
        self.new_number = True

    def negate(self):
        current = float(self.current_number.get())
        self.current_number.set(str(-current))

    def square_root(self):
        current = float(self.current_number.get())
        if current >= 0:
            result = math.sqrt(current)
            self.current_number.set(str(result))
        else:
            self.current_number.set("Error")

    def square(self):
        current = float(self.current_number.get())
        result = current ** 2
        self.current_number.set(str(result))

    def reciprocal(self):
        current = float(self.current_number.get())
        if current != 0:
            result = 1 / current
            self.current_number.set(str(result))
        else:
            self.current_number.set("Error")

    def percentage(self):
        current = float(self.current_number.get())
        result = current / 100
        self.current_number.set(str(result))


def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
