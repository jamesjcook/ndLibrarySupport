## lib.conf loader/saver/handler 
import os
import re

class conf:
    def __init__(self,conf_path,conf_name="lib.conf"):
        # fields is the name ready to use fields
        self.fields=dict()
        # comments will be line num : comment
        self.comments=dict()
        # lines will be line num : field key
        self.lines=dict()
        self.lineCount = 0
        # in the future perhaps we support "json" mode?
        self.mode="conf"
        if os.path.isfile(conf_path):
            self.conf_path=conf_path
            self.conf_dir=os.path.dirname(conf_path)
            self.conf_name=os.path.basename(conf_path)
        else:# os.path.isdir(conf_path):
            self.conf_path=os.path.join(conf_path,conf_name)
            self.conf_dir=conf_path
            self.conf_name=conf_name
        if os.path.isfile(self.conf_path):
            self.load(self.conf_path)
        else:
            print("New empty conf for "+self.conf_path)
    ## Method to load a lib.conf file for a ndLibrary and store the name-value pairs it contains
    def load(self, file=None):
        if file is None:
            file=self.conf_path
        with open(file) as fp:
            # do stuff with fp
            for cnt, line in enumerate(fp):
                #print(cnt)
                self.lineCount = cnt+1
                components = re.match(r"^([^#=]*)(?:=([^#]+))?(#.*)?$",line)
                key = components.group(1)
                value = components.group(2)
                comment = components.group(3)
                if key is not None and key.strip():# and value is not None:
                    if value is None:
                        value=""
                    self.fields[key.strip()] = value.strip()
                    self.lines[cnt] = key.strip()
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
        self.path = file
    ## print conf
    def print(self,indent=""):
        for e in self.fields:
            print(indent+"\t"+e+"\t= "+self.fields[e])
    ## save conf
    def save(self,out_path=None):
        if os.path.isdir(out_path):
            #print("Given dir, add name")
            out_path=os.path.join(out_path,"lib.conf")
        if out_path is None or os.path.isfile(out_path):
            print('Conf overwrite disabled for now');
            #out_path=self.conf_path
            return
        fp = open(out_path,"w")
        fields=self.fields.copy()
        #for e in self.fields:
        for i in range(0,self.lineCount):
            data=""
            comment=""
            if i in self.comments:
                comment=self.comments[i]
            if i in self.lines and not self.lines[i] == "" and self.lines[i] in fields:
                data=self.lines[i]+"="+fields[self.lines[i]]
                del fields[self.lines[i]]
            line=data+comment
            #print(str(i)+":"+line)
            #print(line)
            if not line == "":
                fp.write(line+"\n")
        for e in fields:
            line=""
            if not e == "":
                line = e+"="
            if not fields[e] == "":
                line=line+fields[e]
            #print(line)
            fp.write(line+"\n")
