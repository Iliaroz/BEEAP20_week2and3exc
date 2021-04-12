import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.font as tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import os.path


class App:
    def __init__(self, root):
        # setting title
        root.title("Power histogram maker GUI")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self._gButton_open = tk.Button(root)
        self._gButton_open["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=12)
        self._gButton_open["font"] = ft
        self._gButton_open["fg"] = "#000000"
        self._gButton_open["justify"] = "center"
        self._gButton_open["text"] = "Open csv..."
        self._gButton_open.place(x=50, y=40, width=100, height=32)
        self._gButton_open["command"] = self.hButton_open_command

        self._gCombo_city = ttk.Combobox(root)
        self._gCombo_city.place(x=350, y=50, width=80, height=25)
        self._gCombo_city.bind("<<ComboboxSelected>>", self.hCombo_city_selected)

        self._gLabel_path = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        self._gLabel_path["font"] = ft
        self._gLabel_path["fg"] = "#333333"
        self._gLabel_path["justify"] = "center"
        self._gLabel_path["text"] = "no file selected"
        self._gLabel_path.place(x=150, y=50, width=150, height=25)

       # these canvases are broken, fix them
       # TODO: set canvases size window size related
        self._gCanvas_upleft = tk.Canvas(root, bg='yellow')
        self._gCanvas_upleft.place(x=50, y=130, width=230, height=140)

        self._gCanvas_upright = tk.Canvas(root, bg='red')
        self._gCanvas_upright.place(x=310, y=130, width=230, height=140)

        self._gCanvas_botleft = tk.Canvas(root, bg='blue')
        self._gCanvas_botleft.place(x=50, y=290, width=230, height=140)

        self._gCanvas_botright = tk.Canvas(root, bg='green')
        self._gCanvas_botright.place(x=310, y=290, width=230, height=140)

    def hButton_open_command(self):
        filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
        )

        filePath = fd.askopenfilename(
                title='Open a CSV file ...',
                initialdir='./',
                filetypes=filetypes)
        if os.path.isfile(filePath) :
            try:
                self.__df = pd.read_csv(filePath)
                self.__df = self.__df.dropna()
                vals = list(self.__df['COMMUNITY AREA NAME'].unique())
                vals.sort()
                self._gCombo_city['values'] = vals
                self._gLabel_path["text"] = os.path.basename(filePath)
                
            except OSError as err:
                print(f"Cannot import file {filePath}.\nOS error: {err}\nExit.")
                # TODO:  show some gui error about file
            except:
                print("Some error happend during opening csv file")
                # TODO: show some gui error message
        else:
            print("No file selected. (or not ordinary file selected)")

    # desired behavior: select one area, show 4 plots drawn on 4 canvases of that area: 
    # top left: bar chart, average KWH by month
    # top right: bar chart, average THERM by month
    # bottom left and bottom right up to you
    def hCombo_city_selected(self, event=None):
        # *** top left bar chart for KWH
        selected_city = self._gCombo_city.get()
        print(f"Selected city: {selected_city}")
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME'] == selected_city]
        # // https://datatofish.com/matplotlib-charts-tkinter-gui/
        fig1 = plt.Figure(figsize=( self._gCanvas_upleft.winfo_width(), self._gCanvas_upleft.winfo_height() ), dpi=100)
        ax1 = fig1.add_subplot(111)
        # --- include it into tkinter
        chart_type = FigureCanvasTkAgg(fig1, self._gCanvas_upleft )
        chart_type.get_tk_widget().pack()
        # ---
        janind = self.__subdf.columns.get_loc("KWH JANUARY 2010")
        graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean().plot.bar(ax=ax1)
        # 



        fig2 = plt.Figure(figsize=( self._gCanvas_upright.winfo_width(), self._gCanvas_upright.winfo_height() ), dpi=100)
        ax2 = fig2.add_subplot(111)
        # --- include it into tkinter
        chart_type = FigureCanvasTkAgg(fig2, self._gCanvas_upright )
        chart_type.get_tk_widget().pack()
        janind = self.__subdf.columns.get_loc("THERM JANUARY 2010")
        graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean().plot.bar(ax=ax2)


        fig3 = plt.Figure(figsize=(self._gCanvas_botleft.winfo_width(), self._gCanvas_botleft.winfo_height()), dpi =100)
        ax3= fig3.add_subplot(111)
        chart_type = FigureCanvasTkAgg(fig3, self._gCanvas_botleft)
        chart_type.get_tk_widget().pack()
        janind = self.__subdf.columns.get_loc("KWH JANUARY 2010")
        graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ])
        graph1.max().plot(ax=ax3,color='red', marker ='*')
        graph1.min().plot(ax=ax3, color='green', marker='o')
        
        fig4 = plt.Figure(figsize=(self._gCanvas_botright.winfo_width(), self._gCanvas_botright.winfo_height()), dpi =100)
        ax4= fig4.add_subplot(111)
        chart_type = FigureCanvasTkAgg(fig4, self._gCanvas_botright)
        chart_type.get_tk_widget().pack()
        janind = self.__subdf.columns.get_loc("THERM JANUARY 2010")
        graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ])
        graph1.max().plot(ax=ax4,color='red', marker ='*')
        graph1.min().plot(ax=ax4, color='green', marker='o')
        



    # TODO: resize canvases on window resize



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
