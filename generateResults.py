import sys
import os
import subprocess
import shutil
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar

# ==============================
# Modern Dark UI Template (logic unchanged)
# ==============================
BG_ROOT = "#0b1220"       # app background (dark navy)
BG_CARD = "#111827"       # card/sections
BORDER  = "#1f2937"       # subtle border
ACCENT  = "#22d3ee"       # cyan accent
ACCENT_SOFT = "#a7f3d0"   # soft mint
TEXT_PRIMARY = "#e5e7eb"  # light gray
TEXT_SECOND  = "#9ca3af"  # secondary text
DANGER       = "#f87171"  # highlight red

FONT_TITLE    = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 14, "bold")
FONT_TEXT     = ("Segoe UI", 12)

# --- Matplotlib Configuration ---
plt.rcParams['figure.figsize'] = [16, 9]
plt.rcParams.update({'font.size': 14})
plt.style.use('dark_background')

# --- Global Variables ---
totalProgress = 0
CONTR_PROCESS = 7
CONTR_PLOT = 3

# ------------------------------
# Rounded background helpers (visual only)
# ------------------------------

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

# ------------------------------
# Modern plot styling (visual only)
# ------------------------------

def _modernize_plot(ax, highlight_index=None):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_color(BORDER)
    ax.spines['bottom'].set_color(BORDER)

    ax.tick_params(axis='x', colors=TEXT_PRIMARY, pad=5)
    ax.tick_params(axis='y', colors=TEXT_PRIMARY, pad=10)

    ax.grid(True, which='major', axis='x', linestyle='--', linewidth=0.6, alpha=0.45, color='#374151')

    # Apply accent colors, keep selected bar as danger
    if highlight_index is not None:
        for i, bar in enumerate(ax.patches):
            bar.set_edgecolor('#000000')
            bar.set_linewidth(0.5)
            bar.set_alpha(0.95 if i == highlight_index else 0.85)
            bar.set_color(DANGER if i == highlight_index else ACCENT)

    # Inline value labels
    for rect in ax.patches:
        ax.text(rect.get_width() + max(rect.get_width()*0.01, 0.2),
                rect.get_y() + rect.get_height()/2,
                f"{rect.get_width():.0f}",
                va='center', ha='left', color=TEXT_PRIMARY, fontsize=12)

# ==============================
# Original LOGIC (unchanged)
# ==============================

def generateStatistics_Plot1():
    """
    Generates data for the first plot by running simulations with different page sizes.
    """
    global pageFaults, PATH_TO_PROCESS_LIST, PATH_TO_PROCESS_TRACE, REPLACEMENT, PAGING
    global totalProgress

    pageSizeList = ['1', '2', '4', '8', '16', '32']
    pageFaultList = []

    for i, pageSize in enumerate(pageSizeList):
        if pageSize == PAGE_SIZE:
            pageFaultList.append(pageFaults)
            pageIndex = i
        else:
            processInfo = ['./a.out', PATH_TO_PROCESS_LIST, PATH_TO_PROCESS_TRACE, REPLACEMENT, PAGING, pageSize, '0']
            process   = subprocess.Popen(processInfo, stdout=subprocess.PIPE)
            dataBytes = process.communicate()[0]
            dataStr   = dataBytes.decode('utf-8')
            data      = list(map(int,dataStr.split(' ')))
            pageFaultList.append(data[2])
        
        totalProgress += CONTR_PROCESS
        updateProgressBar()

    return pageSizeList, pageFaultList, pageIndex


def generateStatistics_Plot2():
    """
    Generates data for the second plot by running simulations with different paging/replacement combinations.
    """
    global pageFaults, PATH_TO_PROCESS_LIST, PATH_TO_PROCESS_TRACE, PAGE_SIZE
    global totalProgress
    
    simCombinations = [['DEMAND', 'FIFO'], ['DEMAND', 'LRU'], ['DEMAND', 'CLOCK'], ['PRE', 'FIFO'], ['PRE', 'LRU'], ['PRE', 'CLOCK']]

    for i, combination in enumerate(simCombinations):
        if combination[0] == PAGING and combination[1] == REPLACEMENT:
            simCombinations[i].append(pageFaults)
            mainIndex = i
        else:
            processInfo = ['./a.out', PATH_TO_PROCESS_LIST, PATH_TO_PROCESS_TRACE, combination[1], combination[0], PAGE_SIZE, '0']
            process   = subprocess.Popen(processInfo, stdout=subprocess.PIPE)
            dataBytes = process.communicate()[0]
            dataStr   = dataBytes.decode('utf-8')
            data      = list(map(int,dataStr.split(' ')))
            simCombinations[i].append(data[2])

        totalProgress += CONTR_PROCESS
        updateProgressBar()

    combinationList = [combination[0] + ' + ' + combination[1] for combination in simCombinations]
    pageFaultList = [combination[2] for combination in simCombinations]

    return combinationList, pageFaultList, mainIndex




