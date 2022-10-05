## lib.conf loader/saver/handler
## sub classing dict for super special funtime behavior.
## we have a few extra fields, which we may not use outside the class which
## record meta bits.
from __future__ import print_function
import sys
import os
import re
import logging

class conf(dict):
    def __init__(self,conf_path,conf_name="lib.conf", existing_conf = None):
        self.logger=logging.getLogger("ndLibrary")
        if existing_conf is not None:
            for f in existing_conf:
                    self[f]=existing_conf[f]
        #    self=existing_conf.copy()
        #super(dict, self).__init__()
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
        elif (r'lib.conf' not in conf_path): # os.path.isdir(conf_path):
            self.conf_path=os.path.join(conf_path,conf_name)
            self.conf_dir=conf_path
            self.conf_name=conf_name
        if os.path.isfile(self.conf_path):
            self.load(self.conf_path)#, existing_conf)
        else:
            self.logger.warning("New empty conf for "+self.conf_path)
            
    ## generate a new config file from a template if does not exist
    ## template is the path to template config file 
    def generate(self, template):
        self.logger.warning('    GENERATING NEW CONF FILE FOR: ' + template)
        self.load(template)
        self.save()
        
    ## Method to load a lib.conf file for a ndLibrary and store the name-value pairs it contains
    def load(self, file=None):#, existing_conf = None):
        if file is None:
            file=self.conf_path
        with open(file) as fp:
            # do stuff with fp
            for cnt, line in enumerate(fp):
                #self.logger.warning(cnt)
                self.lineCount = cnt+1
                components = re.match(r"^([^#=]*)(?:=([^#]+))?(#.*)?$",line)
                key = components.group(1)
                value = components.group(2)
                comment = components.group(3)

                if key is not None and key.strip():# and value is not None:
                    if value is None:
                        value=""
                    self[key.strip()] = value.strip()
                    self.lines[cnt] = key.strip()
                elif (key is None or not key) and (value is None or not value):
                    self.logger.warning("Ignore line:"+line.strip())
                    pass
                elif key is None:
                    self.logger.warning("conf error: bad key, value is "+value.strip())
                elif value is None:
                    # This condition has been disabled, by allowing blank values in primary match.
                    # We'll allow blank values as a way to disable a parent key.
                    # THIS IS KINDA AGAINST DESIGN! PARENTS SHOULD ONLY HOLD VALUES WHICH ARE COMMON TO ALL CHILDREN
                    self.logger.warning("conf error: bad value, key is "+key.strip())
                if comment is not None:
                    self.comments[cnt] = comment
        #if  existing_conf is not None:
        #    for f in existing_conf:
        #        if f not in self:
        #            self[f]=existing_conf
        # clean up routine typeo, except its so pervasive... 
        #if self.pattern_field not in self and "FileAbrevPattern" in self:
        #    self.pattern_field = "FileAbrevPattern"
        #    self[self.pattern_field]=
        #if self.match_field not in self and "FileAbbrevMatch" in self:
        #    self.match_field = "FileAbrevMatch"
    ## print conf
    def print(self,indent=""):
        for e in self:
            self.logger.warning(indent+"\t"+e+"\t= "+self[e])
    ## save conf
    def save(self,out_path=None):
        if out_path is None:
            out_path = self.conf_dir
        if out_path and os.path.isdir(out_path):
            #self.logger.warning("Given dir, add name")
            out_path=os.path.join(out_path,"lib.conf")
        else:
            self.logger.warning("Write disabled, switch to print" + "missing out path " + out_path)
            out_path = None
        #if out_path is None or os.path.isfile(out_path):
        if out_path and os.path.isfile(out_path):
            self.logger.warning('Conf overwrite disabled for now');
            #out_path=self.conf_path
            return
        if out_path is not None:
            fp = open(out_path,"w")
        fields=self.copy()
        #for e in self:
        for i in range(0,self.lineCount):
            data=""
            comment=""
            if i in self.comments:
                comment=self.comments[i]
            if i in self.lines and not self.lines[i] == "" and self.lines[i] in fields:
                data=self.lines[i]+"="+fields[self.lines[i]]
                del fields[self.lines[i]]
            line=data+comment
            #self.logger.warning(str(i)+":"+line)
            #self.logger.warning(line)
            if not line == "":
                if out_path is not None:
                    fp.write(line+"\n")
                else:
                    self.logger.warning(line)
        for e in fields:
            line=""
            if not e == "":
                line = e+"="
            if not fields[e] == "":
                line=line+fields[e]
            #self.logger.warning(line)
            if out_path is not None:
                fp.write(line+"\n")
            else:
                self.logger.warning(line)

