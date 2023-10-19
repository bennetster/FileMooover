import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, StringVar, ttk
from matplotlib.widgets import Button

data_frames = []
data_frames_names = []
data_frames_folder = []


def graphEm():
    global folder_path
    for root, dirs, files in os.walk(folder_path):
        if root == folder_path:
            continue
        data_frames = []
        data_frames_names = []
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                df = pd.read_excel(file_path)
                data_frames.append(df)

                dn = os.path.splitext(file)[0]
                data_frames_names.append(dn)

        fig, axs = plt.subplots(1, 2, figsize=(18, 8))
        fig.suptitle(os.path.basename(root) + " Comparison")

        for i in range(len(data_frames)):
            df_plot = data_frames[i].reset_index()

            x = df_plot['Q [acfm] (Air flow)']
            y = df_plot['Ps [in.wg] (Pressure)']
            z = df_plot['P [W] (Power)']

            ax1 = axs[0]
            ax1.set_xlabel('Airflow (cfm)')
            ax1.set_ylabel('Pressure (in.wg.)')
            ax1.set_title("Pressure vs Airflow")

            ax1.plot(x, y, label=data_frames_names[i])
            ax1.legend()

            ax2 = axs[1]
            ax2.set_xlabel('Airflow (cfm)')
            ax2.set_ylabel('Power (W)')
            ax2.set_title("Power vs Airflow")

            ax2.plot(x, z, label=data_frames_names[i])
            ax2.legend()

            plt.show(block=False)

        plt.show(block=True)


def browse_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    # Save the folder path to a text file
    with open("folder_path.txt", "w") as f:
        f.write(folder_path)


root = tk.Tk()
root.title("Graph Generator")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.iconbitmap('SystemairLogo.ico')
root.tk.call('source', 'venv/Forest-ttk-theme-master/forest-dark.tcl')

style = ttk.Style(root)
style.theme_use('forest-dark')

label1 = ttk.Label(root, text="Source Folder")
label1.grid(row=0, column=0, padx=10, pady=5)

# create a variable for dropdown
variable = StringVar(root)
variable.set("Choose a variable")  # default value
'''
# create a dropdown list
dropdown_list = ttk.OptionMenu(root, variable, "Variable 1", "Variable 2", "Variable 3")
dropdown_list.grid(row=0, column=0, sticky='ew', padx=10, pady=10)  # <--- added padx and pady options
'''
# Try to read the last used folder path from the text file
try:
    with open("folder_path.txt", "r") as f:
        last_folder_path = f.read()
    folder_path_var = StringVar()
    folder_path_var.set(last_folder_path)
    folder_path_entry = ttk.Entry(root, textvariable=folder_path_var)
    folder_path_entry.grid(row=1, column=0, sticky='ew', padx=10, pady=5)  # <--- added padx and pady options
except:
    folder_path_var = StringVar()
    folder_path_var.set("Select Source Folder")
    folder_path_entry = ttk.Entry(root, textvariable=folder_path_var)
    folder_path_entry.grid(row=1, column=0, sticky='ew', padx=10, pady=5)  # <--- added padx and pady options
folder_path = folder_path_entry.get()
browse_button = ttk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=2, column=0, sticky='ew', padx=10, pady=5)  # <--- added padx and pady options

GraphButton = ttk.Button(root, text="GraphEm", command=graphEm)
GraphButton.grid(row=3, column=0, sticky='ew', padx=10, pady=5)  # <--- added padx and pady options
root.geometry("275x150")
root.mainloop()
# TODO Save filepath to file
