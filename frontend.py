"""
Book Store GUI (Tkinter front end for backend.py).

Fixes applied:
- backend.connect() is now called on startup to make sure the `book`
  table actually exists. It was never called before, so this app only
  worked because a books.db with the table already happened to exist.
- BUG: `selected_tuple` was never initialized. Clicking Update or Delete
  before selecting a row crashed with NameError. It's now initialized to
  None and Update/Delete check for a selection first.
- `add_command()` used to manually insert a partial tuple (no id) into
  the listbox instead of refreshing from the DB. That row then had the
  wrong shape, so selecting it afterwards broke Update/Delete (which
  expect selected_tuple[0] to be the id). It now just calls view_command()
  to refresh from the database, which includes the real id.
- Added input validation: title is required, year must be a number if
  provided.
- Added a confirmation dialog before deleting.
- Entry fields are now cleared after Add/Update/Delete.
- Replaced wildcard `from tkinter import *` with an explicit import.
"""

import tkinter as tk
from tkinter import messagebox
import backend

backend.connect()

selected_tuple = None

# ---------------- Functions ---------------- #


def clear_entries():
    title_text.set("")
    author_text.set("")
    year_text.set("")
    isbn_text.set("")


def get_selected_row(event):
    global selected_tuple

    try:
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)

        title_text.set(selected_tuple[1])
        author_text.set(selected_tuple[2])
        year_text.set(selected_tuple[3])
        isbn_text.set(selected_tuple[4])

    except IndexError:
        pass


def view_command():
    list1.delete(0, tk.END)

    for row in backend.view():
        list1.insert(tk.END, row)


def search_command():
    list1.delete(0, tk.END)

    for row in backend.search(
        title_text.get().strip(),
        author_text.get().strip(),
        year_text.get().strip(),
        isbn_text.get().strip(),
    ):
        list1.insert(tk.END, row)


def validate_fields():
    if not title_text.get().strip():
        messagebox.showerror("Missing title", "Title is required.")
        return False

    year = year_text.get().strip()
    if year and not year.isdigit():
        messagebox.showerror("Invalid year", "Year must be a number.")
        return False

    return True


def add_command():
    if not validate_fields():
        return

    backend.insert(
        title_text.get().strip(),
        author_text.get().strip(),
        year_text.get().strip() or None,
        isbn_text.get().strip(),
    )

    view_command()
    clear_entries()


def delete_command():
    if selected_tuple is None:
        messagebox.showinfo("No selection", "Select a book from the list first.")
        return

    if not messagebox.askyesno("Confirm delete", f"Delete '{selected_tuple[1]}'?"):
        return

    backend.delete(selected_tuple[0])
    view_command()
    clear_entries()


def update_command():
    if selected_tuple is None:
        messagebox.showinfo("No selection", "Select a book from the list first.")
        return

    if not validate_fields():
        return

    backend.update(
        selected_tuple[0],
        title_text.get().strip(),
        author_text.get().strip(),
        year_text.get().strip() or None,
        isbn_text.get().strip(),
    )

    view_command()
    clear_entries()


# ---------------- Window ---------------- #

window = tk.Tk()
window.title("Book Store")

# ---------------- Labels ---------------- #

tk.Label(window, text="Title").grid(row=0, column=0)
tk.Label(window, text="Author").grid(row=0, column=2)
tk.Label(window, text="Year").grid(row=1, column=0)
tk.Label(window, text="ISBN").grid(row=1, column=2)

# ---------------- Entry Boxes ---------------- #

title_text = tk.StringVar()
e1 = tk.Entry(window, textvariable=title_text)
e1.grid(row=0, column=1)

author_text = tk.StringVar()
e2 = tk.Entry(window, textvariable=author_text)
e2.grid(row=0, column=3)

year_text = tk.StringVar()
e3 = tk.Entry(window, textvariable=year_text)
e3.grid(row=1, column=1)

isbn_text = tk.StringVar()
e4 = tk.Entry(window, textvariable=isbn_text)
e4.grid(row=1, column=3)

# ---------------- Listbox ---------------- #

list1 = tk.Listbox(window, height=8, width=45)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

list1.bind("<<ListboxSelect>>", get_selected_row)

# ---------------- Scrollbar ---------------- #

sb1 = tk.Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

# ---------------- Buttons ---------------- #

tk.Button(window, text="View All", width=12, command=view_command).grid(row=2, column=3)
tk.Button(window, text="Search Entry", width=12, command=search_command).grid(row=3, column=3)
tk.Button(window, text="Add Entry", width=12, command=add_command).grid(row=4, column=3)
tk.Button(window, text="Update", width=12, command=update_command).grid(row=5, column=3)
tk.Button(window, text="Delete", width=12, command=delete_command).grid(row=6, column=3)
tk.Button(window, text="Close", width=12, command=window.destroy).grid(row=7, column=3)

# Load existing data on startup
view_command()

window.mainloop()
