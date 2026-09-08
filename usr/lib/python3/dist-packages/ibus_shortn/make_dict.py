# Copyright (c) 2026 - Bastien Jean Quemener <shortn@bastien.live>  (github.com/BastienJeanQuemerRXJ/ibus-shortn)
#
# This file is part of ibus-shortn, the IBus Shortn input method engine, forked from ibus-cangjie.
#
# ibus-shortn is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-shortn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-shortn.  If not, see <http://www.gnu.org/licenses/>.


#add here
#if .json file doesnt exist, look for a .txt file of the same name
#if exists, check to see if it has windows or unix style ending  (\n) instead of (\r\n)
#then check to see if accents in the file, if yes check if they are one character instead of two  (ie nfc accents)
#then convert to json

import json
import subprocess
import tempfile
import os
#debug tool
"""
def logwrite(the, e=0):
    #except Exception as the
    if e==1:
        the="shortnengine failed because of"+getattr(the, 'message', repr(the))
    the=str(the)
    with open('/home/bastien/Desktop/shortndebug.txt', 'a', encoding='utf-8') as f:
        f.writelines(the)
"""      
#import languageclassfile which does all the language config stuff
try:
    from .languageclassfile import language  
except :
    from languageclassfile import language
# dotlanguageclassfile vs languageclassfile is when running as an app vs as a singular file

#since we mostly import make_dict we need to make a class
class add_to_dic_class:
    def __init__(self):
        True
    #wordlist is a [list] of words, langcode is the code (ie "en", "fr", etc) that is used for lang config stuff. addingto is if the dictionary already exists or start fresh. returns the dic
    def generate_shortcut( wordlist,langcode, addingto={"lolcn":["pedophile", "lolicon"]}):
        overarchinglanguage=language.givelanguageanddic("shortn"+langcode)[0]
        dicvar=addingto
        for word in wordlist:
            vowc=0
            ret=""
            word=overarchinglanguage.encoding(word)
            for i in word:
                if i in overarchinglanguage.encodedvowel and vowc!=1:
                    ret+=i
                    vowc+=1
                elif i not in overarchinglanguage.encodedvowel:
                    ret+=i
            try:
                dicvar[ret]+=[word]
            except:
                dicvar[ret]=[word]
        return dicvar
    #the function to actually do stuff. action=="build" makes you write from fresh. action=="add" makes you add on to a preexisting dictionary. toadd is the content to add to use to build. directory is by default the /usr/lib one. this is to allow it to add a word to a dictionary for a user. 
    def whattodo( action, toadd, langcode, directory="/usr/lib/python3/dist-packages/ibus_shortn/languagelist/"):
        #if we are building then take toadd, use langcode language config to make a [list] for the dictionary. final is that long variable
        if action=="build":
            final=add_to_dic_class.generate_shortcut(toadd, langcode)
        elif action=="add":
            #make sure toadd is a list. a single word to add is fine
            if type(toadd)!=list:
                toadd=[toadd]
            #find langcode.json, read it, make a dictionary variable by converting toadd into it by building it from the dictionary variable of langcode.json. then have final be that final variable
            with open(directory+langcode+".json",'r') as dictoaddto:
                final=add_to_dic_class.generate_shortcut(toadd, langcode, json.load(dictoaddto))
        #to add a word to dictionary we need root access since the dictionary for the user is in /usr/lib which is root protected for modifications
        #therefore we use python to create the .json file in temp and invoke pkexec to move it 
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            json.dump(final, temp)
            temp_path = temp.name
        # Use pkexec to move file with root privileges to directory/langcode.json 
        subprocess.run(['pkexec', 'mv', temp_path, f"{directory}{langcode}.json"], check=True)
        return True