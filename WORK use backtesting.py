# import lib that we need
# Dataframe
import pandas as pd
from tabulate import tabulate

# vis plot
import matplotlib
matplotlib.use('TKAgg')
# import GUI

from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk

#  import filedialog for gui save
from tkinter import filedialog

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG , EURUSD

#######################################################################################################################
# place Holder
#selected_strategy = None

#######################################################################################################################
# function for the root
# label_change_combobox = change label show choose strategy
def label_change_combobox():
    global selected_strategy
    label.config(text=combobox.get())
    # strategies[combobox.get()] need to be value from the combobox as str
    # and str need to be the same in strategies (dict) that point to the class of that strategy
    # combobox.get() = name of strategy in dict that refer to the strategy Class
    selected_strategy = strategies[combobox.get()]
    print(strategies[combobox.get()])




###################################################################################################
# strategy

class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


class Sma4Cross(Strategy):
    n1 = 50
    n2 = 100
    n_enter = 50#20
    n_exit = 25#10

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
        self.sma_enter = self.I(SMA, self.data.Close, self.n_enter)
        self.sma_exit = self.I(SMA, self.data.Close, self.n_exit)

    def next(self):

        if not self.position:

            # On upwards trend, if price closes above
            # "entry" MA, go long

            # Here, even though the operands are arrays, this
            # works by implicitly comparing the two last values
            if self.sma1 > self.sma2:
                if crossover(self.data.Close, self.sma_enter):
                    self.buy()

            # On downwards trend, if price closes below
            # "entry" MA, go short

            else:
                if crossover(self.sma_enter, self.data.Close):
                    self.sell()

        # But if we already hold a position and the price
        # closes back below (above) "exit" MA, close the position

        else:
            if (self.position.is_long and
                    crossover(self.sma_exit, self.data.Close)
                    or
                    self.position.is_short and
                    crossover(self.data.Close, self.sma_exit)):
                self.position.close()
###################################################################################################
# dict contain stg
strategies = {
    'SmaCross': SmaCross,
    'Sma4Cross': Sma4Cross
             }



###################################################################################################
def Run_start():
    global selected_strategy

    bt = Backtest(GOOG, selected_strategy, cash=10_000, commission=.002,
                  exclusive_orders=True)
    stats = bt.run()
    print(stats["_trades"])
    bt.plot()
    Run_start.stats = stats
# make func for button to save file to xlsx
def save_file_xlsx():


    print('check')
    #print(Run_start()[0])
    ##########################################################
    # make DataFrame to pass data from console to DataFrame
    df = pd.DataFrame(Run_start.stats["_trades"])

    # pop up to ask user to save file use filedialog.asksaveasfile and pass data with panda DataFrame
    try:
        with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
            df.to_excel(file.name)
    except AttributeError:
        print("The user cancelled save")
'''
    # this is to make ref set number according to the number of data rows (set colum ref number 1 - n)
    # because when we run plot and save plot data ref is adding itself so we need to set it according to data rows
    # use for loop to check how many row and then add number to ref from 1 to n accordingly to the rows
    for i in range(len(df.loc[:,'ref'])):
        df.loc[i:i, 'ref'] = i+1
    # set ref as index
    df.set_index('ref',inplace=True)
'''

###################################################################################################
# make window
root = tk.Tk()

# Make the app responsive
for index in [0, 1, 2]:
    root.columnconfigure(index=index, weight=1)
    root.rowconfigure(index=index, weight=1)

# Simply set the theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "white")

# set value #### #### #### ###
combo_list = ["Sma4Cross", "SmaCross", "Bollinger Band"]


# make Strategy_frame
Strategy_frame = ttk.LabelFrame(master=root, text="Choose Strategy", padding=(20, 10))
Strategy_frame.grid(row=0, column=0,rowspan=2,
                    padx=(20, 10), pady=(20, 10), sticky="nsew"
                    )

# Text label
label = ttk.Label(master=Strategy_frame, text="Name of the strategy",justify="center",
                  font=("-size", 15, "-weight", "bold")
                  )
label.grid(row=0, column=0,columnspan=2, padx=5, pady=10, sticky="nsew")

# Combobox
selected_name_strategy = tk.StringVar()
combobox = ttk.Combobox(master=Strategy_frame, values=combo_list,
                        textvariable=selected_name_strategy
                        )
combobox.current(0)
combobox['state'] = 'readonly'
combobox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
combobox.bind('<<ComboboxSelected>>')

#######################################################
# Accentbutton_select_strategy
accent_button_select_strategy = ttk.Button(master=Strategy_frame, text="Select Strategy",
                                          style="Accent.TButton"
                                          )
accent_button_select_strategy['command'] = label_change_combobox
accent_button_select_strategy.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

# Accentbutton_run_plot_data
accent_button_run_plot_data = ttk.Button(master=Strategy_frame, text="Plot",
                                         style="Accent.TButton"
                                         )
accent_button_run_plot_data['command'] = Run_start
accent_button_run_plot_data.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

# Accentbutton_save_plot_data
accent_button_save_plot_data = ttk.Button(master=Strategy_frame, text="Save",
                                          style="Accent.TButton"
                                         )
accent_button_save_plot_data['command'] = save_file_xlsx
accent_button_save_plot_data.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")









# Set a minsize for the window, and place it in the middle
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

# run window
root.mainloop()
