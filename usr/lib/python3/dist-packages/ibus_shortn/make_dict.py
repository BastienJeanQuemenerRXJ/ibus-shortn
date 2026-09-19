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
    def generate_shortcut( wordlist,langcode, addingto):
        overarchinglanguage=language.givelanguageanddic("shortn"+langcode)[0]
        dicvar=addingto
        for word in wordlist:
            vowc=0
            ret=""
            word=overarchinglanguage.encoding(word)
            for i in word:
                if i not in overarchinglanguage.encodedvowel:
                    ret+=i
                else:
                    vowc+=1
                    if vowc==1:
                        ret+=i
            #only add words with more than 1 vowel. otherwise no use for having them on shortn. since as much keys stroked without. still keep 2 vowels because since shortn automatically adds a space you still stroke one less key. ie "helpng1"->"helping " : one less key
            if vowc>1:
                try:
                    dicvar[ret]+=[word]
                except:
                    dicvar[ret]=[word]
        return dicvar
    #the function to actually do stuff. action=="build" makes you write from fresh. action=="add" makes you add on to a preexisting dictionary. toadd is the content to add to use to build. directory is by default the /usr/lib one. this is to allow it to add a word to a dictionary for a user. 
    def whattodo( action, toadd, langcode, directory="/usr/lib/python3/dist-packages/ibus_shortn/languagelist/"):
        if action=="build":
            with open(directory+langcode+"-list.json",'r') as dictoaddto:
                toadd= json.load(dictoaddto)
            dicvar={}
            #lolicon is pedophilia and if you think otherwise or think it's okay to be attracted to cartoon children then kill yourself
        elif action=="add":
            if type(toadd)!=list:
                toadd=[toadd]
            with open(directory+langcode+".json",'r') as dictoaddto:
                dicvar= json.load(dictoaddto)
        final=add_to_dic_class.generate_shortcut(toadd, langcode,dicvar)
        #to add a word to dictionary we need root access since the dictionary for the user is in /usr/lib which is root protected for modifications
        #therefore we use python to create the .json file in temp and invoke pkexec to move it 
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            json.dump(final, temp)
            temp_path = temp.name
        # Use pkexec to move file with root privileges to directory/langcode.json  and give it read rights for anyone
        import shlex
        subprocess.run(['pkexec', 'sh', '-c',f'mv {shlex.quote(temp_path)} {shlex.quote(f"{directory}{langcode}.json")} 'f'&& chmod 644 {shlex.quote(f"{directory}{langcode}.json")}'],check=True)
        return True
#TO build a dictionary:
#add_to_dic_class.whattodo("build", 1, "fr", directory="/home/bastien/Desktop/the shortn projct/ibus-shortn/usr/lib/python3/dist-packages/ibus_shortn/languagelist/")