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
        #TODO: MAKE WINDOW BIGGER FOR FIGURES
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        
        ## setting in True  enable to resize window when displayed
        root.resizable(width=False, height=False)

        ## frame for buttons and other controls..
        self._gF_controls = tk.Frame(root)
        self._gF_controls.pack(ipadx=10, ipady=10)
        ## frame for charts
        self._gF_graphs = tk.Frame(root)
        self._gF_graphs.pack(side=tk.BOTTOM,
                             padx=5, pady=5,
                             fill=tk.BOTH,expand=True)


        self._gButton_open = tk.Button(self._gF_controls)
        self._gButton_open["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=12)
        self._gButton_open["font"] = ft
        self._gButton_open["fg"] = "#000000"
        self._gButton_open["justify"] = "center"
        self._gButton_open["text"] = "Open csv..."
        self._gButton_open.pack(side=tk.LEFT,
                                ipadx=10)
        self._gButton_open["command"] = self.hButton_open_command

        #LABEL FOR CSV FILE SELECTED
        self._gLabel_path = tk.Label(self._gF_controls)
        ft = tkFont.Font(family='Times', size=10)
        self._gLabel_path["font"] = ft
        self._gLabel_path["fg"] = "#333333"
        self._gLabel_path["justify"] = "center"
        self._gLabel_path["text"] = "no file selected"
        self._gLabel_path.pack(side=tk.LEFT,
                               ipadx=10)


        #COMBOBOX
        self._gCombo_city = ttk.Combobox(self._gF_controls)
        self._gCombo_city.pack(side=tk.RIGHT)
        self._gCombo_city.bind("<<ComboboxSelected>>", self.hCombo_city_selected)
        #COMBOBOX LABEL
        
        #TODO: MAKE IT NICER LOOKING
        self._gLabel_combo = tk.Label(self._gF_controls)
        ft = tkFont.Font(family = 'Times', size = 12)
        self._gLabel_combo["font"]= ft
        self._gLabel_combo["fg"] = "#333333"
        self._gLabel_combo["justify"] = "center"
        self._gLabel_combo['text']="Select city"
        self._gLabel_combo.pack(side=tk.LEFT)
        
        
        

       #TODO: MAKE THEM BIGGER
       # TODO: set canvases size window size related
        self._gCanvas_upleft = tk.Canvas(self._gF_graphs, bg='yellow')
        self._gCanvas_upleft.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)

        self._gCanvas_upright = tk.Canvas(self._gF_graphs, bg='red')
        self._gCanvas_upright.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)

        self._gCanvas_botleft = tk.Canvas(self._gF_graphs, bg='blue')
        self._gCanvas_botleft.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)

        self._gCanvas_botright = tk.Canvas(self._gF_graphs, bg='green')
        self._gCanvas_botright.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)

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
        #nested functions
        
        selected_city = self._gCombo_city.get()
        print(f"Selected city: {selected_city}")
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME'] == selected_city]
        # // https://datatofish.com/matplotlib-charts-tkinter-gui/
        
        def upleft(self):
            #UP LEFT FIGURE
            fig1 = plt.Figure(figsize=( self._gCanvas_upleft.winfo_width() /100 , self._gCanvas_upleft.winfo_height()/100 ), dpi=40)
            ax1 = fig1.add_subplot(111)
            # --- include it into tkinter
            chart_type = FigureCanvasTkAgg(fig1, self._gCanvas_upleft )
            chart_type.get_tk_widget().pack()
            # ---
            janind = self.__subdf.columns.get_loc("KWH JANUARY 2010")
            graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean().plot.bar(ax=ax1)
        upleft(self)

        def upright(self):
            #UP RIGHT FIGURE
            fig2 = plt.Figure(figsize=( self._gCanvas_upright.winfo_width()/100, self._gCanvas_upright.winfo_height()/100 ), dpi=40)
            ax2 = fig2.add_subplot(111)
            # --- include it into tkinter
            chart_type = FigureCanvasTkAgg(fig2, self._gCanvas_upright )
            chart_type.get_tk_widget().pack()
            janind = self.__subdf.columns.get_loc("THERM JANUARY 2010")
            graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean().plot.bar(ax=ax2)
        upright(self)
        
        def botleft(self):
            #BOTTOM LEFT FIGURE
            fig3 = plt.Figure(figsize=(self._gCanvas_botleft.winfo_width()/100, self._gCanvas_botleft.winfo_height()/100 ), dpi =40)
            ax3= fig3.add_subplot(111)
            chart_type = FigureCanvasTkAgg(fig3, self._gCanvas_botleft)
            chart_type.get_tk_widget().pack()
            janind = self.__subdf.columns.get_loc("KWH JANUARY 2010")
            graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ])
            graph1.max().plot(ax=ax3,color='red', marker ='*')
            graph1.min().plot(ax=ax3, color='green', marker='o')
            plt.setp(ax3.get_xticklabels(), rotation = 90)
        botleft(self)
        
        def botfig(self):   
            #BOTTOM RIGHT FIGURE
            fig4 = plt.Figure(figsize=(self._gCanvas_botright.winfo_width()/100 , self._gCanvas_botright.winfo_height()/100 ), dpi =40)
            ax4= fig4.add_subplot(111)
            chart_type = FigureCanvasTkAgg(fig4, self._gCanvas_botright)
            chart_type.get_tk_widget().pack()
            janind = self.__subdf.columns.get_loc("THERM JANUARY 2010")
            graph1 = (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ])
            graph1.max().plot(ax=ax4,color='red', marker ='*')
            graph1.min().plot(ax=ax4, color='green', marker='o')
            plt.setp(ax4.get_xticklabels(), rotation = 90)
        botfig(self)


    # TODO: resize canvases on window resize

def main():
    root = tk.Tk()
    app = App(root)
    # root.geometry() will return '1x1+www+hhh' here
    root.update()
    # now root.geometry() returns valid size/placement
    root.minsize(root.winfo_width(), root.winfo_height())
    
    ## resize handler
    ### root.bind("<Configure>", app.onsize)
    root.mainloop()




if __name__ == "__main__":
    main()