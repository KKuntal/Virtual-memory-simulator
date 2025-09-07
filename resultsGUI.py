# Importing necessary packages to be used
import sys
from tkinter import *
from PIL import Image as PIL_Image
from PIL import ImageTk
import cv2
from tkinter import messagebox

# ------------------------------
# Modern dark palette & fonts
# ------------------------------
BG_ROOT = "#0b1220"       # app background (dark navy)
BG_CARD = "#111827"       # section/cards
BORDER  = "#1f2937"       # subtle border
ACCENT  = "#22d3ee"       # cyan accent
ACCENT_SOFT = "#a7f3d0"   # soft mint for headings
TEXT_PRIMARY = "#e5e7eb"  # light gray
TEXT_SECOND  = "#9ca3af"  # secondary text
DANGER       = "#f87171"  # faults (soft red)

FONT_TITLE    = ("Segoe UI", 28, "bold")
FONT_SUBTITLE = ("Segoe UI", 20, "bold")
FONT_TEXT     = ("Segoe UI", 16)

# ------------------------------
# Rounded background helper (keeps widgets/logic intact)
# ------------------------------

def _round_rect(canvas, x1, y1, x2, y2, r=18, **kwargs):
    # Draw a rounded rectangle on a Canvas
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
    """Places a resizable rounded background behind all content in 'frame'.
    Does not change the layout/logic of children; purely visual.
    """
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
        # Keep background behind content
        bgc.lower("all")

    frame.bind("<Configure>", _redraw)
    frame.after(50, _redraw)
    return bgc


