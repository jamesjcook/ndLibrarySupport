## Class for a library of data
## NOTE: Assumes files are in a Windows system
## Author: Austin Kao
import os
import re

class ndLibrary:        
    ## Constructor for a ndLibrary
    ## parent: The parent ndLibrary
    ## file_loc: The full file path that the ndLibrary resides in
    ## fields: A dictionary populated with name-value pairs found in lib.conf
    ## recursion_field: String used to identify uses of recursion
    ## conf_file_name: String that stores the default name of a conf file (lib.conf)
    ## labelDict: A dictionary populated with the labels found in a lookup table file
    ## valid: A field that tells if an ndLibrary object is valid for use (Needs to pass the initial checks)
    def __init__(self, parent, file_loc):
        self.valid = False
        if not os.path.isdir(file_loc):
            print('Not a directory')
            return
        self.conf_file_name = "lib.conf"
        if not os.path.isfile(os.path.join(file_loc, self.conf_file_name)):
            #print("No lib.conf file present")
            return
        if isinstance(parent, type(self)):
            self.fields = dict(parent.fields)
        elif parent is None:
            self.fields = dict()
        else:
            print("Parent is invalid")
            return
        self.valid = True
        self.parent = parent
        self.file_loc = file_loc
        self.children = list()
        self.is_leaf = False
        self.volDict = None
        self.recursion_field = "RecursiveLoad"
        self.path_field = "Path"
        self.match_field = "FileAbrevMatch"
        self.pattern_field = "FilePattern"
        self.filter_field = "FileAbrevPattern"
        self.labelDict = None
        self.labelVolume = None
        self.colorTable = None
        self.trackTransform = None
        self.relevantStrainLib = False
        if self.pattern_field in self.fields:
            del self.fields[self.pattern_field]
        if self.match_field in self.fields:
            del self.fields[self.match_field]
        ## Have ndLibrary automatically build the ndLibrary tree if it is a root?
        self.extensionPriority = list({"nhdr", "nrrd", "nii.gz", "nii", "png", "tif", "jpg", "gif", "bmp"})
        if parent == None:
            self.loadEntire()
    
    ## Method to load a lib.conf file for a ndLibrary and store the name-value pairs it contains
    def loadConf(self, file):
        try:
            conf = open(file)
        except:
            print("Could not open conf file")
            return
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
                self.fields[name] = value
            line = conf.readline()
    
    ## Method to find and make child ndLibraries
    def buildChildren(self):
        if self.recursion_field in self.fields and self.fields[self.recursion_field] == "false":
            #print("Reached leaf of tree. No children")
            is_leaf = True
            return
        os.chdir(self.file_loc)
        if (self.recursion_field in self.fields and self.fields[self.recursion_field] == "true"
            and self.path_field in self.fields and os.path.isdir(self.fields[self.path_field])):        
                #print("Going on another path: {}".format(self.fields[self.path_field]))
                os.chdir(self.fields[self.path_field])
        for directory in os.listdir(os.getcwd()):
            #print(os.path.join(self.file_loc, directory))
            if os.path.isdir(os.path.join(os.getcwd(), directory)):
                child_lib = ndLibrary(self, os.path.join(os.getcwd(), directory))
                if child_lib.isValid():
                    self.children.append(child_lib)
        if len(self.children) == 0:
            is_leaf = True
    
    ## Method to load the entire ndLibrary tree
    ## Loads a conf file, makes all possible child ndLibraries, and repeats the process for each child
    def loadEntire(self):
        if self.file_loc is not None and os.path.isfile(os.path.join(self.file_loc, self.conf_file_name)):
            self.loadConf(os.path.join(self.file_loc, self.conf_file_name))
            self.determineRelevance()
            self.loadVolumes()
            self.loadLabels()
            self.loadTrackTransform()
            self.buildChildren()
            for child in self.children:
                child.loadEntire()
        else:
            print("Not loading for {}".format(self.file_loc))
    
    ## Determines whether or not current ndLibrary is relevant enough for a menu of data packages
    ## Meant to be called after loading lib.conf file when building the entire tree
    ## May get incorrect result if used in other circumstances
    def determineRelevance(self):
        if "TestingLib" in self.fields and self.fields["TestingLib"] == "true":
            self.relevantStrainLib = False
        elif "Category" in self.fields and self.fields["Category"] == "Species":
            #and "Strain" in self.fields):
            self.relevantStrainLib = True
        #print("{} is {}".format(self.file_loc, self.relevantStrainLib))
    
    ## Function to change the working directory according to the path specfied in a lib.conf file
    ## By default, the function will change the working directory to the ndLibrary's directory
    def jumpToDir(self):
        os.chdir(self.file_loc)
        #if self.fields.has_key(self.path_field):
        if self.path_field in self.fields:
            relativePath = self.fields[self.path_field].replace("/","\\")
            if os.path.isdir(relativePath):
                os.chdir(relativePath)
                #print("Jumping to {}".format(os.getcwd()))
    
    ## Function that loads the volumes into a dictionary called volDict
    ## Keys for the dictionary are the type of volume ("fa", "dwi", etc.)
    ## Values are a tuple of (file_path, volume_node) where volume_node is initially None
    ## Libraries will load volumes on demand using the file_path
    ## See get_volume_node method for more details
    def loadVolumes(self):
        if self.volDict is not None:
            #print("Volumes are already loaded")
            return
        #if self.fields.has_key(self.pattern_field):
        if self.pattern_field in self.fields:
            filePat = self.fields[self.pattern_field]
        else:
            #print("No files to be found")
            return
        #print("Loading volumes for {}".format(self.file_loc))
        self.jumpToDir()
        try:
            volumes = [f for f in os.listdir(os.getcwd()) if re.match(r''+filePat, f)]
        except re.error:
            #print("Bad regex")
            return
        #print("Found {} volumes with pattern {}".format(len(volumes), filePat))
        if len(volumes) == 0:
            #print("No volumes detected")
            return
        self.volDict = dict()
        for i in range(0, len(volumes)):
            volPath = os.path.join(os.getcwd(), volumes[i])
            extension = volumes[i].split(".", 1)[-1]
            if os.path.isdir(volPath) or "label" in volumes[i] or not extension in self.extensionPriority:
                continue
            fileName = volumes[i].split(".")[0]
            fileName = fileName.lower()
            #if self.fields.has_key("FileAbrevPattern"):
            if self.filter_field in self.fields:
                pattern = self.fields[self.filter_field]
                pattern = pattern.replace("||","|") #Possible mistake with regex? Regex matching doesn't work as expected otherwise
                match = re.search(pattern, fileName)
                #print(pattern)
                #print(fileName)
                if match and len(match.groups()) > 1:
                    #print(match.groups())
                    self.addToVolDict(volPath, match.group(2))
                elif match:
                    #print(match.groups())
                    self.addToVolDict(volPath, match.group(1))
            else:
                self.volDict[fileName] = (volPath, None)
        if len(self.volDict) == 0:
            self.volDict = None
            #print("No valid files found")
            return
    ## Helper function that handles how a determined path and key are added to the volDict
    def addToVolDict(self, volPath, key):
        ## Check if another name is wanted according to the lib.conf file
        if key in self.fields:
            key = self.fields[key]
        ## Compare the file extensions if there are conflicting keys
        if key in self.volDict:
            currentExt = self.volDict[key][0].split(".", 1)[-1]
            newExt = volPath.split(".", 1)[-1]
            for ext in self.extensionPriority:
                if ext == newExt:
                    self.volDict[key] = (volPath, None)
                    break
                if ext == currentExt:
                    break
        else:
            self.volDict[key] = (volPath, None)
    
    ## Loads in the label volume file for a particular specimen
    ## Loads the lookup table for the different regions of the brain
    ## No lookup table in example directory, for now is hard coded to go to a specific file in a specific directory
    def loadLabels(self):
        if self.labelDict is not None and self.colorTable is not None and self.labelVolume is not None:
            print("Labels are already loaded")
            return
        if self.pattern_field in self.fields:
            labelPat = self.fields[self.pattern_field]
        else:
            #print("No files to be found")
            return
        #print("Loading labels for {}".format(self.file_loc))
        tablePat = ".*[.]txt"
        self.jumpToDir()
        try:
            labels = [f for f in os.listdir(os.getcwd()) if re.match(r''+labelPat, f)]
            clts = [f for f in os.listdir(os.getcwd()) if re.match(r''+tablePat, f)]
        except re.error:
            #print("Bad regex")
            return
        if len(labels) == 0 or len(clts) == 0:
            #print("Cannot be a label directory")
            return
        for i in range(0, len(labels)):
            if (not os.path.isfile(labels[i]) or not "label" in labels[i] or
                not labels[i].split(".", 1)[-1] == "nii.gz"):
                    continue
            labelPath = os.path.join(os.getcwd(), labels[i])
            #print(labelPath)
            self.labelVolume = (labelPath, None)
        if not isinstance(self.labelVolume, tuple):
            #print("Not a tuple. No valid volumes found.")
            return
        #txt = open(clts[cltIndex])
        ## Assume that the first text file found is the right color lookup table file
        txt = open(clts[0])
        #print("Found color lookup table")
        self.labelDict = dict()
        [loadSuccess, colorTable] = slicer.util.loadColorTable(os.path.join(os.getcwd(), clts[0]), returnNode=True)
        if loadSuccess == 0:
            print("Could not load color lookup table. File: {}".format(clts[0]))
            return
        self.colorTable = (os.path.join(os.getcwd(), clts[0]), colorTable)
        ## Count parameter is the number a node will be when ordered ascendingly
        ## i.e. node 0 is still 0, but node 1001 becomes 167, 1002 becomes 168, etc.
        ## Useful for InteractiveLabelSelector
        count = 0
        for line in txt:
            words = line.split(' ')
            if words[0] is not "#" and len(words) > 4:
                try:
                    self.labelDict[int(words[0])] = (words[1],words[2],words[3],words[4], count)
                except ValueError:
                    pass
                count += 1
        parent_lib = self.parent
        #print("Found valid labels in {}".format(self.file_loc))
        while parent_lib is not None:
            parent_lib.labelDict = self
            parent_lib.colorTable = self
            parent_lib.labelVolume = self
            parent_lib = parent_lib.parent
    
    ## Function that loads the transform for the volume node
    ## trackTransform is a tuple with two elements
    ## Element 0 is the file path for the transform
    ## Element 1 is the transform node in 3D Slicer
    def loadTrackTransform(self):
        if not "OriginTransform" in self.fields:
            #print("No path to follow for origin transform")
            return
        if self.trackTransform is not None:
            #print("Track transform is already loaded")
            return
        self.jumpToDir()
        originPath = self.fields["OriginTransform"].replace("/","\\")
        if os.path.isfile(originPath):
            self.trackTransform = (os.path.join(os.getcwd(), originPath), None)
    
    ## Returns the origin transform for a given volume
    ## Loads the transform into Slicer if it has not been loaded yet
    def getTrackTransform(self):
        if self.trackTransform is not None:
            if self.trackTransform[1] is None:
                [loadSuccess, transformNode]=slicer.util.loadTransform(self.trackTransform[0], True)
                if loadSuccess == 0:
                    print("Failed to load transform:"+self.trackTransform[0])
                else:
                    self.trackTransform = (self.trackTransform[0], transformNode)
            return self.trackTransform[1]
        return None
    
    ## Returns the volDict for an ndLibrary
    def get_volume_dict(self):
        if isinstance(self.volDict, ndLibrary):
            return self.volDict.get_volume_dict()
        return self.volDict
    
    ## Returns a volume given the type of volume wanted (i.e. fa, dwi)
    ## Loads the volume into Slicer if it has not been loaded yet
    def get_volume_node(self, key):
        if self.volDict is None:
            for child in self.children:
                volNode = child.get_volume_node(key)
                if volNode is not None:
                    return volNode
            return None
        if not key in self.volDict:
            print("Invalid key")
            return
        volNode = self.volDict[key][1]
        if volNode is None:
            [LoadSuccess, volNode]=slicer.util.loadVolume(self.volDict[key][0],{'show':False},True)
            if LoadSuccess==0:
                print("Error loading volume")
                return None
            else:
                self.volDict[key] = (self.volDict[key][0], volNode)
                trackTransform = self.getTrackTransform()
                if trackTransform is not None:
                    volNode.SetAndObserveTransformNodeID(trackTransform.GetID())
        return volNode
    
    ## Returns the name of a labeled region given a region number read from the color lookup table
    def getRegionLabel(self, num):
        if isinstance(self.labelDict, ndLibrary):
            return self.labelDict.getRegionLabel(num)
        if not num in self.labelDict:
            print("Invalid region number")
            return
        return self.labelDict[num][0]
    
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
        if isinstance(self.colorTable, ndLibrary):
            return self.colorTable.getColorTableNode()
        if self.colorTable is not None:
            return self.colorTable[1]
        return None
    
    ## Returns the labelDict associated with the ndLibrary
    def getLabelDict(self):
        if isinstance(self.labelDict, ndLibrary):
            return self.labelDict.getLabelDict()
        return self.labelDict
    
    ## Returns the label volume associated with the ndLibrary
    ## Loads the label volume into Slicer if not loaded yet
    def getLabelVolume(self):
        if isinstance(self.labelVolume, ndLibrary):
            #print("Going to {}".format(self.labelVolume.file_loc))
            return self.labelVolume.getLabelVolume()
        if self.labelVolume == None:
            return None
        if self.labelVolume[1] is None:
            #print(self.labelVolume[0])
            [loadSuccess, labelVolumeNode] = slicer.util.loadLabelVolume(self.labelVolume[0], {'show':False}, returnNode=True)
            #print(type(self.labelVolume))
            if loadSuccess == 0:
                print("Failed to load labelVolume")
                return None
            else:
                self.labelVolume = (self.labelVolume[0], labelVolumeNode)
                labelVolumeNode.GetDisplayNode().SetSliceIntersectionThickness(1)
                labelVolumeNode.GetDisplayNode().SetAndObserveColorNodeID(self.getColorTableNode().GetID())
                trackTransform = self.getTrackTransform()
                if trackTransform is not None:
                    labelVolumeNode.SetAndObserveTransformNodeID(trackTransform.GetID())
        return self.labelVolume[1]
        
    ## From the region number of a label, get the row number for the table of label colors (Found in Colors module)
    ## Mostly used for InteractiveLabelSelector
    def getRowNum(self, roiNum):
        if isinstance(self.labelDict, ndLibrary):
            return self.labelDict.getRowNum(roiNum)
        if roiNum in self.labelDict:
            return self.labelDict[roiNum][4]
        return None
    
    ## From the row number of the table of label colors, find the associated region number of a label
    ## Mostly used for InteractiveLabelSelector
    def getRegionNum(self, countNum):
        if isinstance(self.labelDict, ndLibrary):
            return self.labelDict.getRegionNum(countNum)
        if self.labelDict is None:
            return None
        for key in self.labelDict:
            if self.labelDict[key][4] == countNum:
                return key
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
    
    ## Function that collects all of the volDict information for an ndLibrary and all child ndLibraries
    ## Include volDict information from children of children and so forth
    def getEntireVolumeSet(self):
        if self.volDict is not None:
            entireDict = self.volDict
        else:
            entireDict = dict()
        for child in self.children:
            volumeDict = child.getEntireVolumeSet()
            if volumeDict is not None:
                for key in volumeDict:
                    if key in entireDict:
                        currentExt = entireDict[key][0].split(".", 1)[-1]
                        newExt = volumeDict[key][0].split(".", 1)[-1]
                        #print(currentExt)
                        #print(newExt)
                        for ext in self.extensionPriority:
                            if ext == currentExt:
                                #print("chose {}".format(currentExt))
                                break
                            if ext == newExt:
                                #print("chose {}".format(newExt))
                                entireDict[key] = volumeDict[key]
                                break
                    else:
                        entireDict[key] = volumeDict[key]
        return entireDict