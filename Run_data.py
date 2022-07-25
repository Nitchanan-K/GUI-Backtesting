from tkinter import *
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

########################################################################################################################
#
'''
# dict contain stg
strategies = {
    'golden_cross': GoldenCross,
    'buy_hold': BuyHold
}

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
cerebro.addstrategy(strategies['golden_cross'])
# add analyzers
cerebro.addanalyzer(trade_list, _name='trade_list')
# run
strats = cerebro.run(tradehistory=True)
# get analyzer data
trade_list = strats[0].analyzers.trade_list.get_analysis()
print('\n=== close data list analyzer === \n',tabulate(trade_list, headers="keys"))
#cerebro.plot()
'''
########################################################################################################################

# make window
'''
class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=1024)
        main_frame.tk.call("source",
               "C:\\Users\\User\\PycharmProjects\\GUI Backtrader\\Mainbacktrader\\POC for GUI and BackTrader\\theme\\light.tcl"
               )
        main_frame.tk.call("set_theme","light")
'''
# set window
#window = MainWindow()
window = Tk()
# Set the initial theme
style = ttk.Style(master=window)
window.tk.call("source",'C:\\Users\\User\\PycharmProjects\\GUI Backtrader\\Mainbacktrader\\POC for GUI and BackTrader\\azure.tcl'
               )
window.tk.call('set_theme','light')
#############################################################
button = ttk.Button(master=window,
                    text = "Here I am",
                    style = "Accent.TButton"
                    )
button.pack()
##############################################################
toggle_button = ttk.Checkbutton(master=window,
                                text='Toggle button',
                                style='Toggle.TButton'
                                )
toggle_button.pack()
###############################################################
switch = ttk.Checkbutton(master=window, text='Switch',
                         style='Switch.TCheckbutton'
                         )
switch.pack()
###############################################################
radio_button_1 = ttk.Radiobutton(master=window,text="RadioButton",
                               style='TRadiobutton',
                               value= 0
                               )
radio_button_1.pack()
#
radio_button_2 = ttk.Radiobutton(master=window,text="RadioButton",
                               style='TRadiobutton',
                               value= 1
                               )
radio_button_2.pack()
#
radio_button_3 = ttk.Radiobutton(master=window,text="RadioButton",
                               style='TRadiobutton',
                               value= 2
                               )
radio_button_3.pack()


# run window
window.mainloop()
