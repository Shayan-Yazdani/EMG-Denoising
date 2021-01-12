#Written by Shayan Yazdani

import tkinter
from tkinter import *
from tkinter import filedialog, messagebox
import numpy as np
from denoiseEMG import EMGden 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl

class Window:       
        def __init__(self, master):
            self.master = master
            master.title("EMG Interfrence Removal") 
            self.filetxt=""
            self.currentnumber=0
            self.EMG_clean=""
            self.ECG=""
            self.var=IntVar()
            self.fs_entry = Entry(root,textvariable=self.var)
            self.fs_entry.place(x=20, y=120)
            self.bbutton= Button(root, text='Enter fs (Hz)', command=self.get_fs, height = 1, width = 9,bg="yellow green").place(x=20, y=90)
            self.bbutton= Button(root, text="Upload file", command=self.browsetxt,  height = 1, width = 9,bg="yellow green")
            self.bbutton.place(x=20, y=20)
            self.bbutton= Button(root, text="Denoise", command=self.applyf,  height = 1, width = 9, bg="yellow green")
            self.bbutton.place(x=20, y=170)
            self.bbutton= Button(root, text="Save EMG", command=self.saveEMG, height = 1, width = 9, bg="yellow green")
            self.bbutton.place(x=20, y=240)
            self.bbutton= Button(root, text="Save ECG", command=self.saveECG, height = 1, width = 9, bg="yellow green")
            self.bbutton.place(x=20, y=290)
            self.bbutton= Button(root, text="Next", command=self.next_part, height = 1, width = 6, bg="yellow green")
            self.bbutton.place(x=390, y=535)
            self.bbutton= Button(root, text="Previous", command=self.pre_part, height = 1, width = 6, bg="yellow green")
            self.bbutton.place(x=320, y=535)
            
            
        def browsetxt(self):
         
            Tk().withdraw() 
            self.filename = filedialog.askopenfilename()
            if self.filename:
                self.filetxt = np.loadtxt(self.filename)
                self.EMG_clean=""
                self.ECG=""
                self.fs=""
            self.pltnumber=np.round(self.filetxt/2000)
            self.currentnumber=0
            self.plot_sig()
            
            
        def applyf(self):
            
            if self.fs:
                self.ECG, self.EMG_clean = EMGden(self.filetxt, self.fs)
                self.plot_sig()
            else:
                messagebox.showerror("Error", "First enter fs")
                
            
        def next_part(self):
            
            if(len(self.filetxt) > 0):
                self.currentnumber=self.currentnumber+1
                self.plot_sig()
                
                
        def pre_part(self):
            
            if(len(self.filetxt) > 0):
                self.currentnumber=self.currentnumber-1
                self.plot_sig()
                
               
        def plot_sig(self):
            
            figure = Figure(figsize=(6, 5), dpi=100)
            plot1= figure.add_subplot(3, 1, 1)
            plot2= figure.add_subplot(3, 1, 2)
            plot3= figure.add_subplot(3, 1, 3)
            plot1.set_xlim([(self.currentnumber)*2000, (self.currentnumber+1)*2000])
            plot1.set_title('EMG_contaminated')
            plot1.plot(self.filetxt)
            plot2.set_xlim([(self.currentnumber)*2000, (self.currentnumber+1)*2000])
            plot2.set_title('EMG_final')
            plot2.plot(self.EMG_clean)
            plot3.set_xlim([(self.currentnumber)*2000, (self.currentnumber+1)*2000])
            plot3.set_title('ECG_final')
            plot3.plot(self.ECG)
            figure.subplots_adjust(hspace = 1)
            figure.set_facecolor((.18, .18, .18))
            COLOR = 'white'
            mpl.rcParams['text.color'] = COLOR
            mpl.rcParams['axes.labelcolor'] = COLOR
            mpl.rcParams['xtick.color'] = COLOR
            mpl.rcParams['ytick.color'] = COLOR
            canvas = FigureCanvasTkAgg(figure, root)
            canvas.get_tk_widget().place(x=90, y=20)
            
            
        def saveEMG(self):
            
            filepath1 = filedialog.asksaveasfile(defaultextension=".txt")
            if filepath1:
                np.savetxt(filepath1.name, self.EMG_clean)
                
        def saveECG(self):
            
            filepath2 = filedialog.asksaveasfile(defaultextension=".txt")
            if filepath2:
                np.savetxt(filepath2.name, self.ECG)
            
        def get_fs(self):
            
            self.fs=self.fs_entry.get()
        
        

if __name__ == "__main__": 
    root = Tk()
    root.configure(background='gray18')
    root.geometry("700x600")
    window=Window(root)
    window.plot_sig()
    root.mainloop()  