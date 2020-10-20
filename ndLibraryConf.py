## lib.conf loader/saver/handler 

class ndLibraryConf:
    def __init__(self,confPath):
        # fields is the name ready to use fields
        self.fields=dict()
        # comments will be line num : comment
        self.comments=dict()
        # lines will be line num : field key
        self.lines=dict()
        self.lineCount = 0
        if os.path.isfile(confPath):
            #self.conf_path = conf_path
            #print(self.conf_dir)
            self.load(confPath)
    ## Method to load a lib.conf file for a ndLibrary and store the name-value pairs it contains
    def load(self, file=None):
        if file is None:
            file=self.conf_path
        with open(file) as fp:
            # do stuff with fp
            for cnt, line in enumerate(fp):
                print(cnt)
                self.lineCount = cnt
                components = re.match(r"^([^#=]*)(?:=([^#]+))?(#.*)?$",line)
                key=components.group(1)
                value=components.group(2)
                comment=components.group(3)
                if key is not None:# and value is not None:
                    self.fields[key.strip()] = value.strip()
                    self.lines[cnt]=value.strip()
                elif (key is None or not key) and (value is None or not value):
                    #print("Ignore line:"+line.strip())
                    pass
                elif key is None:
                    print("conf error: bad key, value is "+value.strip())
                elif value is None:
                    # This condition has been disabled, by allowing blank values in primary match.
                    # We'll allow blank values as a way to disable a parent key.
                    # THIS IS KINDA AGAINST DESIGN! PARENTS SHOULD ONLY HOLD VALUES WHICH ARE COMMON TO ALL CHILDREN
                    print("conf error: bad value, key is "+key.strip())
                if comment is not None:
                    self.comments[cnt] = comment
        # clean up routine typeo, except its so pervasive... 
        #if self.pattern_field not in self.fields and "FileAbrevPattern" in self.fields:
        #    self.pattern_field = "FileAbrevPattern"
        #    self.fields[self.pattern_field]=
        #if self.match_field not in self.fields and "FileAbbrevMatch" in self.fields:
        #    self.match_field = "FileAbrevMatch"
        self.conf_path = file
    ## print conf
    def print(self,indent=""):
        for e in self.fields:
            print(indent+"\t"+e+"\t= "+self.fields[e])
    ## save conf
    def save(self,outPath=None):
        if outPath is None:
            print('Conf overwrite disabled for now');
            return
        fields=self.fields.copy()
        #for e in self.fields:
        for i in range(0,self.lineCount):
            data=""
            comment=""
            if i in self.comments:
                comment=self.comments[i]
            if i in self.lines:
                data=self.lines[i]+"="+fields[self.lines[i]]
                del fields[self.lines[i]]
            line=data+comment
            print(line)
        for e in fields:
            line=e+"="+fields[e]
            print(line)
        
    