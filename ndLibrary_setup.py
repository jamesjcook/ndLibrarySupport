# should be a simple gui with a text box for input and an OK button
# text box should take in a string containing project_code and runno, separated by any delimiter
# then, should just simply run our batch script 
#from tkinter import *
#from tkinter import ttk
import tkinter as tk
import os
import logging
# always have workstation_data and wokrstation_home
# if these below are here, we are fully setup
# (RADISH_PERL_LIB BIGGUS_DISKUS WORKSTATION_DATA WORKSTATION_HOME)
logger=logging.getLogger("ndLibrary")

template = "conf_templates/atlas_comparison/project_code"

# this needs to know about workstation_home etc
#self.logger.warning(os.environ) # it is a dict


def check_for_variables(env_variable_list):
    vars_found = 0
    for var in env_variable_list:
        if os.environ[var] is not None and os.environ[var] is not "":
            vars_found += 1
    if vars_found < len(env_variable_list):
        return False
    return True

def environment_setup():
    """checks for required environment varibales. if not found, run the workstation_setup code
    Returns True if environment is already setup or setup is sucessful
    returns false if setup failed"""
    env_variable_list = "RADISH_PERL_LIB BIGGUS_DISKUS WORKSTATION_DATA WORKSTATION_HOME".split(" ")
    if check_for_variables(env_variable_list):
        return True
    else: 
        # TODO: this will ask user to input biggus_diskus
        # makle sure really the right workstaiton_home(reoranization--home or code?)
        cmd = r"bash -c \"cd $WORKSTATION__HOME; ./install.pl --only=shell\""
        os.system(cmd)
    
    # after setup has run, check again to make sure it ran sucessfully
    if check_for_variables(env_variable_list):
        return True
    else: 
        return False

def find_data_in_archive():
    # we know where windows helpoer scripts are to connect to archive as A
    # want connectome results
    # test for A:/ path, if it is not found, then run mounta script
    # os.system(connect.bat)

    # find runno of interest
    # .? means an optional single character
    #A:/project_code/research/connectome.?${runno}.?dsi_studio*
    # also need dwi and b0avg from the diffusion folder 

    # ccheck for connectome*/nhdr
    # and diffusion*/nhdr
    # if its missing, do (tbd) tricks
    # (we're not sure lndir is a good idea)link these to a phony dir in home, thern we can run diffusion_generate_nhdr
    # lndir # this is now put in $WKS_BIN
    # if environment_setup() passes, then lndir will work
    # lndir does not make the main directory (we think) but does for children
    # HOLD ON, we want nhdrs IN our connectome/diffusion folders in the archive! We dont want users re-generating them all the time!
    # diffusion_generate_nhdr input=A:/project_code/... output=~/divm_data_review/proejct_code/...

    # nhdr folder exists, and is ready.
    # replicate template conf to our libdir
    # create data setup in users home documenbts
    # "C:\Users\hmm56\Documents\civm_data_review\19.gaj.43
    # make civm_data_review if missing, project code and other folders also
    
    pass

# this needs to be before the Button(command = startup) line because otherwise it cannot find the function it wants to run
def startup():
    project_code = project_code_var.get()
    runno = runno_var.get()

    logger.warning("project code: {}\nrunno: {}".format(project_code, runno))

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
tk.Label(frm, text="Project Code:", font = ('calibre',14,'bold')).grid(column=0, row=0)
tk.Entry(frm, textvariable=project_code_var, font = ('calibre',14,'bold')).grid(column=1, row=0)
tk.Label(frm, text="Run Number:", font = ('calibre',14,'bold')).grid(column=0, row=1)
tk.Entry(frm, textvariable=runno_var, font = ('calibre',14,'bold')).grid(column=1, row=1)

tk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=1)
tk.Button(frm, text="startup", command=startup, font = ('calibre',30,'bold')).grid(column=1, row=3)

root.mainloop()