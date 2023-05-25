import tkinter as tk
from tkinter import ttk
import o2a

def convert_text(event=None):
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)
    input_data = input_text.get("1.0", tk.END)
    # You can add your conversion logic here
    output_data = "Failed to convert"
    try:
        output_data = o2a.replace_all(input_data, o2a.strings_to_replace)
    except Exception as e:
        output_data += str(e)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, output_data)
    output_text.config(state=tk.DISABLED)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", tk.END))

root = tk.Tk()
root.title("Obsidian to Anki Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)  # makes column 0 in 'frame' expandable
frame.columnconfigure(1, weight=1)  # makes column 1 in 'frame' expandable
frame.columnconfigure(2, weight=1)  # makes column 2 in 'frame' expandable
frame.rowconfigure((0, 2), weight=1)  # makes row 0 and 2 in 'frame' expandable

input_text = tk.Text(frame, width=50, height=10)
input_text.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='nsew') 
input_text.bind('<KeyRelease>', convert_text)  # Calls convert_text on key release

def clear():
    input_text.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)

def insert_from_clipboard():
    input_text.delete(1.0, tk.END)
    input_text.insert(tk.END, root.clipboard_get())
    convert_text()

clear_button = ttk.Button(frame, text="Clear", command=clear)
clear_button.grid(row=1, column=0, pady=5, sticky='ew')

insert_from_clipboard_button = ttk.Button(frame, text="Insert from clipboard", command=insert_from_clipboard)
insert_from_clipboard_button.grid(row=1, column=1, pady=5, sticky='ew')

copy_button = ttk.Button(frame, text="Copy to clipboard", command=copy_to_clipboard)
copy_button.grid(row=1, column=2, pady=5, sticky='ew')

output_text = tk.Text(frame, width=50, height=10)
output_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
output_text.config(state=tk.DISABLED)  # Disables editing of output_text

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
