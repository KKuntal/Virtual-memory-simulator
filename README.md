# Virtual Memory Management Simulator

## Introduction
The Virtual Memory Management Simulator is an interactive tool designed to help users understand and analyze the behavior of virtual memory in operating systems. It allows experimentation with different paging schemes and page replacement algorithms, providing visual feedback and statistics to illustrate their impact on system performance.

## Features
- **Paging Schemes:** Demand Paging and Pre-Paging
- **Page Replacement Algorithms:** FIFO, LRU, CLOCK
- **Customizable Parameters:** Select process list, memory trace, page size, and policies
- **Graphical User Interface:** For input selection and result visualization
- **Plot Generation:** Visualizes page fault trends and algorithm comparisons
- **Modular Design:** Separates simulation logic, data handling, and presentation

## Project Structure
- `Data/` — Contains process list and process trace files
- `Plots/` — Stores generated plots from simulation runs
- `driver.py` — Main entry point for launching the simulator
- `menuGUI.py` — GUI for user input and configuration
- `generateResults.py` — Runs simulations and creates plots
- `resultsGUI.py` — GUI for displaying results and plots
- `simClass.h`, `simConstants.h`, `simInput.h` — C++ headers for classes, constants, and input handling
- `simulator.cpp` — C++ implementation of the simulation engine

## Getting Started
1. **Install Requirements:** Ensure Python 3 and a C++ compiler are available on your system.
2. **Run the Simulator:**
   - Open a terminal in the project directory.
   - Execute:
     ```
     python driver.py
     ```
3. **Configure Simulation:**
   - Use the GUI to select process list and trace files, page fetch and replacement policies, and page size.
   - Or click 'Set Default' to auto-fill recommended options.
4. **Start Simulation:**
   - Click 'Submit' to begin. Progress will be shown in the interface.
5. **View Results:**
   - After completion, results and plots will be displayed in the results GUI.

## How It Works
The simulator reads user-selected input files and parameters, then runs a C++ backend to emulate memory accesses and page management. Python scripts handle orchestration, progress feedback, and visualization. Results include statistics on page faults and graphical plots comparing different strategies.
