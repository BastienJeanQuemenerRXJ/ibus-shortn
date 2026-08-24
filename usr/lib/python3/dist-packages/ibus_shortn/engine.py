# Copyright (c) 2012-2013 - The IBus Cangjie authors (https://gitlab.freedesktop.org/cangjie/ibus-cangjie/)
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




#this is how many shortn engines (ie english french russian etc) there can be so add them here and then also the other places
__all__ = ["EngineShortn", "EngineShortnfr"]

import time
import gettext
from operator import attrgetter
import gi
gi.require_version('IBus','1.0')
from gi.repository import Gio
from gi.repository import IBus
#this is a debug tool that will write on a txt file called "shortndebug.txt" whatever you ask it to. ie logwrite(the) will write 'the' to shortndebug.txt. however it needs sudo perms and editing files so that's not too appropriate for a public release or something. its uses are still left in the file but commented out in case you are having troubles
"""
def logwrite(the, e=0):
    #except Exception as the
    if e==1:
        the="shortnengine failed because of"+getattr(the, 'message', repr(the))
    the=str(the)
    with open('/home/bastien/Desktop/shortndebug.txt', 'a', encoding='utf-8') as f:
        f.writelines(the)
"""
#this defines how to handle the localization of languages in terms of shortn engine
#yes, it's better to convert every non basic latin unicode character into a basic latin character by using upper case basic latin (ie a:a, é:A) because it massively helps on dictionary size and reduces encodign issues
class language:
    def __init__(self, originalalphabet, originalalphabetlowercasetouppercase, originalalphabetuppercasetolowercase, encodingfromoriginal, decodingtooriginal, encodedvowel, punctuation, dictionaryname, wordseparator):
        self.originalalphabet = originalalphabet  
        self.originalalphabetlowercasetouppercase = originalalphabetlowercasetouppercase
        self.originalalphabetuppercasetolowercase = originalalphabetuppercasetolowercase
        self.encodingfromoriginal = encodingfromoriginal
        self.decodingtooriginal = decodingtooriginal
        self.encodedvowel = encodedvowel
        self.punctuation = punctuation
        self.dictionaryname = dictionaryname
        self.wordseparator=wordseparator
    def encoding(self, the,scheme):
        a=""
        for i in the:
            a+= self.originalalphabetuppercasetolowercase.get(i,i)
        the=a
        a=""
        for i in the:
            a+= scheme.get(i,i)
        return a
    def decoding(self, the, scheme):
        a=""
        for i in the:
            a+= scheme.get(i,i)
        return a
        

