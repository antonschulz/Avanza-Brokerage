#! python
import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import avanzaClass as avanza

# TODO: Change colorscheme to something cleaner

root = Tk()
root.configure(background="white")
root.title("Avanza Brokerage")

class App:
    # Creates static app GUI
    def __init__(self):
        self.createButtons()
        self.createGraphs()

    def createButtons(self):
        frame = Frame(root, bg="white")
        frame.pack()

        submitframe = Frame(frame, bg="white")
        submitframe.pack(side=BOTTOM)

        middleframe = Frame(frame, bg="white")
        middleframe.pack(side=BOTTOM)
        # TODO: change name to "courtageframe"
        self.bottomframe = Frame(root, bg="white")
        self.bottomframe.pack(side=BOTTOM)

        self.depositsframe = Frame(self.bottomframe, bg="white")
        self.depositsframe.pack(side=BOTTOM)

        startLabel = Label(frame, text="Start Date",font=("Arial", 13),bg="white")
        startLabel.pack(side=LEFT)

        endLabel = Label(frame,text="End Date ",font=("Arial", 13),bg="white")
        endLabel.pack(side=RIGHT)

        
        self.startDate = StringVar()
        self.startEntry = Entry(middleframe, textvariable=self.startDate, bd=3)
        self.startEntry.pack(side=LEFT)
        
        
        self.endDate = StringVar()
        self.endEntry = Entry(middleframe, textvariable=self.endDate, bd=3)
        self.endEntry.pack(side=LEFT)
        
        submitButton=Button(submitframe, text="Submit", command=self.getUserInput,bg="white")
        submitButton.pack(side=LEFT)

        fileButton = Button(submitframe, text="Open File", command=self.selectFile, bg="white")
        fileButton.pack(side=LEFT)

    def selectFile(self):
        FILE = askopenfilename()
        self.FILE = FILE
    
    def getUserInput(self):
        self.avanza = avanza.Avanza(self.FILE)
        # If no user input => get the whole date-range
        if len(self.startDate.get()) == 0:
            self.newEndDate, self.newStartDate = self.avanza.getFileDates()
            self.startEntry.insert(0,string=self.newStartDate)
            self.endEntry.insert(0,string=self.newEndDate)
        else:
            self.newStartDate = self.startDate.get()
            self.newEndDate = self.endDate.get()

        self.updateCourtageGraphs()
        self.updateDepositGraphs()
    
    def createGraphs(self):
        plt.style.use("seaborn")
        def genericGraph (frameName):
            figure = plt.Figure(figsize=(5,3.2),facecolor="white", tight_layout=True)
            ax = figure.add_subplot(111)
            chart_type = FigureCanvasTkAgg(figure,frameName)
            chart_type.get_tk_widget().pack(side=LEFT)
            ax.tick_params(axis="x", rotation=70)
            figure.subplots_adjust(bottom=0.4)
            ax.set_xlabel("")
            return figure, ax

        self.courtageLineFigure, self.courtageLineAx = genericGraph(self.bottomframe)
        self.courtageBarFigure, self.courtageBarAx = genericGraph(self.bottomframe)

        self.depositLineFigure, self.depositLineAx = genericGraph(self.depositsframe)
        self.depositBarFigure, self.depositBarAx = genericGraph(self.depositsframe)

        #updates embedded graphs on button click
    def updateCourtageGraphs(self):
        # Line graph
        self.courtageLineAx.clear()
        self.avanza.courtageGraph(self.newStartDate, self.newEndDate)\
                .plot(legend=True, ax=self.courtageLineAx)
        self.courtageLineFigure.canvas.draw_idle()
        self.courtageLineFigure.autofmt_xdate()
        self.courtageLineAx.set_xlabel("")
        # Bar graph
        self.courtageBarAx.clear()
        self.avanza.stockBrokerage(self.newStartDate, self.newEndDate).head(10).\
                plot(kind="bar",legend=True, ax=self.courtageBarAx)
        self.courtageBarFigure.canvas.draw_idle()
        self.courtageBarFigure.autofmt_xdate()
        self.courtageBarAx.set_xlabel("")
        
    def updateDepositGraphs(self):
        self.depositLineAx.clear()
        self.avanza.depositsLineData(self.newStartDate, self.newEndDate)\
            .plot(legend=True, ax=self.depositLineAx)
        self.depositLineFigure.canvas.draw_idle()
        self.depositLineFigure.autofmt_xdate()
        self.depositLineAx.set_xlabel("")

        self.depositBarAx.clear()
        self.avanza.depositsMonthlyGraph(self.newStartDate, self.newEndDate)\
            .plot(kind="bar", legend=True, ax=self.depositBarAx)
        self.depositBarFigure.canvas.draw_idle()
        self.depositBarFigure.autofmt_xdate()
        self.depositBarAx.set_xlabel("")


 
if __name__ == "__main__":
    gui = App()

root.mainloop()
