import tkinter as tk
import math

class CircleButton(tk.Canvas):
    def __init__(self, parent, text, command=None, fg="white", bg="#1b3030",
                accent=None, font=("Segoe UI", 13, "bold")):
        super().__init__(parent, highlightthickness=0, bg=parent["bg"])
        self.text = text
        self.command = command
        self.fg = fg
        self.bg = bg
        self.accent = accent
        self.font = font
        self.bind("<Configure>", self._redraw)
        self.bind("<Button-1>", self._click)

    def _redraw(self, event=None):
        self.delete("all")
        size = min(self.winfo_width(), self.winfo_height())
        x0, y0 = (self.winfo_width() - size) // 2, (self.winfo_height() - size) // 2
        x1, y1 = x0 + size, y0 + size

        base_color = self.accent if self.accent else self.bg
        # Shadow oval
        self.create_oval(x0 + 3, y0 + 3, x1 +1, y1+1, fill="#000000", width=5)
        # Opposite side glow oval
        self.create_oval(x0-3, y0-3, x1-2, y1-2, fill="#141414", width=0)
        # Main button oval
        self.create_oval(x0, y0, x1 - 3, y1 - 3, fill=base_color, width=0)
        
        # Text
        self.create_text(self.winfo_width() // 2, self.winfo_height() // 2,
                        text=self.text, fill=self.fg, font=self.font)

    def _click(self, event=None):
        if self.command:
            self.command(self.text)


class DarkCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basic Calculator")
        self.geometry("315x530")
        self.minsize(315, 530)
        self.maxsize(315, 530)
        self.configure(bg="#000000")

        self.display_font = ("Segoe UI", 28, "bold")
        self.button_font = ("Segoe UI", 16, "bold")

        self.text_color = "#e6eef8"
        self.secondary_text = "#9aa6b2"
        self.bg = "#101010"
        self.panel = "#151515"
        self.num_bg = "#252525"
        self.op_bg = "#2d0047"
        self.eq_bg = "#5e0fa0"

        self._make_widgets()
        self._bind_keys()

    def _make_widgets(self):
        top = tk.Frame(self, bg=self.panel, bd=0)
        top.pack(fill="both", padx=6, pady=(6, 6))

        self.display_var = tk.StringVar()
        self.display = tk.Entry(top, textvariable=self.display_var,
                                font=self.display_font, bd=0,
                                justify="right", bg=self.panel,
                                fg=self.text_color,
                                insertbackground=self.text_color)
        self.display.pack(fill="both", ipady=16, padx=8, pady=8)
        self.display_var.set("")

        btn_frame = tk.Frame(self, bg=self.bg)
        btn_frame.pack(fill="both", expand=True, padx=8, pady=6)

        # Button layout
        buttons = [
            ["%", "CE", "C", "⌫"],
            ["1/x", "x²", "²√x", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="]
        ]

        for r, row in enumerate(buttons):
            btn_frame.grid_rowconfigure(r, weight=1)
            for c, label in enumerate(row):
                btn_frame.grid_columnconfigure(c, weight=1)
                if label in ["+", "-", "*", "/", "%"]:
                    accent = self.op_bg
                elif label == "=":
                    accent = self.eq_bg
                else:
                    accent = None
                b = CircleButton(btn_frame, label,
                                command=self._on_button_click,
                                fg=self.text_color,
                                bg=self.num_bg,
                                accent=accent,
                                font=self.button_font)
                b.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

    def _bind_keys(self):
        self.bind("<Return>", lambda e: self._on_button_click("="))
        self.bind("<BackSpace>", lambda e: self._on_button_click("⌫"))
        self.bind("<Escape>", lambda e: self._on_button_click("C"))

    def _validate_input(self, new_value):
        return len(new_value) <= 14


    def _on_button_click(self, char):
        if char == "C":
            self.display_var.set("")            # clear all
        elif char == "CE":
            self.display_var.set("")            # clear entry
        elif char == "⌫":
            ot = self.display_var.get()[:-1] if self.display_var.get()!="Error" else ""
            self.display_var.set(ot)            # backspace
        elif char == "=":
            try:
                expr = self.display_var.get()
                result = eval(expr)
                self.display_var.set(str(result))
            except:
                self.display_var.set("Error")   # Equals
        elif char == "+/-":
            try:
                val = float(self.display_var.get())
                mus = str(-val)
                mus = mus[:-2] if mus.endswith(".0") else mus
                self.display_var.set(str(-val))
            except:
                pass                           # Negative function
        elif char == "%":
            try:
                val = float(self.display_var.get())
                per = str(val / 100)
                per = per[:-2] if per.endswith(".0") else per
                self.display_var.set(per)
            except:
                pass                           # Percentage function
        elif char == "1/x":
            try:
                val = float(self.display_var.get())
                den = str(1 / val)
                den = den[:-2] if den.endswith(".0") else den
                self.display_var.set(den)
            except:
                self.display_var.set("Error")  # Reciprocal function
        elif char == "x²":
            try:
                val = float(self.display_var.get())
                sqr = str(val ** 2)
                sqr = sqr[:-2] if sqr.endswith(".0") else sqr
                self.display_var.set(sqr)
            except:
                self.display_var.set("Error") # Square function
        elif char == "²√x":
            try:
                val = float(self.display_var.get())
                srt = str(math.sqrt(val))
                srt = srt[:-2] if srt.endswith(".0") else srt
                self.display_var.set(srt)
            except:
                self.display_var.set("Error") # Square root function
        else:
            # limit input length to 13 characters
            if len(self.display_var.get()) >= 13:
                return
            self.display_var.set(self.display_var.get() + char)


if __name__ == "__main__":
    DarkCalculator().mainloop()
