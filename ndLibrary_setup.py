# should be a simple gui with a text box for input and an OK button
# text box should take in a string containing project_code and runno, separated by any delimiter
# then, should just simply run our batch script
#from tkinter import *
#from tkinter import ttk
from email.policy import default
import tkinter as tk
import os
import subprocess
import logging
import shutil
import re
from collections import OrderedDict
import fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

class ndLibrary_setup():
    def __init__(self):
        root = tk.Tk()
        self.root=root
        self.logger=logging.getLogger("ndLibrary")
        self.script_dir="{}/code/display/ndLibrarySupport".format(os.environ["WORKSTATION_HOME"])
        self.template = "{}/conf_templates/atlas_comparison/project_code".format(self.script_dir).replace(r'\\','/').replace('//','/')
        self.slicer_exe_path = None
        self.data_dir = None # or empty string?
        self.checkboxes = None
        self.display_path_button = None

        sys_drives = [ r'L:\\', r'K:\\', r'D:\\', r'C:\\' ]
        base_path = None
        for sd in sys_drives:
          sd=os.path.join(sd,r'CIVM_Apps')
          if os.path.exists(sd):
            base_path = sd
          #else:
          #  print("no {}".format(sd))
        self.slicer_exe_path=r'{}\Slicer\4.11.20200930\Slicer.exe'.format(base_path)
        if not os.path.exists(self.slicer_exe_path):
          print('Bad slicer path {}'.format(self.slicer_exe_path))
          return

        self.data_organization = None
        od=OrderedDict()
        od["base_dir"]=tk.StringVar()
        od["project_code"]=tk.StringVar()
        od["p_sub"]=tk.StringVar()
        od["data_pattern"]=tk.StringVar()
        #od["data_suffix"]=tk.StringVar()
        #od["trail"]=tk.StringVar()# -results?
        # set default values
        # save previous values in a local file, use these as defaults next time
        od["base_dir"].set("A:/")
        od["project_code"].set("20.5xfad.01")
        od["p_sub"].set("research")
        od["data_pattern"].set("connectomeRUNNOdsi_studio/nhdr")
        #od["data_suffix"].set("")
        #od["trail"].set("")# -results?"""
        self.data_organization=od

        self.adv_panel = None
        # setting the windows size
        root.geometry("600x400")
        if 0 :
            w = tk.Label(root, text="Red Sun", bg="red", fg="white")
            w.pack()
            w = tk.Label(root, text="Green Grass", bg="green", fg="black")
            w.pack()
            w = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
            w.pack()


        # declaring string variable
        self.project_code_var=tk.StringVar()
        self.runno_var=tk.StringVar()
        self.runno_var.set("N58840NLSAM")
        # frm is short for frame
        frm=root

        frm = tk.Frame(root);frm.grid()
        project_code_label = tk.Label(frm, text="Project Code:", font = ('calibre',14,'bold'))
        project_code_entry = tk.Entry(frm, textvariable=self.data_organization["project_code"], font = ('calibre',14,'bold'), width=40)
        runno_label = tk.Label(frm, text="Run Number:", font = ('calibre',14,'bold'))
        runno_entry = tk.Entry(frm, textvariable=self.runno_var, font = ('calibre',14,'bold'), width=40)
        start_button = tk.Button(frm, text="startup", command=self.startup, font = ('calibre',30,'bold'))
        quit_button = tk.Button(frm, text="Quit", command=root.destroy)
        adv_button = tk.Button(frm, text="...", command=self.show_adv_panel)

        c=0;r=0;
        project_code_label.grid(column=c,row=r);  c+=1;  project_code_entry.grid(column=c,row=r)
        c=0; r+=1
        runno_label.grid(column=c,row=r);  c+=1;  runno_entry.grid(column=c,row=r)
        c=0; r+=1
        start_button.grid(column=c,row=r);  c+=1;
        c=0; r+=1
        quit_button.grid(column=c,row=r);  c+=1;  adv_button.grid(column=c,row=r)
        print("{} {} ".format(c, r))

        root.mainloop()
    def cleanup_adv_panel(self):
        self.adv_panel.destroy()
        self.display_path_button = None
        #self.checkboxes = None
        self.adv_panel = None

    def show_adv_panel(self):
        # only allow for one advanced menu panel to show
        if self.adv_panel is not None:
            return

        # Toplevel object which will be treated as a new window
        adv_panel = tk.Toplevel(self.root); adv_panel.grid()
        # sets the title of the Toplevel widget
        adv_panel.title("data organization")
        c=0; r=0
        # checkboxes determine whether or not that field goes in to the data path or not
        #checkboxes[key] is NOT a checkbox itself, it holds the boolean value of the checkbox
        checkboxes = OrderedDict()
        for entry in self.data_organization.keys():
            tk.Label(adv_panel, text=entry, font = ('calibre',14,'bold')).grid(column=c, row=r);  c=c+1;  tk.Entry(adv_panel, textvariable=self.data_organization[entry], font = ('calibre',14,'bold'), width=40).grid(column=c, row=r)
            c=c+1
            checkboxes[entry] = tk.IntVar()
            temp_button = tk.Checkbutton(adv_panel, variable=checkboxes[entry], command=self.update_path_display)
            temp_button.grid(column=c,row=r)
            temp_button.select()
            #checkboxes[entry] = tk.Checkbutton(adv_panel, command=self.update_path_display)
            #checkboxes[entry].grid(column=c,row=r)
            #checkboxes[entry].select()
            r=r+1
            c=0
        # creates a button that dynamically displays the resulting search directory
        self.display_path_button = tk.Button(adv_panel, text=self.data_dir, command=self.cleanup_adv_panel)
        self.display_path_button.grid(column=c, row=r)
        self.checkboxes = checkboxes

        self.update_path_display()


        tk.Button(adv_panel, text="Update Path", command=self.update_path_display).grid(column=c, row=r+1)

        # need to be configuratble patternizaingatairoetoieanognan for ou r connectome folders
        #base dir
        #layers of stuff...
        # array ?
        #data_dir = "{}/{}/research/connectome{}dsi_studio/nhdr".format(data_dir, self.project_code, self.runno)



        self.adv_panel = adv_panel

    def update_path_display(self):
        from tkinter import messagebox
        # should update self.display_path
        l = []
        for key in self.data_organization.keys():
            if self.checkboxes is None or self.checkboxes[key].get():
                l.append(self.data_organization[key].get())
        self.data_dir = os.path.join(*l)
        if self.display_path_button is not None:
            self.display_path_button.config(text=self.data_dir)
        if "RUNNO" not in self.data_organization["data_pattern"].get():
            messagebox.showerror("data_pattern error","literal 'RUNNO' is required in the search pattern")
        pass

    # always have workstation_data and wokrstation_home
    # if these below are here, we are fully setup
    # (RADISH_PERL_LIB BIGGUS_DISKUS WORKSTATION_DATA WORKSTATION_HOME)


    # this needs to know about workstation_home etc
    #self.logger.warning(os.environ) # it is a dict
    #logger.warning(os.environ["WORKSTATION_DATA"])

    def check_for_variables(self, env_variable_list):
        vars_found = 0
        for var in env_variable_list:
            # TODO: this fails, if the var key is not in environ, then this throws error
            if var in os.environ and os.environ[var] is not None and os.environ[var] != "":
                vars_found += 1
        if vars_found < len(env_variable_list):
            return False
        return True

    def environment_setup(self):
        """checks for required environment varibales. if not found, run the workstation_setup code
        Returns True if environment is already setup or setup is sucessful
        returns false if setup failed"""
        # thought we needed this to do data curation prep
        # but now we arn not letting that happen int this script
        # once this runs, assumed that data curation is ready (nhdr exist and transforms exist)
        # thjis script still creates lib.conf directories in users HOME
        return True
        env_variable_list = "RADISH_PERL_LIB BIGGUS_DISKUS WORKSTATION_DATA WORKSTATION_HOME".split(" ")
        if self.check_for_variables(env_variable_list):
            return True
        else:
            # TODO: this will ask user to input biggus_diskus
            # makle sure really the right workstaiton_home(reoranization--home or code?)
            # -l is login mode
            cmd = r"bash -l -c \'cd $WORKSTATION_HOME; ./install.pl --only=shell\'"
            os.system(cmd)

        # after setup has run, check again to make sure it ran sucessfully
        if self.check_for_variables(env_variable_list):
            return True
        else:
            return False

    def archive_connect(self,basedir="A:"):
        if not os.path.exists(basedir) and re.match("^A:.*", basedir):
            # then mount A
            var="WORKSTATION_HOME"
            drive=""
            if var in os.environ and os.environ[var] is not None and os.environ[var] != "":
                # tjem we have it
                import pathlib
                drive = pathlib.Path(os.environ[var]).drive
                print(drive)
                # drive isnt handled proerly here, so you need to add literal slashes
                # probably safe =because other OS do not have drives
                archive_connector = os.path.join(drive,"/", "civm_apps", "network_shares", "connect_A_civm_archive.bat")
                self.logger.warning(archive_connector)
                os.system("{} 0 ".format(archive_connector))
            else:
                msg="Couln't auto connect archive for you"
                print(msg)
                self.logger.warning(msg)
        if not os.path.exists(basedir):
            self.logger.warning("ERROR: unable to mount the archive.")
            #exit()


    def find_data(self, basedir="A:"):
        data_dir = basedir
        # we know where windows helpoer scripts are to connect to archive as A
        # want connectome results
        # test for A:/ path, if it is not found, then run mounta script
        # os.system(connect.bat)
        self.archive_connect(basedir)
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


        # TODO: use os.path.join
        data_dir = "{}/{}/research/connectome{}dsi_studio/nhdr".format(data_dir, self.project_code, self.runno)
        #data_dir = "{}/{}/connectome{}dsi_studio/nhdr".format(data_dir, self.runno)
        self.logger.warning(data_dir)
        if os.path.exists(data_dir):
            os.listdir(data_dir)
            return(data_dir)
        else:
            return None

        pass

    # this needs to be before the Button(command = startup) line because otherwise it cannot find the function it wants to run
    def startup(self):
        self.runno = self.runno_var.get()
        if self.environment_setup():
            self.logger.warning("SETUP PASSED")
        else:
            self.logger.warning("SETUP FAILURE")
        """# if self.data_organization is not None, then use it's path instead, else run find_data
        # nono, checking if self.data_dir is not None is sufficient
        if self.data_dir is None:
            self.logger.info("Searching for your data...")
            self.data_dir = self.find_data()
            if self.data_dir is None:
                self.logger.error("cannot find data directory. are you sure A is mounted?")
                return
        else:
            self.logger.info("Using path defined in advanced configuration menu...:\n\t{}".format(self.data_dir))
            print(self.data_dir)"""
        self.update_path_display()
        self.data_dir = self.data_dir.replace("RUNNO", self.runno)
        self.logger.warning(self.data_dir)
        self.archive_connect(self.data_dir)
        # replicate conf templates within lib conf dir
        self.project_conf_dir = os.path.join(os.environ["USERPROFILE"], "civm_data_review", self.data_organization["project_code"].get())
        # check for these guys
        specimen_selections_dir = os.path.join(self.project_conf_dir, "specimen_selections")
        self.runno_conf_dir = os.path.join(specimen_selections_dir, self.runno)
        if not os.path.exists(self.project_conf_dir):
            os.makedirs(self.project_conf_dir)
            shutil.copy(os.path.join(self.template, "lib.conf"), os.path.join(self.project_conf_dir, "lib.conf"))
            # copy whole specimen_selections folder
            template_specimen_selections_dir = os.path.join(self.template, "specimen_selections")
            shutil.copytree(template_specimen_selections_dir, specimen_selections_dir)
            shutil.copytree(os.path.join(self.template, "atlas"), os.path.join(self.project_conf_dir, "atlas"))

            files = [f for f in os.listdir(specimen_selections_dir) if not re.match(r'template|lib\.conf|\.\.?', f)]
            for f in files:
                shutil.rmtree(os.path.join(specimen_selections_dir,f))
        specimen_template=os.path.join(specimen_selections_dir,"template")
        if not os.path.exists(self.runno_conf_dir) and os.path.exists(self.data_dir) and os.path.exists(specimen_template):
            shutil.copytree(specimen_template,self.runno_conf_dir)
            transform_files = find("*.mat", os.path.join(self.data_dir, "transforms"))
            with open(os.path.join(self.runno_conf_dir, "lib.conf"), "a") as f:
                f.write("Path={}\n".format(self.data_dir))
                if transform_files is not None:
                    f.write("OriginTransform={}\n".format(transform_files[0].replace("\\","/")))
        else:
          if not os.path.exists(specimen_template):
            print("Error finding spec template {}".format(specimen_template))
          if not os.path.exists(self.data_dir):
            print("Error no data dir {}".format(self.data_dir))

        # TODO: update atlas lib conf, must use correct voxel size

        # build the lib starter
        cmd = r'{} --python-script "{}/ndLibrarySupportMain.py" -l "{}" --data_package "{}"'.format(self.slicer_exe_path, self.script_dir, self.project_conf_dir, self.runno)
        #cmd = r'L:\CIVM_Apps\Slicer\4.11.20200930\Slicer.exe --python-script "L:\workstation\code\display\ndLibrarySupport\ndLibrarySupportMain.py" -l "{}" --data_package "{}"'.format(self.project_conf_dir, self.runno)
        #cmd = r'L:\CIVM_Apps\Slicer\5.0.3\Slicer.exe --python-script "L:\workstation\code\display\ndLibrarySupport\ndLibrarySupportMain.py" -l "{}" --data_package "{}"'.format(self.project_conf_dir, self.runno)
        #os.system(cmd)
        s_output=subprocess.Popen(cmd);
        # this will be the last call to make
        #os.system(r"C:\Users\hmm56\Documents\civm_data_review\19.gaj.43\start_1_BXD45.bat")
    print(2)

setupper = ndLibrary_setup()
