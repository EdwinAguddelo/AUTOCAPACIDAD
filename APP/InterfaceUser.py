from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import SetupPath
import InitDataFrames
import Process

class Application():
    def __init__(self, master):
        frame = Frame(master,width=3000,height=3000)
        frame.pack()

        self.insert_file_path_btn = Button(frame, text="Carpeta", command=self.selectLogFile, width=18)
        self.insert_file_path_btn.place(x=190,y=80)
        self.qc_start_proccess_btn = Button(frame,text="Ejecutar",command=self.start, width=18)
        self.qc_start_proccess_btn.place(x=190,y=110)

        self.logFilePath =StringVar()
        self.label = Label(frame,text="Número mes vencido:")
        self.label.place(x=60,y=40)

        self.mes = StringVar()
        self.txtmes = Entry(frame,textvariable=self.mes,width=22).place(x=190,y=40)


        self.logFilePathMessage =StringVar()
        self.labelMessage = Label(frame,textvariable=self.logFilePathMessage)
        self.labelMessage.place(x=190,y=140)

        self.logFilePath =StringVar()
        self.label = Label(frame,textvariable=self.logFilePath)
        self.label.place(x=190,y=20)

    def selectLogFile(self):
        filename = filedialog.askdirectory()
        self.logFilePath.set(filename)


    def start(self):
     self.logFilePathMessage.set("")
     if self.logFilePath.get() and self.mes.get():

        path = SetupPath.pathFiles(self.logFilePath.get())
        init_dataframes = InitDataFrames.InitDataFrames(path)
        Process.mainProcess(init_dataframes,self.mes.get())

     else:
        self.logFilePathMessage.set("Seleccione la Carpeta Resources y ponga el mes")







if __name__=="__main__":

    root = Tk()
    root.title("Indicadores Capacidad")
    root.geometry("500x400+410+180")
    root.grid_anchor(anchor="nw")
    app = Application(root)
root.mainloop()
