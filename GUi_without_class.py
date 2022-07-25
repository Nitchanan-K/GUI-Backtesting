from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import backtrader as bt
import matplotlib
matplotlib.use('TKAgg')
from tabulate import tabulate
# import strategies that in the dict contain stg
from Strategies.buyandhold import BuyHold
from Strategies.goldencross import GoldenCross
# import analyzer
from close_trade_list import trade_list
#  import filedialog for gui save
from tkinter import filedialog
#################################################################




# dict contain stg
strategies = {
    'Golden Cross': GoldenCross,
    'BuyHold': BuyHold
             }
##
'''
# set framework
cerebro = bt.Cerebro()
# set cash
cerebro.broker.setcash(10000)
# data
btc_prices = pd.read_csv('C:\\Users\\User\\PycharmProjects\\GUI Backtrader\\Mainbacktrader\\POC for GUI and BackTrader\\BTC-USD.csv', index_col='Date', parse_dates=True)
# feed data and add data
feed = bt.feeds.PandasData(dataname=btc_prices)
cerebro.adddata(feed)
# ask for stg input
#strategy_input()  # or
#cerebro.addstrategy(strategies['Golden Cross'])
# add analyzers
cerebro.addanalyzer(trade_list, _name='trade_list')
# run
#strats = cerebro.run(tradehistory=True)
# get analyzer data
#trade_list = strats[0].analyzers.trade_list.get_analysis()
#print('\n=== close data list analyzer === \n',tabulate(trade_list, headers="keys"))
'''
#######################################################################################################################
# place Holder
selected_strategy = None

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
'''
def show_plot():
    global selected_strategy
    global trade_list


    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000)
    btc_prices = pd.read_csv(
        'C:\\Users\\User\\PycharmProjects\\GUI Backtrader\\Mainbacktrader\\POC for GUI and BackTrader\\BTC-USD.csv',
        index_col='Date', parse_dates=True)
    feed = bt.feeds.PandasData(dataname=btc_prices)
    cerebro.adddata(feed)
    cerebro.addstrategy(selected_strategy)
    # add ana
    cerebro.addanalyzer(trade_list,_name='trade_list')
    # run data

    strats = cerebro.run(tradehistory=True)
    print(strats)
    # get analyzer data to trade_list variable
    trade_list = strats[0].analyzers.trade_list.get_analysis()

    #print('\n=== close data list analyzer === \n', tabulate(trade_list, headers="keys"))
    # plot is last / print any is before plot
    cerebro.plot()
'''



def Run_start():
    cerebro = bt.Cerebro()
    #global cerebro
    global trade_list
    global selected_strategy
    # set cash
    cerebro.broker.setcash(10000)
    # set data
    dataframe = pd.read_csv('BTC-USD.csv', index_col='Date', parse_dates=True)
    # feed data
    feed = bt.feeds.PandasData(dataname=dataframe)
    # add data
    cerebro.adddata(feed)
    # add stg
    cerebro.addstrategy(selected_strategy)
    # add ana
    cerebro.addanalyzer(trade_list, _name='trade_list')
    # run

    #strats = cerebro.run(tradehistory=True)

    # get data from run
    trade_list = cerebro.run(tradehistory=True)[0].analyzers.trade_list.get_analysis()

   # print('\n=== close data list analyzer === \n', tabulate(trade_list, headers="keys"))
    # plot
    cerebro.plot()
    return trade_list


#######################################################################################################################
# make func for button to save file to xlsx
def save_file_xlsx():


    print('check')
    #print(Run_start()[0])
    ##########################################################
    # make DataFrame to pass data from console to DataFrame
    df = pd.DataFrame(trade_list)

    # this is to make ref set number according to the number of data rows (set colum ref number 1 - n)
    # because when we run plot and save plot data ref is adding itself so we need to set it according to data rows
    # use for loop to check how many row and then add number to ref from 1 to n accordingly to the rows
    for i in range(len(df.loc[:,'ref'])):
        df.loc[i:i, 'ref'] = i+1
    # set ref as index
    df.set_index('ref',inplace=True)
    # pop up to ask user to save file use filedialog.asksaveasfile and pass data with panda DataFrame
    try:
        with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
            df.to_excel(file.name)
    except AttributeError:
        print("The user cancelled save")


#######################################################################################################################
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
combo_list = ["Golden Cross", "BuyHold", "Bollinger Band"]


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

























