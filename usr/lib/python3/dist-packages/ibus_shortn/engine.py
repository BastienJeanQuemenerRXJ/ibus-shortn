#!/usr/bin/python3
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






__all__ = ["EngineShortn"]
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



def is_inputnumber(keyval):
    """Is the `keyval` param a numeric input, e.g to select a candidate."""
    return ((keyval in range(getattr(IBus, "0"), getattr(IBus, "9")+1)) or
            (keyval in range(IBus.KP_0, IBus.KP_9+1)))


class Engine(IBus.Engine):
    """The base class for Shortn and Quick engines."""
    def __init__(self):
        self.dic=self.loaddic()
        thename=self.__name__
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
    #loads dictionary. call it only once. the dictionary stays loaded. to call it. self.dic. 
    def loaddic(self,curdic="/usr/lib/python3/dist-packages/ibus_shortn/en-dic.json"):
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
    #shows you thestr in the edit window
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
    def setcand(self, thelist=None,tables=False, additionalfunc=None):
        if tables==True:
            if not self.current_input:
                self.setcand()
            self.update_lookup_table(self.lookuptable, self.lookuptable.get_number_of_candidates()>0)
            return True
        self.lookuptable.clear()
        if thelist!=None:
            num_candidates = 0
            for c in thelist:
                abcd=c
                if additionalfunc!=None:
                    abcd=additionalfunc(abcd)
                self.lookuptable.append_candidate(IBus.Text.new_from_string(abcd))
                num_candidates += 1
        self.update_lookup_table(self.lookuptable, self.lookuptable.get_number_of_candidates()>0)
    def init_properties(self):
        self.prop_list = IBus.PropList()

        for (key, label) in (("halfwidth-chars", gettext.dgettext("ibus-shortn", "Half-Width Characters")),):
            stored_value = self.settings.get_boolean(key)
            state = IBus.PropState.CHECKED if stored_value else IBus.PropState.UNCHECKED

            try:
                # Try the new constructor from IBus >= 1.5
                prop = IBus.Property(key=key, prop_type=IBus.PropType.TOGGLE, label=label, icon='', sensitive=True, visible=True, state=state, sub_props=None)
            except TypeError:
                # IBus 1.4.x didn't have the GI overrides for the nice
                # constructor, so let's do it the old, non-pythonic way.
                #   IBus.Property.new(key, type, label, icon, tooltip, sensitive, visible, state, sub_props)
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

    def do_page_down(self):
        #Present the next page of candidates. However, if there isn't any current input, then we shouldn't try to do anything at all, so that the key can fulfill its original function.
        if not self.lookuptable.get_number_of_candidates():
            return False

        self.lookuptable.page_down()
        self.setcand(tables=True)
        self.showtext(self.current_showtext)
        return True

    def do_page_up(self):
        #Present the previous page of candidates. However, if there isn't any current input, then we shouldn't try to do anything at all, so that the key can fulfill its original function.
        if not self.lookuptable.get_number_of_candidates():
            return False

        self.lookuptable.page_up()
        self.setcand(tables=True)
        self.showtext(self.current_showtext)
        return True


    def cleareverything(self):
        """Clear the current input."""
        self.current_input = ""
        self.current_showtext=""
        self.clear_on_next_input = False
        self.setcand(tables=True)
        self.showtext(self.current_showtext)
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
    vowels={'a', 'e', 'i', 'o', 'u', 'y'}
    englishlistfilter01={"a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G", "h", "H", "i", "I", "j", "J", "k", "K", "l", "L", "m", "M", "n", "N", "o", "O","p", "P", "q", "Q", "r", "R", "s", "S", "t", "T","u", "U", "v", "V", "w", "W", "x", "X", "y", "Y", "z", "Z", "'"}
    englishpunctuation={"?", "!", ".", ";", ","}
    capital ={ "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O","p": "P", "q": "Q", "r": "R", "s": "S", "t": "T","u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "'":"'", " ": " "}
    nocaplist = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n", "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t","U": "u", "V": "v", "W": "w", "X": "x", "Y": "y","Z": "z", "'": "'", " ": " "}
    addpunc=None
    
    def nocap(self, the):
        a=""
        for i in the:
            try:
                a+=self.nocaplist.get(i)
            except:
                a+=i
        return a
    def firstcap(self, the):
        if the==None:
            return True
        try:
            the=self.nocap(the)
        except:
            True
        if len(the)==1:
            the=self.capital.get(the)
            return the
        try:
            a=self.capital.get(the[:1])
        except:
            a=the[:1]
        the=str(str(a)+str(the[1:]))
        return the
        
    def allcap(self,the):
        a=""
        for i in the:
            a+=self.capital.get(i)
        return a


    def do_number(self, keyval):
        if self.lookuptable.get_number_of_candidates():
            a=int(IBus.keyval_to_unicode(keyval))
            if a==0:
                return False
            else:
                return self.do_select_candidate(a)
    def appendables(self,the):
        if the==" ":
            return " "
        if the=="":
            return ""
        if the==None:
            return None
        if self.capstoggle:
            the=self.firstcap(the)
        if self.addpunc!=None:
            the+=self.addpunc
        return the+" "
    def do_select_candidate(self, index):
        page_index = self.lookuptable.get_cursor_pos()
        selected = self.lookuptable.get_candidate(page_index+index-1)
        if selected!=None:
            b=selected.text
            b=self.appendables(b)
            self.commit(b)
        self.addpunc=None
        self.cleareverything()
        return True
    #called by ibus
    def do_candidate_clicked(self, index, button, state):
        self.do_select_candidate(index+1)
    def getlastvowel(self, inpp):
        inp=inpp
        a=[i for i in inp if i in self.vowels]
        if len(a)>1:
            return a[-1]
        else:
            return None
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
    escapetoggle=True
    capstoggle=False
    #sometimes the code needs an overflow variable. basically pressing one key once will have ibus interpret it as if you pressed it multiple times. these "overflow" variables are meant to prevent this. if a key is pressed multiple times under an interval lesser than 0.3 seconds it will only register it once
    capsoverflow=time.time()
    def do_process_key_event(self, keyval, keycode, state):
        if keyval==IBus.Caps_Lock and time.time()-self.capsoverflow>0.3:
            self.capstoggle=self.capstoggle==False
            self.capsoverflow=time.time()
            return False
        if keyval==IBus.KEY_Return:
            self.forward_key_event(keyval, keycode, state)
            return True
        elif (state & IBus.ModifierType.RELEASE_MASK):
            return False
        elif state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK |IBus.ModifierType.MOD4_MASK):
            # Ignore Alt+<key> and Ctrl+<key>
            return False
        elif keyval==IBus.Escape:
            self.escapetoggle=self.escapetoggle==False
            self.addpunc=None
            self.cleareverything()
        return self.do_inputchar(keyval)

    def do_inputchar(self, inputchar):
        if not self.escapetoggle:
            return False
        if inputchar == IBus.space:
            if self.current_input!="":
                rtr=self.appendables(self.current_input)
                if rtr!=" " and rtr!=None:
                    self.commit(str(rtr))
            else:
                self.commit(str(" "))
            self.setcand()
            self.addpunc=None
            self.cleareverything()
            return True
        elif inputchar == IBus.Page_Down:
            return self.do_page_down()
        elif inputchar == IBus.Page_Up:
            return self.do_page_up()
        elif inputchar == IBus.BackSpace:
            if not self.current_input:
                return False
            self.update_current_input(drop=1)
            self.setcand(self.shortnenginefunction(self.current_input))
            self.showtext(self.current_input)
            return True
        elif is_inputnumber(inputchar):
            return self.do_number(inputchar)
        inputchar = IBus.keyval_to_unicode(inputchar)
        try:
            inputchar=self.nocap(inputchar)
        except:
            True
        if inputchar not in self.englishlistfilter01 and inputchar not in self.englishpunctuation:
            return False 
        if inputchar in self.englishpunctuation:
            self.addpunc=inputchar
            if self.current_input==None or self.current_input=="":
                self.commit(self.addpunc+" ")
                time.sleep(0.1)
                self.cleareverything()
                self.addpunc=None
                return True
        else:
            self.update_current_input(append=inputchar)
        ut=self.shortnenginefunction(self.current_input)    
        if ut!=None and type(ut)==list and type(ut)!=None:
            self.setcand(thelist=ut)
        self.showtext(self.current_input)
        return True

        