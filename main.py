import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.font as tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure

import os.path


class App:
    def __init__(self, root):
        # setting title
        root.title("Power histogram maker GUI")
        # setting window size
        #TODO: MAKE WINDOW BIGGER FOR FIGURES
        width = 1200
        height = 700
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
        
        
        # TODO: fake chart with text "no data to graph"

       # TODO: set canvases size window size related
        self._gCanvas_upleft = tk.Canvas(self._gF_graphs, bg='yellow')
#        self._gCanvas_upleft.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)
        self._gCanvas_upleft.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
        self._gCanvas_upleft.update()
        self.fig1 = figure(figsize=(      self._gCanvas_upleft.winfo_width() / 100, self._gCanvas_upleft.winfo_height() /100   ), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.chart1 = FigureCanvasTkAgg(self.fig1, self._gCanvas_upleft )


        self._gCanvas_upright = tk.Canvas(self._gF_graphs, bg='red')
#        self._gCanvas_upright.pack(side=tk.RIGHT, fill = tk.BOTH, expand = True)
        self._gCanvas_upright.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
        self._gCanvas_upright.update()
        self.fig2 = figure(figsize=(   self._gCanvas_upright.winfo_width() / 100, self._gCanvas_upright.winfo_height() /100  ), dpi=100)
        self.ax2 = self.fig1.add_subplot(111)
        self.chart2 = FigureCanvasTkAgg(self.fig1, self._gCanvas_upright )

        self._gCanvas_botleft = tk.Canvas(self._gF_graphs, bg='blue')
        self._gCanvas_botleft.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)
        self.fig3 = figure(figsize=(   self._gCanvas_botleft.winfo_width() / 100, self._gCanvas_botleft.winfo_height() /100  ), dpi=100)
        self.ax3 = self.fig1.add_subplot(111)
        self.chart3 = FigureCanvasTkAgg(self.fig1, self._gCanvas_botleft )
#        self.chart3.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

        self._gCanvas_botright = tk.Canvas(self._gF_graphs, bg='green')
        self._gCanvas_botright.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
        self.fig4 = figure(figsize=(   self._gCanvas_botright.winfo_width() / 100, self._gCanvas_botright.winfo_height() /100  ), dpi=100)
        self.ax4 = self.fig1.add_subplot(111)
        self.chart4 = FigureCanvasTkAgg(self.fig1, self._gCanvas_botright )
#        self.chart4.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

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
            self.chart1.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
            self.ax1.clear()
            janind = self.__subdf.columns.get_loc("KWH JANUARY 2010")
            self.ax1.bar(     range(1, 13),
                    (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean()     )
            self.chart1.draw()

        def upright(self):
            #UP RIGHT FIGURE
            self.chart2.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
            self.ax2.clear()
            janind = self.__subdf.columns.get_loc("THERM JANUARY 2010")
            self.ax2.bar(    range(1, 13),
                    (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean()     )
            self.chart2.draw()
        
        def botleft(self):
            #BOTTOM LEFT FIGURE
            self.chart3.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
            self.ax3.clear()
            janind = self.__subdf.columns.get_loc("KWH JANUARY 2010")
            self.ax3.plot(     range(1, 13),
                    (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).max(),
                    color='red', marker ='*'    )
            self.ax3.plot(     range(1, 13),
                    (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean(),
                    color='blue', marker ='s'    )
            self.chart3.draw()
        
        def botfig(self):   
            #BOTTOM RIGHT FIGURE
            self.chart4.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
            self.ax4.clear()
            janind = self.__subdf.columns.get_loc("THERM JANUARY 2010")
            self.ax4.plot(     range(1, 13),
                    (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).max(),
                    color='red', marker ='*'    )
            self.ax4.plot(     range(1, 13),
                    (self.__subdf.iloc[ : ,  range(janind, (janind + 12))  ]).mean(),
                    color='blue', marker ='s'    )
            self.chart4.draw()
            
            
            
        upleft(self)
        upright(self)
        botleft(self)
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