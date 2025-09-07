# Modernized Main UI for Virtual Memory Management Simulator
# Applies the same modern rounded dark template used in the other windows.

from tkinter import *
import tkinter.filedialog as tkFileDialog
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import os

# Theme (shared with other UI files)
BG_ROOT = "#0b1220"
BG_CARD = "#111827"
BORDER  = "#1f2937"
ACCENT  = "#22d3ee"
ACCENT_SOFT = "#a7f3d0"
TEXT_PRIMARY = "#e5e7eb"
TEXT_SECOND  = "#9ca3af"

FONT_TITLE    = ("Segoe UI", 26, "bold")
FONT_SUBTITLE = ("Segoe UI", 14, "bold")
FONT_TEXT     = ("Segoe UI", 12)

# Rounded background helper (visual only)
from tkinter import Canvas

def _round_rect(canvas, x1, y1, x2, y2, r=18, **kwargs):
    points = [
        x1+r, y1,
        x2-r, y1,
        x2, y1,
        x2, y1+r,
        x2, y2-r,
        x2, y2,
        x2-r, y2,
        x1+r, y2,
        x1, y2,
        x1, y2-r,
        x1, y1+r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def attach_rounded_bg(frame, radius=18, pad=8, fill=BG_CARD, outline=BORDER):
    bgc = Canvas(frame, highlightthickness=0, bd=0, bg=BG_ROOT)
    bgc.place(x=0, y=0, relwidth=1, relheight=1)

    def _redraw(event=None):
        bgc.delete("all")
        w = frame.winfo_width()
        h = frame.winfo_height()
        if w <= 2 or h <= 2:
            return
        _round_rect(
            bgc,
            pad,
            pad,
            max(2, w - pad),
            max(2, h - pad),
            r=radius,
            fill=fill,
            outline=outline,
            width=1,
        )
        bgc.lower("all")

    frame.bind("<Configure>", _redraw)
    frame.after(50, _redraw)
    return bgc

# -----------------
# Logic (kept unchanged)
# -----------------

def select_plist():
    global plist_path
    plist_path = tkFileDialog.askopenfilename()
    if len(plist_path) > 0 and plist_path[-4:]=='.txt':
        plist_path_entry.delete(0,tk.END)
        plist_path_entry.insert(0,plist_path)
    else:
        messagebox.showinfo("Warning","Please choose a .txt file!")


def select_ptrace():
    global ptrace_path
    ptrace_path = tkFileDialog.askopenfilename()
    if len(ptrace_path) > 0 and ptrace_path[-4:]=='.txt':
        ptrace_path_entry.delete(0,tk.END)
        ptrace_path_entry.insert(0,ptrace_path)
    else:
        messagebox.showinfo("Warning","Please choose a .txt file!")


def setDefault():
    global fetch_policy
    global replacement_policy
    global page_size
    global plist_path
    global ptrace_path

    page_size = 2
    fetch_policy ='DEMAND'
    replacement_policy='FIFO'
    plist_path = './Data/plist.txt'
    ptrace_path = './Data/ptrace.txt'

    plist_path_entry.delete(0, tk.END)
    plist_path_entry.insert(0, plist_path)

    ptrace_path_entry.delete(0, tk.END)
    ptrace_path_entry.insert(0, ptrace_path)

    try:
        combobox1.current(0)
        combobox2.current(0)
        combobox3.current(1)
    except Exception:
        pass


def submit():
    global fetch_policy
    global replacement_policy
    global page_size
    global plist_path_var
    global ptrace_path_var
    global plist_path
    global ptrace_path

    plist_path=str(plist_path_var.get())
    ptrace_path=str(ptrace_path_var.get())

    if len(plist_path)<1 or plist_path[-4:]!='.txt':
        messagebox.showinfo("Error", "Process List path invalid!")
        return
    if len(ptrace_path)<1 or ptrace_path[-4:]!='.txt':
        messagebox.showinfo("Error", "Process Trace path invalid!")
        return
    if os.path.isfile(plist_path) == False:
        messagebox.showinfo("Error", "Process List file doesn't exist!")
        return
    if os.path.isfile(ptrace_path) == False:
        messagebox.showinfo("Error", "Process Trace file doesn't exist!")
        return

    fetch_policy = str(c1.get())
    replacement_policy = str(c2.get())
    page_size = int(c3.get())

    if fetch_policy=='' or replacement_policy=='' or page_size=='':
        messagebox.showinfo("Error","All fields not field!")
        return

    print(fetch_policy, replacement_policy, plist_path, ptrace_path, page_size, end='')

    messagebox.showinfo("Info", "Successfully submitted for processing!")

    root.destroy()

# -----------------
# Main UI (modernized visuals)
# -----------------

root = Tk()
root.title('Virtual Memory Management Simulator')
root.resizable(False, False)
root.config(bg=BG_ROOT)

window_height = 500
window_width = 1200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Main card that holds the form
main_card = Frame(root, bg=BG_CARD, bd=0)
# place it centered with margin
main_card.place(relx=0.5, rely=0.5, anchor='center', width=window_width-60, height=window_height-60)
attach_rounded_bg(main_card, radius=18)

# inner frames to preserve your vertical stacking layout
frame1 = Frame(master = main_card, height = 100, width = 1000, pady = 10, bg = BG_CARD)
frame2 = Frame(master = main_card, height = 50, width = 1000, pady = 6, bg = BG_CARD)
frame3 = Frame(master = main_card, height = 50, width = 1000, pady = 6, bg = BG_CARD)
frame4 = Frame(master = main_card, height = 50, width = 1000, pady = 6, bg = BG_CARD)
frame5 = Frame(master = main_card, height = 50, width = 1000, pady = 6, bg = BG_CARD)
frame6 = Frame(master = main_card, height = 50, width = 1000, pady = 6, bg = BG_CARD)

frame1.pack(fill='x', padx=18, pady=(18,6))
frame2.pack(fill='x', padx=18, pady=6)
frame3.pack(fill='x', padx=18, pady=6)
frame4.pack(fill='x', padx=18, pady=6)
frame5.pack(fill='x', padx=18, pady=6)
frame6.pack(fill='x', padx=18, pady=(6,18))

# Title
title = Label(master=frame1, text='VIRTUAL MEMORY MANAGEMENT SIMULATOR', font=FONT_TITLE, fg=ACCENT_SOFT, bg=BG_CARD)
title.pack(anchor='w', padx=6)

# Process list row
plist_path_label = Label(master=frame2, text='Process list :', font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
plist_path_label.pack(side=LEFT, padx=10)

plist_path_var=StringVar()
plist_path=''
plist_path_entry = Entry(master=frame2, textvariable=plist_path_var, width=50, font=FONT_TEXT, bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief=FLAT)
plist_path_entry.pack(side=LEFT, padx=10)

plist_btn = ttk.Button(master=frame2, text='Browse', command=select_plist, style='Accent.TButton')
plist_btn.pack(side=LEFT, padx=10)

# Process trace row
ptrace_path_label = Label(master=frame3, text='Process trace:', font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
ptrace_path_label.pack(side=LEFT, padx=10)

ptrace_path_var=StringVar()
ptrace_path=''
ptrace_path_entry = Entry(master=frame3, textvariable=ptrace_path_var, width=50, font=FONT_TEXT, bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief=FLAT)
ptrace_path_entry.pack(side=LEFT, padx=10)

ptrace_btn = ttk.Button(master=frame3, text='Browse', command=select_ptrace, style='Accent.TButton')
ptrace_btn.pack(side=LEFT, padx=10)

# Fetch & Replacement row
label_fetch = Label(master=frame4, text='Fetch Policy:', font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
label_fetch.pack(side=LEFT, padx=5)

c1 = StringVar()
combobox1 = ttk.Combobox(master=frame4, textvariable=c1, font=FONT_TEXT, width=10, state='readonly')
combobox1['values']=('DEMAND','PRE')
try:
    combobox1.current(0)
except Exception:
    pass
combobox1.pack(side=LEFT, padx=10)

label_replace = Label(master=frame4, text='Replacement Policy:', font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
label_replace.pack(side=LEFT, padx=10)

c2 = StringVar()
combobox2 = ttk.Combobox(master=frame4, textvariable=c2, font=FONT_TEXT, width=10, state='readonly')
combobox2['values']=('FIFO','LRU','CLOCK')
try:
    combobox2.current(0)
except Exception:
    pass
combobox2.pack(side=LEFT, padx=10)

# Page size row
label_pg = Label(master=frame5, text='Page Size:', font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
label_pg.pack(side=LEFT, padx=10)

c3 = StringVar()
combobox3 = ttk.Combobox(master=frame5, textvariable=c3, font=FONT_TEXT, width=10, state='readonly')
combobox3['values']=(1,2,4,8,16,32)
try:
    combobox3.current(0)
except Exception:
    pass
combobox3.pack(side=LEFT, padx=10)

# Buttons row
# configure ttk style for accent buttons
style = ttk.Style(root)
try:
    style.theme_use('clam')
except Exception:
    pass
style.configure('Accent.TButton', foreground=BG_CARD, background=ACCENT, padding=6, relief='flat')
style.map('Accent.TButton', background=[('active', '#1fb8d9')])

btn_default = ttk.Button(master=frame6, text='Set Default', command=setDefault, style='Accent.TButton')
btn_default.pack(side=LEFT, padx=10)

btn_submit = ttk.Button(master=frame6, text='Submit', command=submit, style='Accent.TButton')
btn_submit.pack(side=LEFT, padx=10)

# initialize default values visually
try:
    setDefault()
except Exception:
    pass

root.mainloop()