en=language(
    {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "'"},
    { "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O","p": "P", "q": "Q", "r": "R", "s": "S", "t": "T","u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "'":"'", " ": " "},
    {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n", "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t","U": "u", "V": "v", "W": "w", "X": "x", "Y": "y","Z": "z", "'": "'", " ": " "},
    lambda x:x,
    lambda x:x,
    {'a', 'e', 'i', 'o', 'u', 'y'},
    {"?", "!", ".", ";", ","},
    "en.json",
    {" ", "-", "_"}
    )


fr=language(
    {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ö", "ä", "ü", "ï", "ë", "ù", "è", "à", "ç", "ô", "â", "ê", "î", "û", "é", "'"},
    { "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O","p": "P", "q": "Q", "r": "R", "s": "S", "t": "T","u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "'":"'", " ": " ","ö":"Ö","ä":"Ä","ü":"Ü","ï":"Ï","ë":"Ë","ù":"Ù","è":"È","à":"À","ç":"Ç","ô":"Ô","â":"Â","ê":"Ê","î":"Î","û":"Û","é":"É" },
    {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n", "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t","U": "u", "V": "v", "W": "w", "X": "x", "Y": "y","Z": "z", "'": "'", " ": " ", "Ö":"ö","Ä":"ä","Ü":"ü","Ï":"ï","Ë":"ë","Ù":"ù","È":"è","À":"à","Ç":"ç","Ô":"ô","Â":"â","Ê":"ê","Î":"î","Û":"û","É":"é"},
    lambda x : fr.encoding(x, {"ö":"O", "ä":"A", "ü":"U", "ï":"I", "ë":"E", "ù":"Y", "è":"R", "à":"W", "ç":"C", "ô":"K", "â":"S", "ê":"F", "î":"V", "û":"N", "é":"M"}),
    lambda x : fr.decoding(x, {"O":"ö", "A":"ä", "U":"ü", "I":"ï", "E":"ë", "Y":"ù", "R":"è", "W":"à", "C":"ç", "K":"ô", "S":"â", "F":"ê", "V":"î", "N":"û", "M":"é"}),
    {'a', 'e', 'i', 'o', 'u', 'y', "O", "A", "U", "I", "E", "Y", "R", "W", "C", "K", "S", "F", "V", "N", "M"},
    {"?", "!", ".", ";", ","},
    "fr.json",
    {" ", "'", "_", "-"}
    )
langlist={"fr":fr, "en":en}



#try to replace multiple line if statements by one line if statements
#if age >= 18: print("Adult")
#and
#status = "Adult" if age >= 18 else "Minor"

#i feel that it's ugly that is_inputnumber isn't inside class engine but whatever
#Is the `keyval` param a numeric input, e.g to select a candidate.
def is_inputnumber(keyval):
    return ((keyval in range(getattr(IBus, "0"), getattr(IBus, "9")+1)) or
            (keyval in range(IBus.KP_0, IBus.KP_9+1)))
class Engine(IBus.Engine):
    """The base class for Shortn engines."""
    def __init__(self):
        classname = self.__name__
        logwrite(classname)
        self.overarchinglanguage= en if classname == "shortn" else langlist.get(classname[6:], en)
        self.dic=self.loaddic()
        super(Engine, self).__init__()
        schema_id = "org.shortn-scheme.ibus.%s" % self.__name__
        self.settings = Gio.Settings(schema_id=schema_id)
        self.settings.connect("changed", self.on_value_changed)
        self.current_input = ""
        self.current_showtext = ""
        self.clear_on_next_input = False
        self.lookuptable = IBus.LookupTable()
        self.lookuptable.set_page_size(9)
        self.lookuptable.set_round(True)
        self.lookuptable.set_orientation(IBus.Orientation.HORIZONTAL)
        self.init_properties()
        self.init_shortn()
        #list of vowels
        self.vowels=self.overarchinglanguage.encodedvowel
        #every character that shortn accepts as inputtable to the engine
        self.acceptedshortnenginecharacterlist=self.overarchinglanguage.originalalphabet
        #appendable things to characters
        self.commonpunctuation=self.overarchinglanguage.punctuation
        #turn lowercase to uppercase
        self.capital=self.overarchinglanguage.originalalphabetlowercasetouppercase
        #turn uppercase to lowercase
        self.nocaplist=self.overarchinglanguage.originalalphabetuppercasetolowercase
        #punctuation variable
        self.addpunc=None
        #turns a word into all lowercase

    #loads dictionary. call it only once. the dictionary stays loaded. to call it. self.dic. 
    def loaddic(self,curdic=None):
        curdic="/usr/lib/python3/dist-packages/ibus_shortn/"+self.overarchinglanguage.dictionaryname if curdic==None else curdic
        try:
            import json
            with open(curdic,'r') as dic:
                return json.load(dic)
        except Exception as err:
            errc= getattr(err, 'message', repr(err))
            #logwrite("dicloading failed because of"+errc)
            return {"json":["failed"]}
    #commits inp (string) as final output. if ibusencode==False then it assumes inp is already converted into ibus encode. if you want to deconvert something from ibus encode to text, then you can do inp.text
    #it is necessary for what is being committed to be in ibus encode in the end
    def commit(self,inp=None, ibusencode=True):
        if not inp or inp==None or inp=="":
            return True
        if ibusencode:
            self.commit_text(IBus.Text.new_from_string(inp))
        else:
            self.commit_text(inp)
    #self.current_showtext    this is the name of what's being shown in the editable text input
    #shows you thestr in the edit window. keep in mind that what's shown is ran through appendables so for example if thestr=hosptl and shifttoggle is on and addpunc is "," then what's shown is "Hosptl,". albeit be aware that shortnengine does NOT see "Hosptl," it will always only see "hosptl"
    def showtext(self, thestr):
        thestr=self.appendables(thestr)
        text = IBus.Text.new_from_string(thestr)
        super(Engine, self).update_auxiliary_text(text, len(thestr)>0)
        # We don't use pre-edit at all for Shortn or Quick. However, some applications (most notably Firefox) fail to correctly position the candidate popup, as if they got confused by the absence of a pre-edit text. fix this 
        if thestr:
            super(Engine, self).update_preedit_text(IBus.Text.new_from_string('\u200B'), 0, True)
        else:
            super(Engine, self).update_preedit_text(IBus.Text.new_from_string(''), 0, False)
    

    #sets the list of candidates from a list of strings called thelist. if thelist==None then removes the candidate list panel
    def setcand(self, thelist=None,tables=False):
        if tables==True:
            if not self.current_input:
                self.setcand()
            self.update_lookup_table(self.lookuptable, self.lookuptable.get_number_of_candidates()>0)
            return True
        self.lookuptable.clear()
        if thelist!=None:
            num_candidates = 0
            for c in thelist:
                abcd=self.overarchinglanguage.decodingtooriginal(c)
                self.lookuptable.append_candidate(IBus.Text.new_from_string(abcd))
                num_candidates += 1
        self.update_lookup_table(self.lookuptable, self.lookuptable.get_number_of_candidates()>0)
    def init_properties(self):
        #this thing was here before multilanguage but now makes it crash pls fix it 
        self.prop_list = IBus.PropList()
        for (key, label) in (("halfwidth-chars", gettext.dgettext("ibus-shortn", "Half-Width Characters")),):
            stored_value = self.settings.get_boolean(key)
            state = IBus.PropState.CHECKED if stored_value else IBus.PropState.UNCHECKED
            try:
                # Try the new constructor from IBus >= 1.5
                prop = IBus.Property(key=key, prop_type=IBus.PropType.TOGGLE, label=label, icon='', sensitive=True, visible=True, state=state, sub_props=None)
            except TypeError:
                # IBus 1.4.x didn't have the GI overrides for the nice constructor, so let's do it the old, non-pythonic way.
                #IBus.Property.new(key, type, label, icon, tooltip, sensitive, visible, state, sub_props)
                prop = IBus.Property.new(key, IBus.PropType.TOGGLE, IBus.Text.new_from_string(label), '', IBus.Text.new_from_string(''), True, True, state, None)
            self.prop_list.append(prop)
    #i think this is important
    def do_property_activate(self, prop_name, state):
        active = state == IBus.PropState.CHECKED
        self.settings.set_boolean(prop_name, active)
    #when you switch windows or tabs back to the original one
    def do_focus_in(self):
        self.register_properties(self.prop_list)
    #supposed to do something
    def init_shortn(self):
        version = self.settings.get_int("version")
    #idk what this really does
    def on_value_changed(self, settings, key):
        # Only recreate the Shortn object if necessary
        return True
    #Handle focus out event. This happens, for example, when switching between application windows or input contexts. Such events should clear the current input.
    def do_focus_out(self):
        self.cleareverything()
    #Cancel the current input. However, if there isn't any current input, then we shouldn't try to do anything at all, so that the key can fulfill its original function.
    def do_cancel_input(self):
        if not self.current_input:
            return False
        self.cleareverything()
        return True
    #move up and down the candidate selection list
    def do_page_down(self):
        #Present the next page of candidates. However, if there isn't any current input, then we shouldn't try to do anything at all, so that the key can fulfill its original function.
        if not self.lookuptable.get_number_of_candidates():
            return False
        self.lookuptable.page_down()
        self.setcand(tables=True)
        self.showtext(self.current_showtext)
        return True
    #move up and down the candidate selection list
    def do_page_up(self):
        #Present the previous page of candidates. However, if there isn't any current input, then we shouldn't try to do anything at all, so that the key can fulfill its original function.
        if not self.lookuptable.get_number_of_candidates():
            return False

        self.lookuptable.page_up()
        self.setcand(tables=True)
        self.showtext(self.current_showtext)
        return True
    #return to base state
    def cleareverything(self):
        """Clear the current input."""
        self.current_input = ""
        self.clear_on_next_input = False
        self.setcand(tables=True)
        self.addpunc=None
        self.showtext("")
    #this updates the showtext variable and current_input variable. append is what you add to the current_input and current_showtext, drop is how much you remove
    def update_current_input(self, append=None, drop=None):
        if append is not None:
            if self.clear_on_next_input:
                self.cleareverything()
            self.current_input += append
        elif drop is not None:
            self.clear_on_next_input = False
            self.current_input = self.current_input[:-drop]
        else:
            raise ValueError("You must specify either 'append' or 'drop'")




class EngineShortn(Engine):
    #use something better than shift delay variables
    """The English Shortn engine."""
    __gtype_name__ = "EngineShortn"
    __name__ = "shortn"
    def nocap(self, the):
        a=""
        for i in the:
            a+=self.nocaplist.get(i,i)
        return a
    #turns a word into all lowercase except first letter that is uppercase
    def firstcap(self, the):
        if the==None:
            return True
        try:
            the=self.nocap(the)
        except:
            True
        if len(the)==1:
            return self.capital.get(the)
        return str(str(self.capital.get(the[:1],the[:1]))+str(the[1:]))
    #turns a word into all uppercase
    def allcap(self,the):
        a=""
        for i in the:
            a+=self.capital.get(i)
        return a
    #what to do when engine sees you typed a number
    def do_number(self, keyval):
        if self.lookuptable.get_number_of_candidates():
            a=int(IBus.keyval_to_unicode(keyval))
            if a==0:
                return False
            else:
                return self.do_select_candidate(a)
    #turns a normall lowercase word into the final product ie from 'hospital' to 'Hospital?' etc
    def appendables(self,a, encodingchange=True):
        the=a
        if the==" ":
            return " "
        elif the=="":
            return ""
        elif the==None:
            return None
        if encodingchange:
            the=self.overarchinglanguage.decodingtooriginal(the)
        if self.shifttoggle:
            the=self.firstcap(the)
        if self.addpunc!=None:
            the+=self.addpunc
        return the
    #once you get 'index' aka number what you do to it aka you choose from the list and input it
    def do_select_candidate(self, index):
        page_index = self.lookuptable.get_cursor_pos()
        selected = self.lookuptable.get_candidate(page_index+index-1)
        if selected!=None:
            b=selected.text
            b=self.overarchinglanguage.decodingtooriginal(b)
            b=self.appendables(b,encodingchange=False)+" "
            self.commit(b)
            self.shifttoggle=False
        self.cleareverything()
        if self.capitalizeaftercommit==True:
            self.shifttoggle=True
            self.capitalizeaftercommit=False
        return True
    #called by ibus. ie you use your mouse to click on a candidate
    def do_candidate_clicked(self, index, button, state):
        self.do_select_candidate(index+1)
    #from a word you get the last vowel aka type "hosptla" you get "a"
    def getlastvowel(self, inpp):
        inp=inpp
        a=[i for i in inp if i in self.vowels]
        if len(a)>1:
            return a[-1]
        else:
            return None
    #the main engine function. type "hosptl" and get "hospital"
    def shortnenginefunction(self, theinputt):
        theinput=theinputt
        a=self.getlastvowel(theinput)
        if a!=None:
            theinput=theinput[:-1]
        try:
            sug= self.dic.get(theinput)
        except:
            return None
        if a!=None:
            if type(sug)==list:
                b= [i for i in sug if self.getlastvowel(i)==a]
            else:
                return None
            if len(b)==0:
                return None
            else:
                return b
        else:
            return sug
    #when you press esc it "disables" the engine. these are its variables for that
    escapetoggle=True
    #sometimes the code needs an overflow variable. basically pressing one key once will have ibus interpret it as if you pressed it multiple times. these "overflow" variables are meant to prevent this. if a key is pressed multiple times under an interval lesser than 0.3 seconds it will only register it once
    escapeoverflow=time.time()
    #same thing but for pressing shift
    shifttoggle=False
    shiftoverflow=time.time()
    #when you type ANY key what to do
    def do_process_key_event(self, keyval, keycode, state):
        #if theres some issue with a user pressing keys too fast like return then delete and it not registering then change all elif to if 
        #mechanism for escape toggle. catches it and changes state
        if keyval==IBus.Escape and time.time()-self.escapeoverflow>0.3:
            self.escapetoggle= not self.escapetoggle
            if self.current_input!="":
                self.commit(self.overarchinglanguage.decodingtooriginal(self.current_input))
            self.cleareverything()
            self.escapeoverflow=time.time()
            return True
        #mechanism for escape toggle. if on, then return all false
        elif not self.escapetoggle:
            return False
        #when you press something without releasing it doesnt count?? ithink? 
        elif (state & IBus.ModifierType.RELEASE_MASK):
            return False
        # Ignore Alt+<key> and Ctrl+<key>
        elif state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK |IBus.ModifierType.MOD4_MASK):
            return False
        #mechanism for shift system
        if keyval==IBus.KEY_Shift_L and time.time()-self.shiftoverflow>0.3:
            self.shifttoggle=self.shifttoggle==False
            self.shiftoverflow=time.time()
            self.showtext(self.current_input)
            return False
        #if enter key pressed then commit it natively aka return false
        elif keyval==IBus.KEY_Return:
            return False
        return self.do_inputchar(keyval)
    #after do_process_key_event and you know it's a regular key so what to do with it
    capitalizeaftercommit=False
    def do_inputchar(self, inputchar):
        #if inputchar is space then commit current_input with appendables without using shortnengine and if no current_input then just commit space
        if IBus.keyval_to_unicode(inputchar) in self.overarchinglanguage.wordseparator:
            inputchar = IBus.keyval_to_unicode(inputchar)
            if self.current_input!="":
                rtr=self.overarchinglanguage.decodingtooriginal(self.current_input)
                rtr=self.appendables(rtr, encodingchange=False)
                if rtr!=inputchar and rtr!=None:
                    self.commit(str(rtr)+str(inputchar))
            else:
                self.commit(inputchar)
            self.shifttoggle=False
            self.setcand()
            self.cleareverything()
            if self.capitalizeaftercommit==True:
                self.shifttoggle=True
                self.capitalizeaftercommit=False
            return True
        elif inputchar == IBus.Page_Down:
            return self.do_page_down()
        elif inputchar == IBus.Page_Up:
            return self.do_page_up()
        #if you press delete then either current current_input removes one letter, if current_input not exist then return false so deletes in the "real world"
        elif inputchar == IBus.BackSpace:
            if not self.current_input:
                return False
            self.update_current_input(drop=1)
            self.setcand(self.shortnenginefunction(self.current_input))
            self.showtext(self.current_input)
            return True
        #if the thing is a number then treat it like selecting candidate thingie index
        elif is_inputnumber(inputchar):
            return self.do_number(inputchar)
        inputchar = IBus.keyval_to_unicode(inputchar)
        #turns the current_input into lowercase. necessary for shortn_engine
        try:
            inputchar=self.nocap(inputchar)
        except:
            True
        #if the inputchar is neither in latin alphabet nor a common punctuation then let it commit natively aka return false. so like #$% etc
        if inputchar not in self.acceptedshortnenginecharacterlist and inputchar not in self.commonpunctuation:
            return False
        #converts into injective latin set
        try:
            inputchar=self.overarchinglanguage.encodingfromoriginal(inputchar)
        except:
            True
        #if inputchar is a regular punctuation then make it self.addpunc (the punctuation variable). if current_input is empty then just commit addpunc and call it a day. if current_input is not empty then nothing happens other than self.addpunc being updated accordingly
        if inputchar in self.commonpunctuation:
            if inputchar=="." or inputchar=="?" or inputchar=="!":
                self.capitalizeaftercommit=True
            self.addpunc=inputchar
            #if you type a character in the list of common punctuation and curent input is empty then cleareverything and then capitalize 
            if self.current_input==None or self.current_input=="":
                self.commit(self.addpunc+" ")
                self.addpunc=None
                self.cleareverything
                if inputchar=="." or inputchar=="?" or inputchar=="!":
                    self.shifttoggle=True
                    self.capitalizeaftercommit=False
                return True
        else:
            #if inputchar is not punctuation then append it to current_input
            self.update_current_input(append=inputchar)
        #from current_input ask shortnengine for a list of suggestions. if list not empty then display it. then show the current_input.
        ut=self.shortnenginefunction(self.current_input)
        if ut!=None and type(ut)==list and type(ut)!=None:
            self.setcand(thelist=ut)
        self.showtext(self.current_input)
        return True


class EngineShortnfr(Engine):
    #The Shortn FR engine.
    __gtype_name__ = "EngineShortnfr"
    __name__ = "shortnfr"
    def nocap(self,the):
        a=""
        for i in the:
            a+=self.nocaplist.get(i,i)
        return a
    #turns a word into all lowercase except first letter that is uppercase
    def firstcap(self, the):
        if the==None:
            return True
        try:
            the=self.nocap(the)
        except:
            True
        if len(the)==1:
            return self.capital.get(the)
        return str(str(self.capital.get(the[:1],the[:1]))+str(the[1:]))
    #turns a word into all uppercase
    def allcap(self,the):
        a=""
        for i in the:
            a+=self.capital.get(i)
        return a
    #what to do when engine sees you typed a number
    def do_number(self, keyval):
        if self.lookuptable.get_number_of_candidates():
            a=int(IBus.keyval_to_unicode(keyval))
            if a==0:
                return False
            else:
                return self.do_select_candidate(a)
    #turns a normall lowercase word into the final product ie from 'hospital' to 'Hospital?' etc
    def appendables(self,a, encodingchange=True):
        the=a
        if the==" ":
            return " "
        elif the=="":
            return ""
        elif the==None:
            return None
        if encodingchange:
            the=self.overarchinglanguage.decodingtooriginal(the)
        if self.shifttoggle:
            the=self.firstcap(the)
        if self.addpunc!=None:
            the+=self.addpunc
        return the
    #once you get 'index' aka number what you do to it aka you choose from the list and input it
    def do_select_candidate(self, index):
        page_index = self.lookuptable.get_cursor_pos()
        selected = self.lookuptable.get_candidate(page_index+index-1)
        if selected!=None:
            b=selected.text
            b=self.overarchinglanguage.decodingtooriginal(b)
            b=self.appendables(b,encodingchange=False)+" "
            self.commit(b)
            self.shifttoggle=False
        self.cleareverything()
        if self.capitalizeaftercommit==True:
            self.shifttoggle=True
            self.capitalizeaftercommit=False
        return True
    #called by ibus. ie you use your mouse to click on a candidate
    def do_candidate_clicked(self, index, button, state):
        self.do_select_candidate(index+1)
    #from a word you get the last vowel aka type "hosptla" you get "a"
    def getlastvowel(self, inpp):
        inp=inpp
        a=[i for i in inp if i in self.vowels]
        if len(a)>1:
            return a[-1]
        else:
            return None
    #the main engine function. type "hosptl" and get "hospital"
    def shortnenginefunction(self, theinputt):
        theinput=theinputt
        a=self.getlastvowel(theinput)
        if a!=None:
            theinput=theinput[:-1]
        try:
            sug= self.dic.get(theinput)
        except:
            return None
        if a!=None:
            if type(sug)==list:
                b= [i for i in sug if self.getlastvowel(i)==a]
            else:
                return None
            if len(b)==0:
                return None
            else:
                return b
        else:
            return sug
    #when you press esc it "disables" the engine. these are its variables for that
    escapetoggle=True
    #sometimes the code needs an overflow variable. basically pressing one key once will have ibus interpret it as if you pressed it multiple times. these "overflow" variables are meant to prevent this. if a key is pressed multiple times under an interval lesser than 0.3 seconds it will only register it once
    escapeoverflow=time.time()
    #same thing but for pressing shift
    shifttoggle=False
    shiftoverflow=time.time()
    #when you type ANY key what to do
    def do_process_key_event(self, keyval, keycode, state):
        #if theres some issue with a user pressing keys too fast like return then delete and it not registering then change all elif to if 
        #mechanism for escape toggle. catches it and changes state
        if keyval==IBus.Escape and time.time()-self.escapeoverflow>0.3:
            self.escapetoggle= not self.escapetoggle
            if self.current_input!="":
                self.commit(self.overarchinglanguage.decodingtooriginal(self.current_input))
            self.cleareverything()
            self.escapeoverflow=time.time()
            return True
        #mechanism for escape toggle. if on, then return all false
        elif not self.escapetoggle:
            return False
        #when you press something without releasing it doesnt count?? ithink? 
        elif (state & IBus.ModifierType.RELEASE_MASK):
            return False
        # Ignore Alt+<key> and Ctrl+<key>
        elif state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK |IBus.ModifierType.MOD4_MASK):
            return False
        #mechanism for shift system
        if keyval==IBus.KEY_Shift_L and time.time()-self.shiftoverflow>0.3:
            self.shifttoggle=self.shifttoggle==False
            self.shiftoverflow=time.time()
            self.showtext(self.current_input)
            return False
        #if enter key pressed then commit it natively aka return false
        elif keyval==IBus.KEY_Return:
            return False
        return self.do_inputchar(keyval)
    #after do_process_key_event and you know it's a regular key so what to do with it
    capitalizeaftercommit=False
    def do_inputchar(self, inputchar):
        #if inputchar is space then commit current_input with appendables without using shortnengine and if no current_input then just commit space
        if IBus.keyval_to_unicode(inputchar) in self.overarchinglanguage.wordseparator:
            inputchar = IBus.keyval_to_unicode(inputchar)
            if self.current_input!="":
                rtr=self.overarchinglanguage.decodingtooriginal(self.current_input)
                rtr=self.appendables(rtr, encodingchange=False)
                if rtr!=inputchar and rtr!=None:
                    self.commit(str(rtr)+str(inputchar))
            else:
                self.commit(inputchar)
            self.shifttoggle=False
            self.setcand()
            self.cleareverything()
            if self.capitalizeaftercommit==True:
                self.shifttoggle=True
                self.capitalizeaftercommit=False
            return True
        elif inputchar == IBus.Page_Down:
            return self.do_page_down()
        elif inputchar == IBus.Page_Up:
            return self.do_page_up()
        #if you press delete then either current current_input removes one letter, if current_input not exist then return false so deletes in the "real world"
        elif inputchar == IBus.BackSpace:
            if not self.current_input:
                return False
            self.update_current_input(drop=1)
            self.setcand(self.shortnenginefunction(self.current_input))
            self.showtext(self.current_input)
            return True
        #if the thing is a number then treat it like selecting candidate thingie index
        elif is_inputnumber(inputchar):
            return self.do_number(inputchar)
        inputchar = IBus.keyval_to_unicode(inputchar)
        #turns the current_input into lowercase. necessary for shortn_engine
        try:
            inputchar=self.nocap(inputchar)
        except:
            True
        #if the inputchar is neither in latin alphabet nor a common punctuation then let it commit natively aka return false. so like #$% etc
        if inputchar not in self.acceptedshortnenginecharacterlist and inputchar not in self.commonpunctuation:
            return False
        #converts into injective latin set
        try:
            inputchar=self.overarchinglanguage.encodingfromoriginal(inputchar)
        except:
            True
        #if inputchar is a regular punctuation then make it self.addpunc (the punctuation variable). if current_input is empty then just commit addpunc and call it a day. if current_input is not empty then nothing happens other than self.addpunc being updated accordingly
        if inputchar in self.commonpunctuation:
            if inputchar=="." or inputchar=="?" or inputchar=="!":
                self.capitalizeaftercommit=True
            self.addpunc=inputchar
            #if you type a character in the list of common punctuation and curent input is empty then cleareverything and then capitalize 
            if self.current_input==None or self.current_input=="":
                self.commit(self.addpunc+" ")
                self.addpunc=None
                self.cleareverything
                if inputchar=="." or inputchar=="?" or inputchar=="!":
                    self.shifttoggle=True
                    self.capitalizeaftercommit=False
                return True
        else:
            #if inputchar is not punctuation then append it to current_input
            self.update_current_input(append=inputchar)
        #from current_input ask shortnengine for a list of suggestions. if list not empty then display it. then show the current_input.
        ut=self.shortnenginefunction(self.current_input)
        if ut!=None and type(ut)==list and type(ut)!=None:
            self.setcand(thelist=ut)
        self.showtext(self.current_input)
        return True