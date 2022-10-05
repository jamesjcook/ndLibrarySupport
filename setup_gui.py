# should be a simple gui with a text box for input and an OK button
# text box should take in a string containing project_code and runno, separated by any delimiter
# then, should just simply run our batch script 
#from tkinter import *
#from tkinter import ttk
import tkinter as tk
import os

# this needs to be before the Button(command = startup) line because otherwise it cannot find the function it wants to run
def startup():
    project_code = project_code_var.get()
    runno = runno_var.get()

    print("project code: {}\nrunno: {}".format(project_code, runno))

    os.system(r"C:\Users\hmm56\Documents\civm_data_review\19.gaj.43\start_1_BXD45.bat")

root = tk.Tk()
# setting the windows size
root.geometry("600x400")

# declaring string variable
project_code_var=tk.StringVar()
runno_var=tk.StringVar()



# frm is short for frame
frm = tk.Frame(root)
frm.grid()
tk.Label(frm, text="Project Code:", font = ('calibre',10,'bold')).grid(column=0, row=0)
tk.Entry(frm, textvariable=project_code_var).grid(column=1, row=0)
tk.Label(frm, text="Run Number:", font = ('calibre',10,'bold')).grid(column=0, row=1)
tk.Entry(frm, textvariable=runno_var).grid(column=1, row=1)

tk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=1)
tk.Button(frm, text="startup", command=startup).grid(column=2, row=0)

root.mainloop()