def createPlot1():
    """
    Creates and saves the first plot (Page Faults vs. Page Size).
    """
    global totalProgress
    pageSizeList, pageFaultList, pageIndex = generateStatistics_Plot1()
    
    fig, ax = plt.subplots(figsize =(16, 9))
    
    bars = ax.barh(pageSizeList, pageFaultList)  
    ax.invert_yaxis()

    ax.set_ylabel('Page size', color=TEXT_PRIMARY)
    ax.set_xlabel('Number of page faults', color=TEXT_PRIMARY)

    _modernize_plot(ax, highlight_index=pageIndex)
    
    plt.tight_layout()
    plt.savefig('./Plots/plot1.png', dpi=200, bbox_inches='tight')

    totalProgress += CONTR_PLOT
    updateProgressBar()



def createPlot2():
    """
    Creates and saves the second plot (Page Faults vs. Algorithm Combination).
    """
    global totalProgress
    combinationList, pageFaultList, mainIndex = generateStatistics_Plot2()

    fig, ax = plt.subplots(figsize =(16, 9))
    
    bars = ax.barh(combinationList, pageFaultList) 
    ax.invert_yaxis()

    ax.set_ylabel('Different combinations of paging and replacement methods', color=TEXT_PRIMARY)
    ax.set_xlabel('Number of page faults', color=TEXT_PRIMARY)

    _modernize_plot(ax, highlight_index=mainIndex)

    plt.tight_layout()
    plt.savefig('./Plots/plot2.png', dpi=200, bbox_inches='tight')

    totalProgress += CONTR_PLOT
    updateProgressBar()



def executeMainRequest():
    """
    Compiles and runs the main C++ simulation to get the primary results.
    """
    global totalProgress, CONTR_PROCESS

    os.system('g++ -I ./ simulator.cpp')

    processInfo = ['./a.out', PATH_TO_PROCESS_LIST, PATH_TO_PROCESS_TRACE, REPLACEMENT, PAGING, PAGE_SIZE, '1']

    backend   = subprocess.Popen(processInfo, stdout=subprocess.PIPE)
    dataBytes = backend.communicate()[0]
    dataStr   = dataBytes.decode('utf-8')
    data      = list(map(int,dataStr.split(' ')))

    global processCount, memoryRequestCount, pageFaults, pageFaultTracker
    processCount = data[0]
    memoryRequestCount = data[1]
    pageFaults = data[2]
    pageFaultTracker = data[3:]

    totalProgress += CONTR_PROCESS
    updateProgressBar()


def printData():
    """
    Prints the final results to standard output.
    """
    global REPLACEMENT, PAGING, PAGE_SIZE
    global processCount, memoryRequestCount, pageFaults
    print(processCount, memoryRequestCount, PAGING, REPLACEMENT, PAGE_SIZE, pageFaults, end='')


def updateProgressBar():
    """
    Updates the Tkinter progress bar.
    """
    global progress, totalProgress
    progress['value']=totalProgress
    ProgressWin.update_idletasks()


def destroyProgressBar():
    """
    Destroys the Tkinter window.
    """
    global ProgressWin
    ProgressWin.destroy()



def main():
    """
    Main function to orchestrate the simulation and plotting.
    """
    updateProgressBar()
    
    argData = sys.argv

    global PAGING, REPLACEMENT, PATH_TO_PROCESS_LIST, PATH_TO_PROCESS_TRACE, PAGE_SIZE, progress, totalProgress

    PAGING = argData[1]
    REPLACEMENT = argData[2]
    PATH_TO_PROCESS_LIST = argData[3]
    PATH_TO_PROCESS_TRACE = argData[4]
    PAGE_SIZE = argData[5]

    dir = './Plots'
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

    executeMainRequest()
    createPlot1()
    createPlot2()  

    totalProgress += 3
    updateProgressBar()

    printData()
    destroyProgressBar()


if __name__ == '__main__':
    ProgressWin = Tk() 
    ProgressWin.title('Virtual Memory Management Simulator - Processing')
    ProgressWin.config(bg = BG_ROOT)
    ProgressWin.resizable(False, False)

    window_height = 170
    window_width = 520

    screen_width = ProgressWin.winfo_screenwidth()
    screen_height = ProgressWin.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    ProgressWin.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    # Main card frame (keeps your grid layout/logic)
    main_frame=Frame(ProgressWin, relief=GROOVE, bg=BG_CARD, bd=0)
    main_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Rounded card background behind content
    attach_rounded_bg(main_frame, radius=18)

    frame1 = Frame(main_frame, padx=3, pady=3, bg=BG_CARD)
    frame2 = Frame(main_frame, bg=BG_CARD, pady=10, padx=10)

    frame1.grid(row=1, column=1, padx=12, pady=10)
    frame2.grid(row=2, column=1, padx=12, pady=(6,12))

    # Label (modern font/colors)
    label = Label(master=frame1,
                  text="Running simulations! Please wait...",
                  fg=ACCENT_SOFT,
                  font=FONT_SUBTITLE,
                  bg=BG_CARD)
    label.pack()

    # ttk style for progressbar (accent color)
    style = ttk.Style(ProgressWin)
    try:
        style.theme_use('clam')
    except Exception:
        pass
    style.configure("Modern.Horizontal.TProgressbar",
                    troughcolor=BG_CARD,
                    bordercolor=BORDER,
                    background=ACCENT,
                    lightcolor=ACCENT,
                    darkcolor=ACCENT)

    progress = Progressbar(frame2, orient=HORIZONTAL, length=450, mode='determinate',
                           style="Modern.Horizontal.TProgressbar") 
    progress.pack()

    main()