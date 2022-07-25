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
#################################################################

# dict contain stg
strategies = {
    'Golden Cross': GoldenCross,
    'Buy and Hold': BuyHold
             }
##

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


#######################################################################################################################
#######################################################################################################################
class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_list = ["GoldenCross", "Buy and Hold", "Bollinger Band"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):
        # Create a Frame for the Checkbuttons
        self.Strategy_frame = ttk.LabelFrame(self, text="Choose Strategy", padding=(20, 10))
        self.Strategy_frame.grid(
            row=0, column=0,rowspan=2, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        # Text label
        self.label = ttk.Label(
            self.Strategy_frame, text="Name of the strategy",justify="center",
            font=("-size", 15, "-weight", "bold")
        )
        self.label.grid(row=0, column=0,columnspan=2, padx=5, pady=10, sticky="nsew")

        # Combobox
        selected_name_strategy = tk.StringVar()
        self.combobox = ttk.Combobox(self.Strategy_frame, values=self.combo_list,
        textvariable=selected_name_strategy
        )
        self.combobox.current(0)
        self.combobox['state'] = 'readonly'
        self.combobox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.combobox.bind('<<ComboboxSelected>>')

        # function to change label according to what is selected in combobox


        # Accentbutton_select_strategy
        self.accentbutton_select_strategy = ttk.Button(
            self.Strategy_frame, text="Select Strategy", style="Accent.TButton"
        )
        self.accentbutton_select_strategy['command'] = self.label_change_combobox
        self.accentbutton_select_strategy.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")


        # Accentbutton_run_plot_data
        self.accentbutton_run_plot_data = ttk.Button(
            self.Strategy_frame, text="Plot", style="Accent.TButton"
        )
        self.accentbutton_run_plot_data['command'] = self.show_plot
        self.accentbutton_run_plot_data.grid(row=3, column=0,columnspan=2, padx=5, pady=10, sticky="nsew")

    def label_change_combobox(self):
        self.label.config(text=self.combobox.get())
        cerebro.addstrategy(strategies[self.combobox.get()])
    def show_plot(self):
        #cerebro.addstrategy(strategies[self.combobox.get()])
        # run data
        strats = cerebro.run(tradehistory=True)
        # get analyzer data to trade_list variable
        trade_list = strats[0].analyzers.trade_list.get_analysis()
        print('\n=== close data list analyzer === \n', tabulate(trade_list, headers="keys"))
        # plot is last / print any is before plot
        cerebro.plot()




if __name__ == "__main__":
    root = tk.Tk()
    root.title("")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "white")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()