def displayOutputInCanvas():
    # Creating 4 sub frames inside the master_frame (plus extra ones used by original layout)
    frame1 = Frame(master=master_frame, width=1530, pady=10, bg=BG_ROOT)
    frame2 = Frame(master=master_frame, width=1530, pady=6, bg=BG_ROOT)
    frame3 = Frame(master=master_frame, width=1530, pady=12, bg=BG_ROOT)
    frame4 = Frame(master=master_frame, width=1530, pady=6, bg=BG_ROOT)
    frame5 = Frame(master=master_frame, width=1530, pady=6, bg=BG_ROOT)
    frame6 = Frame(master=master_frame, width=1530, pady=10, bg=BG_ROOT)
    frame7 = Frame(master=master_frame, width=1530, pady=6, bg=BG_ROOT)
    frame8 = Frame(master=master_frame, width=1530, pady=10, bg=BG_ROOT)
    frame9 = Frame(master=master_frame, width=1530, pady=10, bg=BG_ROOT)

    frame1.pack(fill=X)
    frame2.pack(fill=X)
    frame3.pack(fill=X)
    frame4.pack(fill=X, pady=(24, 0))
    frame5.pack(fill=X)
    frame6.pack(fill=X)
    frame7.pack(fill=X, pady=(24, 0))
    frame8.pack(fill=X)
    frame9.pack(fill=X)

    # Rounded backgrounds behind key sections
    attach_rounded_bg(frame1, radius=18)
    attach_rounded_bg(frame3, radius=16)
    attach_rounded_bg(frame6, radius=16)
    attach_rounded_bg(frame8, radius=16)

    title = Label(master=frame1,
                  text='VIRTUAL MEMORY MANAGEMENT SIMULATOR',
                  font=FONT_TITLE,
                  fg=ACCENT_SOFT,
                  bg=BG_CARD)
    title.pack(pady=(6, 2))

    subtitle1 = Label(master=frame2, text='Results', font=FONT_SUBTITLE, fg=ACCENT, bg=BG_ROOT)
    subtitle1.pack(side=LEFT, padx=12)

    height = 6
    width = 2
    data = [['Number of Processes',            ':  ' + PROCESS_COUNT],
            ['Number of Memory Requests',      ':  ' + MEMORY_REQ_COUNT],
            ['Fetch Policy',                   ':  ' + PAGING],
            ['Replacement Policy',             ':  ' + REPLACEMENT],
            ['Page size',                      ':  ' + PAGE_SIZE],
            ['Number of Page Faults',          ':  ' + PAGE_FAULTS]]

    # Grid-like key/value lines using Entry (kept for logic parity). Styled to look like labels.
    for i in range(height):  # Rows
        for j in range(width):  # Columns
            if j == 0:
                fgcolor = TEXT_PRIMARY
            elif i == 5:
                fgcolor = DANGER
            else:
                fgcolor = ACCENT

            e = Entry(frame3,
                      fg=fgcolor,
                      font=FONT_TEXT,
                      bg=BG_CARD,
                      highlightthickness=0,
                      borderwidth=0,
                      width=36,
                      disabledbackground=BG_CARD,
                      disabledforeground=fgcolor,
                      readonlybackground=BG_CARD)
            e.grid(row=i, column=j, padx=(18 if j == 0 else 6), pady=6, sticky="w")
            e.insert(END, data[i][j])
            e['state'] = DISABLED

    subtitle2 = Label(master=frame4, text='Statistics', font=FONT_SUBTITLE, fg=ACCENT, bg=BG_ROOT)
    subtitle2.pack(side=LEFT, padx=12)

    plottitle1 = Label(master=frame5,
                       text='Plot 1: Number of pagefaults VS Page size',
                       font=FONT_TEXT,
                       fg=TEXT_PRIMARY,
                       bg=BG_ROOT)
    plottitle1.pack(side=LEFT, padx=12)

    # Displaying plot 1
    canvas1 = Canvas(master=frame6, width=1100, height=619, bg=BG_CARD, highlightthickness=0)
    canvas1.pack(padx=12, pady=8)

    image = cv2.imread('./Plots/plot1.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (1100, 619))
    image = PIL_Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    canvas1.image = image
    canvas1.create_image(0, 0, anchor=NW, image=image)

    plottitle2 = Label(master=frame7,
                       text='Plot 2: Number of pagefaults for different combinations of paging and replacement methods',
                       font=FONT_TEXT,
                       fg=TEXT_PRIMARY,
                       bg=BG_ROOT,
                       wraplength=1400,
                       justify=LEFT)
    plottitle2.pack(side=LEFT, padx=12)

    # Displaying plot 2
    canvas2 = Canvas(master=frame8, width=1100, height=619, bg=BG_CARD, highlightthickness=0)
    canvas2.pack(padx=12, pady=8)

    image = cv2.imread('./Plots/plot2.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (1100, 619))
    image = PIL_Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    canvas2.image = image
    canvas2.create_image(0, 0, anchor=NW, image=image)


def main():
    # Arguments
    argData = sys.argv

    global PROCESS_COUNT, MEMORY_REQ_COUNT, PAGING, REPLACEMENT, PAGE_SIZE, PAGE_FAULTS

    PROCESS_COUNT = argData[1]
    MEMORY_REQ_COUNT = argData[2]
    PAGING = argData[3]
    REPLACEMENT = argData[4]
    PAGE_SIZE = argData[5]
    PAGE_FAULTS = argData[6]

    displayOutputInCanvas()


# Configuring the scroll bar widget and canvas widget

def scrollbar_function(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=1530, height=795)


if __name__ == '__main__':
    # Declaring root window and specifying its attributes
    root = Tk()
    root.title('Virtual Memory Management - Results')
    root.resizable(False, False)
    root.config(bg=BG_ROOT)

    # Defining attributes of root window
    window_height = 800
    window_width = 1550

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    # Creating a main frame inside the root window
    main_frame = Frame(root, relief=GROOVE, bd=0, bg=BG_ROOT)
    main_frame.place(x=0, y=0)

    # Creating a canvas inside main_frame
    canvas = Canvas(main_frame, bg=BG_ROOT, highlightthickness=0, bd=0)
    master_frame = Frame(canvas, bg=BG_ROOT, padx=10, pady=10)

    # Inserting and configuring scrollbar widget
    myscrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill=BOTH, expand=True)
    canvas.create_window((0, 0), window=master_frame, anchor='nw')
    master_frame.bind("<Configure>", scrollbar_function)

    main()

    # Open the root window and loop
    root.mainloop()
