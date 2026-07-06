"""
Simple km -> miles converter.

Fixes applied:
- BUG: original code multiplied by 1.6 (that's miles -> km). The correct
  km -> miles factor is 0.6214.
- Added input validation so non-numeric input shows a friendly error
  instead of crashing.
- Clear the output box before writing a new result (previously results
  just kept appending on repeated clicks).
- Replaced wildcard `from tkinter import *` with an explicit import.
"""

import tkinter as tk
from tkinter import messagebox

KM_TO_MILES = 0.6214


def km_to_miles():
    raw_value = km_value.get().strip()

    try:
        km = float(raw_value)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a numeric value for kilometers.")
        return

    miles = km * KM_TO_MILES

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, f"{miles:.2f}")


window = tk.Tk()
window.title("Km to Miles Converter")

label = tk.Label(window, text="Kilometers:")
label.grid(row=0, column=0, padx=5, pady=5)

km_value = tk.StringVar()
entry = tk.Entry(window, textvariable=km_value)
entry.grid(row=0, column=1, padx=5, pady=5)
entry.focus()

convert_button = tk.Button(window, text="Convert", command=km_to_miles)
convert_button.grid(row=0, column=2, padx=5, pady=5)

result_box = tk.Text(window, height=1, width=20)
result_box.grid(row=0, column=3, padx=5, pady=5)

# Allow pressing Enter to trigger the conversion too
window.bind("<Return>", lambda event: km_to_miles())

window.mainloop()
