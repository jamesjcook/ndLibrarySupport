## Class for a library of data
## NOTE: Assumes files are in a Windows system
## Author: Austin Kao
import sys
import os
import re
import logging

import ndLibrarySupport

class ndLibrary:        
    ## Constructor for a ndLibrary
    ## parent: The parent ndLibrary
    ## file_loc: The full path of the ndLibrary
    ## conf: A dictionary populated with name-value pairs found in lib.conf
    ## recursion_field: String used to identify uses of recursion
    ## conf_file_name: String that stores the default name of a conf file (lib.conf)
    ## labelDict: A dictionary populated with the labels found in a lookup table file
    ## valid: A field that tells if an ndLibrary object is valid for use (Needs to pass the initial checks)
    def __init__(self, parent, file_loc):
        self.valid = False
        ## set log bits so we can easily spam regex info for debug
        #logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        self.logger=logging.getLogger("ndLibrary")
        #handler = logging.StreamHandler()
        #self.logger.addHandler(handler)
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #formatter = logging.Formatter('%(message)s')
        #handler.setFormatter(formatter)
        # simple way to flag logging on/off
        # set value to logging.DEBUG INFO WARNING ERROR
        #self.logger.setLevel(logging.DEBUG)
        #self.logger.setLevel(logging.INFO)
        #self.logger.setLevel(logging.WARNING)
        # TODO: support libs as files as well as dir
        if not os.path.isdir(file_loc):
            print('Not a directory')
            return
        self.conf_dir=file_loc
        self.conf_file_name = "lib.conf"
        self.conf_path = None
        # TODO: adjust all the special field handlers to be simply read from the field.
        #       Perhaps they should be accessors? 
        #       Or we should craft a special operator to get access to conf?
        self.recursion_field = "RecursiveLoad"
        self.path_field = "Path"
        # filter child/vol discovery 
        self.filter_field = "FilePattern"
        # carve filename into parts 
        self.pattern_field = "FileAbrevPattern"
        # pull parts of carved filename with this match info
        self.match_field = "FileAbrevMatch"
        self.vol_ordering = "PreferedImgTypeAbbrevOrder"
        if isinstance(parent, type(self)):
            self.conf = parent.conf.copy()
            if self.path_field in self.conf:
                del self.conf[self.path_field]
            self.conf["Category"]=self.conf["ChildCategory"]
            del self.conf["ChildCategory"]
            del self.conf["LibName"]
        elif parent is None:
            self.conf = ndLibrarySupport.conf("blank")
            pass
        else:
            print("Parent is invalid")
            return
        #self.valid = True
        self.parent = parent
        self.file_loc = file_loc
        self.children = list()
        # TODO: replace is_leaf with function checking child count
        self.is_leaf = False
        # TODO: instead of volDict, add "node" field to definition, and the children will be ndLib nodes all the way down to the independent volumes, we'll update path as well to be the "fully-resolved" path to file.
        self.volDict = None
        self.labelDict = None
        self.labelVolume = None
        self.colorTable = None
        self.originTransform = None
        self.relevantStrainLib = False
        #if self.pattern_field in self.conf:
        #    del self.conf[self.pattern_field]
        #if self.match_field in self.conf:
        #    del self.conf[self.match_field]
        self.extensionPriority = list(["nhdr", "nrrd", "nii.gz", "nii", "png", "tif", "jpg", "gif", "bmp"])
        self.extReg = r".+[.]"+'(% s)' % '|'.join([sub.replace('.', '[.]') for sub in self.extensionPriority])+"$"
        ## Have ndLibrary automatically build the ndLibrary tree if it is a root?
        if parent == None:
            # to make life easier we're gonna dict transforms, but only in the oldest ancestor(the progenitor).
            self.transforms = dict()
            #self.logger.debug('debug message')
            #self.logger.info('info message')
            #self.logger.warning('warn message')
            #self.logger.error('error message')
            #self.logger.critical('critical message')
            self.loadEntire()
    
    ## Method to load a lib.conf file for a ndLibrary and store the name-value pairs it contains
    def loadConf1(self, file):
        try:
            conf = open(file)
        except:
            print("Could not open conf file"+file)
            return
        self.conf_path=file
        line = conf.readline()
        while line is not "":
            is_comment = False
            components = line.split("=")
            if line[0] == "#":
                #print("Comment encountered")
                is_comment = True
            if len(components) == 2 and is_comment == False:
                name = components[0]
                value = components[1].replace("\n", "")
                self.conf[name] = value
            line = conf.readline()

    ## Method to load a lib.conf file for a ndLibrary and store the name-value pairs it contains
    def loadConf(self, file=None):
        if file is None:
            file=self.conf_path
        with open(file) as fp:
            # do stuff with fp
            for cnt, line in enumerate(fp):
                components = re.match(r"^([^#=]*)(?:=([^#]+))?(#.*)?$",line)
                key=components.group(1)
                value=components.group(2)
                comment=components.group(3)
                if key is not None and value is not None:
                    self.conf[key.strip()] = value.strip()
                elif (key is None or not key) and (value is None or not value):
                    #print("Ignore line:"+line.strip())
                    pass
                elif key is None:
                    print("conf error: bad key, value is "+value.strip())
                elif value is None:
                    print("conf error: bad value, key is "+key.strip())
        # clean up routine typeo, except its so pervasive... 
        #if self.pattern_field not in self.conf and "FileAbrevPattern" in self.conf:
        #    self.pattern_field = "FileAbrevPattern"
        #    self.conf[self.pattern_field]=
        #if self.match_field not in self.conf and "FileAbbrevMatch" in self.conf:
        #    self.match_field = "FileAbrevMatch"
        self.conf_path = file

    ## Method to find and make child ndLibraries
    def buildChildren(self):
        # this is incomplete! recusive load is not cutting the end of the branch, it is do we continue loading our child.
        if self.recursion_field in self.conf and self.conf[self.recursion_field] == "false":
            #print("Reached leaf of tree. No children")
            self.is_leaf = True
            return
        #if (self.recursion_field in self.conf and self.conf[self.recursion_field] == "true"
        #    and self.path_field in self.conf and os.path.isdir(self.conf[self.path_field])):        
        #        #print("Going on another path: {}".format(self.conf[self.path_field]))
        #        os.chdir(self.conf[self.path_field])
        if self.filter_field in self.conf:
            filter = self.conf[self.filter_field]
        else:
            self.logger.info("Lib very promiscuous has no filter: "+self.conf_dir)
            filter = ".*"
        self.jumpToDir()
        neighborhood = os.getcwd()
        for entry in os.listdir(neighborhood):
            #self.jumpToDir()
            if os.path.isdir(os.path.join(neighborhood, entry)) and re.match(r''+filter, entry):
                child_lib = ndLibrary(self, os.path.join(neighborhood, entry))
                child_lib.loadEntire()
                if child_lib.isValid():
                    self.children.append(child_lib)
                    #print(os.path.join(self.conf_dir, entry))
        if len(self.children) == 0:
            self.is_leaf = True
    
    ## Method to load the entire ndLibrary tree
    ## Loads a conf file, makes all possible child ndLibraries, and repeats the process for each child
    def loadEntire(self):
        conf_path = os.path.join(self.file_loc, self.conf_file_name)
        if self.file_loc is not None and os.path.isfile(conf_path):
            self.valid = True
            #self.conf_path = conf_path
            #print(self.conf_dir)
            #before we subclassed dict
            #self.conf=ndLibrarySupport.conf(conf_path)
            #self.conf=self.conf.fields.copy()
            par_conf=self.conf.copy()
            #par_conf["Category"]=par_conf["ChildCategory"]
            #del par_conf["ChildCategory"]
            self.conf = ndLibrarySupport.conf(conf_path,self.conf_file_name,par_conf)
            if "LibName" not in self.conf:
                libName = os.path.basename(self.file_loc)
                ext = re.match(r''+self.extReg, libName)
                if ext is not None:
                    ext=ext.group(1)
                    libName = libName.replace(r"."+ext,"")
                #if self.pattern_field not in self.conf:
                #    self.conf[self.pattern_field]="(.*)"
                #if self.match_field not in self.conf:
                #    self.conf[self.match_field]=r"\1"
                #try:
                #    match_text=re.sub(self.conf[self.pattern_field], self.conf[self.match_field], libName.lower())
                #except:
                #    self.logger.error("regex error "+self.conf[self.match_field]+" or "+self.conf[self.pattern_field]+" in conf:"+conf_path )
                self.conf["LibName"]=libName
            self.conf_path = conf_path
            #self.loadConf(conf_path)
            self.determineRelevance()
            if not self.valid:
                return
            self.jumpToDir()
            self.Path=os.getcwd()
            self.loadOriginTransform()
            self.loadVolumes()
            self.loadLabels()
            self.buildChildren()
            
            #for child in self.children:
            #    child.loadEntire()
            #for i in xrange(len(somelist) - 1, -1, -1):
            #    #element = somelist[i]
            #for c in range(len(self.children) - 1, -1, -1):
            #    if not self.children[c].isValid():
            #        del self.children[c]
        else:
            print("Not loading for {}".format(self.file_loc))
    
    ## Determines whether or not current ndLibrary is relevant enough for a menu of data packages
    ## Meant to be called after loading lib.conf file when building the entire tree
    ## May get incorrect result if used in other circumstances
    def determineRelevance(self):
        if "TestingLib" in self.conf and self.conf["TestingLib"].lower() == "true":
            self.relevantStrainLib = False
            self.valid = False
        elif "Category" in self.conf and self.conf["Category"] == "Species":
            #and "Strain" in self.conf):
            self.relevantStrainLib = True
        #print("{} is {}".format(self.file_loc, self.relevantStrainLib))
    
    ## Function to change the working directory according to the path specfied in a lib.conf file
    ## By default, the function will change the working directory to the ndLibrary's directory
    def jumpToDir(self):
        os.chdir(self.conf_dir)
        #if self.conf.has_key(self.path_field):
        if self.path_field in self.conf:
            # CANT BE BOTHERD TO SORT THIS OUT SMART(right now)
            relativePath = self.conf[self.path_field]
            winnie_path = self.conf[self.path_field].replace("/","\\")
            nix_path = self.conf[self.path_field].replace("\\","/").replace("//","/")
            if not os.path.isdir(relativePath) and os.path.isdir(winnie_path):
                relativePath = winnie_path
            if not os.path.isdir(relativePath) and os.path.isdir(nix_path):
                relativePath = nix_path
            if os.path.isdir(relativePath):
                os.chdir(relativePath)
                #print("Jumping to {}".format(os.getcwd()))
            else:
                print("Path jump error from "+self.conf_dir+" to "+relativePath)
                self.valid = False
        #if self.conf_dir == os.path.getcwd():
        #    return True
        #return False
    ## get list of all ancestors starting at parent
    def ancestorList(self,includeSelf=False):
        ancestors = list()
        lib = self
        if includeSelf:
            ancestors.append(lib)
        while lib.parent is not None:
            ancestors.append(lib.parent)
            lib = lib.parent
        return ancestors
    
    ## print conf
    def print_conf(self):
        for e in self.conf:
            print("\t"+e+"\t= "+self.conf[e])
    ## print the tree below our location
    def printTree(self,indent=None):
        if indent is None:
            indent = ""
        for child in self.children:
            if not child.isValid():
                print("invalid child"+child.conf_dir)
            try:
                volCount = len(child.volDict)
            except:
                volCount = 0
            print(indent+os.path.basename(child.file_loc)+":"+str(volCount))
            try:
                print(indent+"  "+child.Path)
            except:
                print(indent+"  UNBUILT "+child.conf_dir)
            child.printTree(indent+"\t")
    ## print entire connected tree by finding oldest parent
    def printFullTree(self,indent=None):
        lib = self
        while lib.parent is not None:
            lib=lib.parent
        lib.printTree()
    
    ## Function that loads the volumes into a dictionary called volDict
    ## Keys for the dictionary are the type of volume ("fa", "dwi", etc.)
    ## Values are a tuple of (file_path, volume_node) where volume_node is initially None
    ## Libraries will load volumes on demand using the file_path
    ## See get_volume_node method for more details
    ## TODO: adjust name from loadVolumes to more accurate, maybe discover?
    def loadVolumes(self):
        if self.volDict is not None:
            #print("Volumes are already loaded")
            return
        #print("Loading volumes for {}".format(self.file_loc))
        self.jumpToDir()
        #print("\t"+os.getcwd())
        if self.filter_field in self.conf:
            filter = self.conf[self.filter_field]
        else:
            self.logger.info("Lib very permissive: "+self.file_loc)
            filter = ".*"
        if self.pattern_field in self.conf:
            pattern=self.conf[self.pattern_field]
        else:
            pattern="(.*)"
        ## the repPattern is not used directly, so its okay to garble it here.
        if self.match_field in self.conf:
            repPattern=" and "+self.conf[self.match_field]
        else:
            repPattern = ""
        try:
            libEntries = [f for f in os.listdir(os.getcwd()) if re.match(r''+filter, f) and not os.path.isdir(os.path.join(os.getcwd(),f))]
        except re.error:
            self.logger.warning("loadVolumes bad regex " + filter +" for "+os.getcwd())
            return
        if len(libEntries) == 0:
            self.logger.warning("No volumes detected: "+os.getcwd()+" using "+filter+" from conf "+self.conf_path)
            return
        self.volDict = dict()
        volExtPriority = dict()
        self.logger.debug("Carving "+str(len(libEntries))+" vol names into meaning with "+pattern+repPattern);
        #print("Carving "+str(len(libEntries))+" vol names into meaning with "+pattern+repPattern);
        for i in range(0, len(libEntries)):
            libPath = os.path.join(os.getcwd(), libEntries[i])
            ext = re.match(r''+self.extReg, libEntries[i])
            if ext is not None:
              ext=ext.group(1)
            if ext is None:
                self.logger.debug("\tNot expected ext:"+libEntries[i]+" using:"+self.extReg)
                continue
            cExtPriority = self.extensionPriority.index(ext)
            #fileName = libEntries[i].split(".")[0]
            libName = libEntries[i].replace(r"."+ext,"")
            #libName = libEntries[i]
            if self.match_field in self.conf:
                match_text=self.conf[self.match_field]
            else:
                match_text=r"\1"
            #match = re.search(pattern, libName)
            try:
                match_text=re.sub(pattern,match_text,libName.lower())
            except:
                self.logger.error("regex error "+match_text+" or "+pattern+" in conf:"+( o.conf_path for o in self.ancestorList(True)) )
            if match_text is None:
                self.logger.warning("lib name to abrev fail:"+libName)
                #print("lib name to abrev fail:"+libName)
                continue
            #else:
            #    match_text=match.group(1)
            lExtPriority = 100
            if match_text in volExtPriority:
                lExtPriority = volExtPriority[match_text]
            if lExtPriority > cExtPriority:
                self.addToVolDict(libPath, match_text)
                volExtPriority[match_text]=cExtPriority
            else:
                #print("pri ex:"+libName)
                self.logger.debug("\tpriority exclusion, e:"+str(lExtPriority)+" < c:"+str(cExtPriority)+" "+libName+"("+match_text+")")
        if len(self.volDict) == 0:
            self.volDict = None
            #print("No valid files found")
            return
    ## Helper function that handles how a determined path and key are added to the volDict
    def addToVolDict(self, volPath, key):
        ## Check if another name is wanted according to the lib.conf file
        if "LibNameSubstitution" in self.conf and self.conf["LibNameSubstitution"].lower() == "true":
            if key in self.conf:
                key = self.conf[key]
        ## Compare the file extensions if there are conflicting keys
        #if key in self.volDict:
        #    currentExt = self.volDict[key][0].split(".", 1)[-1]
        #    newExt = volPath.split(".", 1)[-1]
        #    for ext in self.extensionPriority:
        #        if ext == newExt:
        #            self.volDict[key] = (volPath, None)
        #            break
        #        if ext == currentExt:
        #            break
        #else:
        #    self.volDict[key] = (volPath, None)
        self.volDict[key] = (volPath, None)
    
    ## Loads in the label volume file for a particular specimen
    ## Loads the lookup table for the different regions of the brain
    def loadLabels(self):
        if self.labelDict is not None and self.colorTable is not None and self.labelVolume is not None:
            print("Labels are already loaded")
            return
        labelPat = r".*[._-]labels[._-].*"
        lookupPat = ".*_lookup[.](?:txt|ctbl)$"
        if self.filter_field in self.conf:
            filter = self.conf[self.filter_field]
        else:
            filter=r".*"
            #print("No files to be found")
            #return
        #print("Loading labels for {}".format(self.file_loc))
        self.jumpToDir()
        try:
            labels = [f for f in os.listdir(os.getcwd()) if re.match(r''+labelPat, f) and re.match(r''+filter, f) and os.path.isfile(f) ]
            clts = [f for f in os.listdir(os.getcwd()) if re.match(r''+lookupPat, f) and re.match(r''+filter, f) and os.path.isfile(f)]
        except re.error:
            print("loadLabels failed on regex match "+labelPat+" and "+filter)
            return
        #if re.match(".*labels.*", os.getcwd()) and ( len(labels) == 0 or len(clts) == 0 ):
        if "labels" in os.getcwd() and ( len(labels) == 0 or len(clts) == 0 ):
            #print("loadLabels unsucecssful, labels found:"+str(len(labels))+" color tables:"+str(len(clts)))
            #print("\t"+os.getcwd()+"  pattern: "+filter+" lbl filter: "+labelPat+" ctbl filter: "+lookupPat)
            return
        extPriority = 100
        for i in range(0, len(labels)):
            f = os.path.basename(labels[i])
            ext = re.match(r''+self.extReg,f)
            if ext is not None:
              ext=ext.groups()[0]
            if ext is None:
                print("Not expected ext:"+f+" using:"+self.extReg)
                continue
            lExtPriority = self.extensionPriority.index(ext)
            if lExtPriority<extPriority:
                labelPath = os.path.join(os.getcwd(), labels[i])
                #print(labelPath)
                self.labelVolume = (labelPath, None)
        if not isinstance(self.labelVolume, tuple):
            #print("Not a tuple. No valid volumes found.")
            return
        ## Assume that the first text file found is the right color lookup table file
        clt_idx=0
        ctbl_file_path=os.path.join(os.getcwd(), clts[clt_idx])
        #print("Found color lookup table")
        self.labelDict = dict()
        if (sys.version_info > (3, 0)):
            # slicer py3 call, nightlies, and future next release
            colorTable = slicer.util.loadColorTable(ctbl_file_path)
        else:
            #slicer py2 call, current release(as of 2020-10) 4.10.2
            [loadSuccess, colorTable] = slicer.util.loadColorTable(ctbl_file_path, returnNode=True)
            if not loadSuccess:
                colorTable = None
        if colorTable is None:
            print("Could not load color lookup table. File: {}".format(clts[clt_idx]))
            return
        self.colorTable = (ctbl_file_path, colorTable)
        ## This loads up and parses the color table manually... that should be completely unnecessary
        ## The dict is required for InteractiveLabelSelector
        ## Count parameter is the number a node will be IF ordered ascendingly
        ## SO, IF INPUT NOT ORDERED ASCENDINGLY THIS IS BROKEN. eg... this is bad...
        ## Replacing with use loaded color table below
        #txt = open(clts[cltIndex])
        # txt = open(clts[clt_idx])
        # count = 0
        # for line in txt:
            # words = line.split()
            # if words[0] is not "#" and len(words) >= 5:
                # try:
                    # self.labelDict[int(words[0])] = (words[1],words[2],words[3],words[4], count)
                # except ValueError:
                    # pass
                # count += 1
        blank='(none)'
        for roi_num in range(0,colorTable.GetNumberOfColors()):
            cname=colorTable.GetColorName(roi_num)
            #cname=colorTable.GetColorNameWithoutSpaces(roi_num,'_')
            # set color 0 to black, and invsisble
            #colorTable.SetColor(0,0,0,0,0)
            # an invalid color which we'll fill in using GetColor(IDX,color_at_idx)
            # r, g, b, alpha
            color_at_idx = [-1,-1,-1,-1]
            # We dont know the row until we the table view is populated! I think we've got our code connected wrong!
            row_num = -1
            # selector.tableView.model().rowCount()
            if cname != blank:
                try:
                    if colorTable.GetColor(roi_num,color_at_idx):
                        # self.labelDict[roi_num] = [cname, row_num, color_at_idx[0],color_at_idx[1],color_at_idx[2]]
                        self.labelDict[roi_num] = [cname, color_at_idx[0],color_at_idx[1],color_at_idx[2]]
                        # self.labelDict[cname] = [roi_num, row_num, color_at_idx[0],color_at_idx[1],color_at_idx[2]]
                        self.labelDict[cname] = [roi_num, color_at_idx[0],color_at_idx[1],color_at_idx[2]]
                    else:
                        print("error color fetching idx "+roi_num+" name:"+cname)
                except ValueError:
                    pass
        parent_lib = self.parent
        ## assign label info to this library and all libraries above this level.
        #print("Found valid labels in {}".format(self.file_loc))
        while parent_lib is not None:
            parent_lib.labelDict = self
            parent_lib.colorTable = self
            parent_lib.labelVolume = self
            parent_lib = parent_lib.parent
    
    ## Function that loads the transform for the volume node
    ## originTransform is a tuple with two elements
    ## Element 0 is the file path for the transform
    ## Element 1 is the transform node in 3D Slicer
    def loadOriginTransform(self):
        if not "OriginTransform" in self.conf:
            #print("No path to follow for origin transform")
            return
        if self.originTransform is not None:
            #print("Track transform is already loaded")
            return
        self.jumpToDir()
        # CANT BE BOTHERD TO SORT THIS OUT SMART(right now)
        originPath = self.conf["OriginTransform"]
        winnie_path = self.conf["OriginTransform"].replace("/","\\")
        nix_path = self.conf["OriginTransform"].replace("\\","/").replace("//","/")
        if not os.path.isdir(originPath) and os.path.isdir(winnie_path):
            originPath = winnie_path
        if not os.path.isdir(originPath) and os.path.isdir(nix_path):
            originPath = nix_path
        if os.path.isfile(originPath):
            # fully resolve the originPath so we can find by path.
            relD=os.path.dirname(originPath)
            if not relD:
                originPath = os.path.join(os.getcwd(), originPath)
            else:
                os.chdir(relD)
                originPath = os.path.join(os.getcwd(), os.path.basename(originPath))
            if os.path.isfile(originPath):
                self.originTransform = (originPath, None)
                #ot=self.getOriginTransform()
            else:
                self.jumpToDir()
                print("error resolving "+self.conf["OriginTransform"]+" in "+os.getcwd()+" for lib "+self.conf_dir)
            #if self.parent is not None and self.parent.originTransform is not None and self.parent.originTransform[1] is not None:
            #    ot.SetAndObserveTransformNodeID(self.parent.originTransform[1].GetID())
        else:
            print("Error on transform resolution:"+originPath+" in "+self.conf_dir)
    ## Returns the origin transform for a given volume
    ## Loads the transform into Slicer if it has not been loaded yet
    def getOriginTransform(self):
        if self.originTransform is not None:
            ancestors=self.ancestorList(True)
            tformStashLib = ancestors[-1]
            if tformStashLib is not None and self.originTransform[0] in tformStashLib.transforms:
                self.originTransform = (self.originTransform[0], tformStashLib.transforms[self.originTransform[0]])
            if self.originTransform[1] is None:
                if (sys.version_info > (3, 0)):
                    # slicer py3 call, nightlies, and future next release
                    transformNode = slicer.util.loadTransform(self.originTransform[0])
                else:
                    #slicer py2 call, current release(as of 2020-10) 4.10.2
                    [loadSuccess, transformNode]=slicer.util.loadTransform(self.originTransform[0], returnNode=True)
                    if loadSuccess == 0:
                        transformNode = None
                if transformNode is not None:
                    self.originTransform = (self.originTransform[0], transformNode)
                    tformStashLib.transforms[self.originTransform[0]] = transformNode
                else:
                    print("Failed to load transform:"+self.originTransform[0]+" from "+self.conf_dir)
            return self.originTransform[1]
        return None
    
    ## Returns the volDict for an ndLibrary
    def get_volume_dict(self):
        if isinstance(self.volDict, type(self)):
            return self.volDict.get_volume_dict()
        return self.volDict
    
    ## Returns a volume given the type of volume wanted (i.e. fa, dwi)
    ## Loads the volume into Slicer if it has not been loaded yet
    def get_volume_node(self, key):
        # No volDict, check children.
        if self.volDict is None or key not in self.volDict:
            for child in self.children:
                volNode = child.get_volume_node(key)
                if volNode is not None:
                    return volNode
            try:
                print("Invalid key "+key+" in "+self.Path)
            except:
                print("Invalid key "+key+" in unbuilt lib from conf "+self.conf_dir)
            return None
        volNode = self.volDict[key][1]
        if volNode is None:
            #slicer.util.showStatusMessage("loading "+key+" ...")
            ctblKey="ColorTable_"+key
            if ctblKey in self.conf:
                ctbl=os.path.join(os.path.dirname(self.volDict[key][0]),self.conf[ctblKey])
                print("custom color table:"+self.conf[ctblKey]+" for "+key)
            else:
                ctbl = None
            if (sys.version_info > (3, 0)):
                if ctbl is not None:
                    ctbl=slicer.util.loadColorTable(ctbl)
                volNode=slicer.util.loadVolume(self.volDict[key][0],{'show':False})
            else:
                if ctbl is not None:
                    [loadSuccess,ctbl]=slicer.util.loadColorTable(ctbl,returnNode=True)
                    if loadSuccess == 0:
                        ctbl = None
                [LoadSuccess, volNode]=slicer.util.loadVolume(self.volDict[key][0],{'show':False},returnNode=True)
                if LoadSuccess==0:
                    volNode = None
            if volNode is not None:
                self.volDict[key] = (self.volDict[key][0], volNode)
                originTransform = self.getOriginTransform()
                if originTransform is not None:
                    volNode.SetAndObserveTransformNodeID(originTransform.GetID())
                if ctbl is not None:
                    volNode.GetDisplayNode().SetAndObserveColorNodeID(ctbl.GetID())
            else:
                #slicer.util.showStatusMessage(key+ " Error loading")
                print("Error loading volume:"+key)
            #slicer.util.showStatusMessage("")
        return volNode
    
    ## Returns the name of a labeled region given a region number read from the color lookup table
    def getRegionLabel(self, roi_num):
        if isinstance(self.labelDict, type(self)):
            return self.labelDict.getRegionLabel(roi_num)
        if not roi_num in self.labelDict:
            print("Invalid region number")
            return
        return self.labelDict[roi_num][0]
    
    ## Toggles the label volume on or off given the value of show
    def toggleLabelVolume(self, show):
        compNodes = slicer.app.mrmlScene().GetNodesByClass("vtkMRMLSliceCompositeNode")
        if show == True and self.getLabelVolume() is not None:
            for node in compNodes:
                node.SetReferenceLabelVolumeID(self.getLabelVolume().GetID())
        else:
            for node in compNodes:
                node.SetReferenceLabelVolumeID("None")
    
    ## Returns the color table node associated with the ndLibrary
    def getColorTableNode(self):
        if isinstance(self.colorTable, type(self)):
            return self.colorTable.getColorTableNode()
        if self.colorTable is not None:
            return self.colorTable[1]
        return None
    
    ## Returns the labelDict associated with the ndLibrary
    def getLabelDict(self):
        if isinstance(self.labelDict, type(self)):
            return self.labelDict.getLabelDict()
        return self.labelDict
    
    def load_tractography(self):
        print("Tract load")
        tract_path = os.path.join(self.Path,"tractography.mrml")
        if not os.path.isfile(tract_path):
            print("No tractography.mrml available at "+tract_path)
            return False
        labels = self.getLabelVolume()
        self.jumpToDir()
        slicer.util.loadScene(tract_path)
        # look for custom python
        if "CustomPython" in self.conf:
            print("\t with CustomPython")
            # run
            library=self
            try:
                exec(open(self.conf["CustomPython"]).read())
            except:
                print("CustomPython\""+self.conf["CustomPython"]+"\"Failed in dir"+os.getcwd())
                return False
        return True
    
    ## Returns the label volume associated with the ndLibrary
    ## Loads the label volume into Slicer if not loaded yet
    def getLabelVolume(self):
        if isinstance(self.labelVolume, type(self)):
            #print("Going to {}".format(self.labelVolume.file_loc))
            return self.labelVolume.getLabelVolume()
        if self.labelVolume == None:
            return None
        if self.labelVolume[1] is None:
            if (sys.version_info > (3, 0)):
                # slicer py3 call, nightlies, and future next release
                labelVolumeNode = slicer.util.loadLabelVolume(self.labelVolume[0], {'show':False})
            else:
                #slicer py2 call, current release(as of 2020-10) 4.10.2
                [loadSuccess, labelVolumeNode] = slicer.util.loadLabelVolume(self.labelVolume[0], {'show':False}, returnNode=True)
                if not loadSuccess:
                    labelVolumeNode = None
            #print(self.labelVolume[0])
            #print(type(self.labelVolume))
            if labelVolumeNode is not None:
                self.labelVolume = (self.labelVolume[0], labelVolumeNode)
                labelVolumeNode.GetDisplayNode().SetSliceIntersectionThickness(1)
                labelVolumeNode.GetDisplayNode().SetAndObserveColorNodeID(self.getColorTableNode().GetID())
                originTransform = self.getOriginTransform()
                if originTransform is not None:
                    labelVolumeNode.SetAndObserveTransformNodeID(originTransform.GetID())
            else:
                print("Failed to load labelVolume")
                return None
        return self.labelVolume[1]
    
    ## Should be unnecessary going forward, as we'll connect "colornum"(which appears to be roinum) direct on load
    ## From the region number of a label, get the row number for the table of label colors (Found in Colors module)
    ## Mostly used for InteractiveLabelSelector
    def getRowNum(self, roi_num):
        print("there is no row data for ndlibrary!")
    
    ## Should be unnecessary going forward, as we'll connect "colornum"(which appears to be roinum) direct on load
    ## From the row number of the table of label colors, find the associated region number of a label
    ## Mostly used for InteractiveLabelSelector
    def getRegionNum(self, row_num):
        print("there is no row data for ndlibrary!")
        return None
    
    ## Meant to tell whether or not ndLibrary object is initialized properly
    def isValid(self):
        return self.valid
    
    ## Meant to tell whether or not current ndLibrary is the root ndLibrary for a relevant strain
    def isRelevantStrainLibrary(self):
        return self.relevantStrainLib
    
    ## Returns a list of relevant strains meant to be options for the DataPackageMenu
    def getRelevantStrainList(self):
        if self.isRelevantStrainLibrary():
            return [self]
        relevantStrainList = list()
        for child in self.children:
            relevantStrainList.extend(child.getRelevantStrainList())
        return relevantStrainList
    
    ## Returns a list of libs by category, will sometime expand to also choose what we're filtering on.
    def getLibsByCategory(self,categoryFilter):
        if self.valid and self.conf["Category"] == categoryFilter:
            return [self]
        libList = list()
        for child in self.children:
            if child.valid and child.conf["Category"] == categoryFilter:
                libList.extend(child.getLibsByCategory(categoryFilter))
        return libList

    ## Function that collects all of the volDict information for an ndLibrary and all child ndLibraries
    ## Include volDict information from children of children and so forth
    ## this unfortunately loses libconf information replacing it with oldest parent.
    def getEntireVolumeSetPaths(self):
        if self.volDict is not None:
            entireDict = self.volDict
        else:
            entireDict = dict()
        for child in self.children:
            volumeDict = child.getEntireVolumeSet()
            if volumeDict is not None:
                for key in volumeDict:
                    if not key in entireDict:
                        entireDict[key] = volumeDict[key]
        if "labels" in entireDict:
            del entireDict["labels"]
        return entireDict
    
    ## Function that collects pointers to lib for all volDict for an ndLibrary and all child ndLibraries
    ## Include volDict information from children of children and so forth
    def getEntireVolumeSet(self):
        entireDict = dict()
        if self.volDict is not None:
            #entireDict = self.volDict
            for key in self.volDict:
                entireDict[key] = self
        #type(self.libDict[name]) is tuple:
        for child in self.children:
            volumeDict = child.getEntireVolumeSet()
            if volumeDict is not None:
                for key in volumeDict:
                    if not key in entireDict:
                        entireDict[key] = child
        if "labels" in entireDict:
            del entireDict["labels"]
        return entireDict