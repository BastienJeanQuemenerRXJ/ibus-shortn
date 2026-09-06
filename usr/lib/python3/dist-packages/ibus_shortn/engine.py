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




#try to replace multiple line if statements by one line if statements
#if age >= 18: print("Adult")
#and
#status = "Adult" if age >= 18 else "Minor"




#this is the list of valid shortn engines (ie languages here). EngineShortn is for english. EngineShortnfr is for french, and other languages (like say spanish=es, makes EngineShortnes). language code is 2 letters. before adding or removing anything here make sure that all the other config files are present or else does not load
__all__ = ["EngineShortn", "EngineShortnfr"]
#necessary
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
        
#import languageclassfile which does all the language config stuff 
try:
    from .languageclassfile import language  
except Exception as p:
    from languageclassfile import language

#the shortn engine. this is also the english (en) english because '''$ibus engine shortn''' has to return something instead of being only able to command '''ibus engine shortnen''' (shortnen as an engine doesn't exist by convention)
class Engine(IBus.Engine):
    """The base class for Shortn engines."""
    def __init__(self):
        # bash command $ibus engine shortn makes english shortn. equivalent to selecting english shortn keyboard. $ibus engine shortnfr makes for french. again, equivalent with native keyboards. the name of the engine, if not english, is shortn[x] where x is a 2 letter lower case language code, so, ru, de, fr, es, etc. ie shortnfr, shortnru, shortnes. there is no shortnen since shortn =default=english. it's the default because it was the easiest language to work with at first (no accents, no weird words (like aujourd'hui which uses a ') or compounding (like l'atmosphère where l' and atmosphère are separate words)).
        #if engine name is shortn then language is english, if not then it has to be of the form shortnLC, so cut down "shortn" to get LC which is the language code (fr, ru, de,es...)
        #overarchinglanguage is the language that the engine uses, dynamically changes whenever you change engine (shortnes->shortnfr etc). global variable
        #this is how we get the language code
        b=language.givelanguageanddic(self.__name__)
        self.overarchinglanguage=b[0]
        self.dic=b[1]
        #initializing the engine 
        super(Engine, self).__init__()
        #im not sure exactly. gets the schematics. useful for a native setting environment in the future. there's no "org.shortn-scheme.ibus" in the files but removing it breaks everything so idk. most likely i have to touch this to add native ui settings
        schema_id = "org.shortn-scheme.ibus.%s" % self.__name__
        self.settings = Gio.Settings(schema_id=schema_id)
        self.settings.connect("changed", self.on_value_changed)
        #current input 
        self.current_input = ""
        #current text shown (usually also current_input most of the time but don't merge the variables for good practice)
        self.current_showtext = ""
        #reset everything on next word (im not sure at all)
        self.clear_on_next_input = False
        #initializes the ui (i think?)
        self.lookuptable = IBus.LookupTable()
        #maximum candidate list showing size is 9 because beyond 9 is 10,11,12 and there's no 10, 11, 12... key on your keyboard (can only press 1 and then 0)
        #also we don't use 0 as a candidate index (for the user, keep in mind that python indexes start at 0 ie list[0] =first element) but maybe we could find a functionality for pressing 0
        self.lookuptable.set_page_size(9)
        #ideally something like this should be changeable in settings. what this does is that if you press candidate list to move up or down and it hits the end of the index, then it returns back to the original. if False then stops moving even if you press to move candidate list shown
        self.lookuptable.set_round(True)
        #ideally something like this should be changeable in settings. what it says on the tin: suggestions are displayed horizontally or vertically
        self.lookuptable.set_orientation(IBus.Orientation.HORIZONTAL)
        #there's a cursor (it highlights a specific candidate in the list that you can see, ie, on the shown candidate list. if you were to fork off of this you might want to turn it on to have an additional functionality to do something
        self.lookuptable.set_cursor_visible(False)
        self.init_properties()
        self.init_shortn()

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
    #shows you thestr in the edit window. keep in mind that what's shown is ran through appendables so for example if thestr=hosptl and shifttoggle is on and punctuationvariable is "," then what's shown is "Hosptl,". albeit be aware that shortnengine does NOT see "Hosptl," it will always only see "hosptl"
    #setting noencoding to True prevents the appendables
    def showtext(self, thestr, noencoding=False):
        if not noencoding:
            thestr=self.appendables(thestr)
        text = IBus.Text.new_from_string(thestr)
        super(Engine, self).update_auxiliary_text(text, len(thestr)>0)
        # We don't use pre-edit at all for Shortn or Quick. However, some applications (most notably Firefox) fail to correctly position the candidate popup, as if they got confused by the absence of a pre-edit text. fix this 
        if thestr:
            super(Engine, self).update_preedit_text(IBus.Text.new_from_string('\u200B'), 0, True)
        else:
            super(Engine, self).update_preedit_text(IBus.Text.new_from_string(''), 0, False)
    

    #sets the list of candidates from a list of strings called thelist. if thelist==None then removes the candidate list panel. if justupdate=True then it simply updates what should be shown without needing to change the actual candidate list itself. so if the candidate list doesnt change but you want to change how the panel looks, this is what you want
    def setcand(self, thelist=None, justupdate=False):
        if justupdate:
            self.update_lookup_table(self.lookuptable, self.lookuptable.get_number_of_candidates()>0)
            return True
        self.lookuptable.clear()
        if thelist!=None:
            num_candidates = 0
            for c in thelist:
                self.lookuptable.append_candidate(IBus.Text.new_from_string(c))
                num_candidates += 1
        self.update_lookup_table(self.lookuptable, self.lookuptable.get_number_of_candidates()>0)
        return True
    #this does something with respect to ibus keyboard localization settings or something idk. came from ibus-cangjie
    def init_properties(self):
        self.prop_list = IBus.PropList()
        for (key, label) in (("halfwidth-chars", "Half-Width Characters"),):
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
            self.prop_list = IBus.PropList()
    #'activates the properties'. idk this came from ibus-cangjie. i'm guessing something to do with ibus keyboard localization config. ie it 'activates' the properties of that. not sure
    def do_property_activate(self, prop_name, state):
        active = state == IBus.PropState.CHECKED
        self.settings.set_boolean(prop_name, active)
    #when you switch windows or tabs back, it changes keyboard
    def do_focus_in(self):
        self.register_properties(self.prop_list)
    #came from ibus-cangjie but again idk what this does exactly or if it does anything. it "gets the version of the settings". im guessing ibus keyboard localization settings
    def init_shortn(self):
        version = self.settings.get_int("version")
    #came from ibus-cangjie. idk what this really does. i'm guessing if something goes bad to recreate (restart) the engines. idk
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
    #move down the candidate selection list
    def do_page_down(self):
        #Present the next page of candidates. However, if there isn't any current input, then we shouldn't try to do anything at all, so that the key can fulfill its original function.
        if not self.lookuptable.get_number_of_candidates():
            return False
        self.lookuptable.page_down()
        #updates lookuptable
        self.setcand(justupdate=True)
        return True
    #move up the candidate selection list
    def do_page_up(self):
        #Present the previous page of candidates. However, if there isn't any current input, then we shouldn't try to do anything at all, so that the key can fulfill its original function.
        if not self.lookuptable.get_number_of_candidates():
            return False
        self.lookuptable.page_up()
        #updates lookuptable
        self.setcand(justupdate=True)
        return True
    #return to base state
    def cleareverything(self):
        """Clear the current input."""
        self.current_input = ""
        self.clear_on_next_input = False
        self.updatecandidatelistshortn()
        self.punctuationvariable=None
        self.showtext("")
        return True
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
    """The English Shortn engine."""
    __gtype_name__ = "EngineShortn"
    __name__ = "shortn"
    #the global punctuation variable
    punctuationvariable=None
    #the "when you press esc it "disables" the engine" variable
    disabletoggle=True
    #the capitalization system variable
    shifttoggle=False
    #when you type . or ! or ? it capitalizes the word after, it needs a new variable to do that
    capitalizeaftercommit=False
    
    #turns a word into all lowercase
    def nocap(self, the):
        a=""
        for i in the:
            a+=self.overarchinglanguage.originalalphabetuppercasetolowercase.get(i,i)
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
            return self.overarchinglanguage.originalalphabetlowercasetouppercase.get(the)
        return str(str(self.overarchinglanguage.originalalphabetlowercasetouppercase.get(the[:1],the[:1]))+str(the[1:]))
    #turns a word into all uppercase
    def allcap(self,the):
        a=""
        for i in the:
            a+=self.overarchinglanguage.originalalphabetlowercasetouppercase.get(i)
        return a

    #turns a normal lowercase word into the final product ie from 'hospital' to 'Hospital?' etc
    def appendables(self,a, encodingchange=True):
        the=a
        if the==" ":
            return " "
        elif the=="":
            return ""
        elif the==None:
            return None
        if encodingchange:
            the=self.overarchinglanguage.decoding(the)
        if self.shifttoggle:
            the=self.firstcap(the)
        if self.punctuationvariable!=None:
            the+=self.punctuationvariable
        return the
    #once you get 'index' aka number what you do to it aka you choose from the list and input it
    def do_select_candidate(self, index):
        #when you move up the candidate list, there's an issue where selecting a candidate doesnt select the right one. it fixes that. basically get_cursor_pos is where the engine situates where the candidate list is shown but it should be a multiple of 9
        selected = self.lookuptable.get_candidate(9*(self.lookuptable.get_cursor_pos()//9)+index-1)
        if selected!=None:
            #gets from selected from candidate list, turns it into ibus text, decodes, appendables, commits, removes caps, clears everything, if capitalizeaftercommit then purn caps back on and disable capitalizeaftercommit
            self.commit(selected.text+" ")
            self.shifttoggle=False
        self.cleareverything()
        #this is the capitalizeaftercommit mechanism. necessary because otherwise if someone types "test." it would capitalize "test" itself, ie typing "test. word " would make "Test. word" which we don't want (we want "test. word "->"test. Word ")
        if self.capitalizeaftercommit:
            self.shifttoggle=True
            self.capitalizeaftercommit=False
        return True
    #called by ibus. ie you use your mouse to click on a candidate
    def do_candidate_clicked(self, index, button, state):
        self.do_select_candidate(index+1)
    #from a word you get the last vowel aka type "hosptla" you get "a"
    def getlastvowel(self, inp):
        a=[i for i in inp if i in self.overarchinglanguage.encodedvowel]
        if len(a)>1:
            return a[-1]
        else:
            return None
    #the main engine function. type "hosptl" and get "hospital". also includes lastvowel system so "hosptla"->hosptl etc
    def shortnenginefunction(self, theinput):
        lastvowelvar=self.getlastvowel(theinput)
        if lastvowelvar!=None:
            theinput=theinput[:-1]
        try:
            sug= self.dic.get(theinput)
        except:
            return None
        if lastvowelvar!=None:
            try:
                b= [i for i in sug if self.getlastvowel(i)==lastvowelvar]
                t=b[0]
                return b
            except:
                return None
        return sug
    #this is setcand but fit for shortn. setcand is more of a "universal" function without any shortn specific thing or something. updatecandidatelistshortn is setcand but with appendables and decoding at the end 
    def updatecandidatelistshortn(self):
        if self.current_input=="":
            return self.setcand()
        i=self.shortnenginefunction(self.current_input)
        if i==None:
            self.setcand()
        else:
            self.setcand([self.appendables(self.overarchinglanguage.decoding(k)) for k in i])
        return True
        
    
    #called by ibus do not rename this function. when you type ANY key what to do
    def do_process_key_event(self, keyval, keycode, state):
        #ignore key release events AND ALSO PREVENTS KEYS GETTING "BOUNCED" IE IF U PRESS A KEY ONCE IT REGISTERS MULTIPLE TIMES. ie IT DEBOUNCES
        #normally we should set it to return true but ibus crashes and becomes too annoying if we do so im not sure exactly 
        if state & IBus.ModifierType.RELEASE_MASK:
            return False
        #mechanism for disable toggle. catches it and changes state
        if keyval == IBus.KEY_space and state & IBus.ModifierType.SHIFT_MASK:
            self.disabletoggle= not self.disabletoggle
            if self.current_input!="":
                self.commit(self.overarchinglanguage.decoding(self.current_input))
            self.cleareverything()
            return True
        #mechanism for disable toggle. if on, then return all false
        if not self.disabletoggle:
            return False
        # Ignore Alt+<key> and Ctrl+<key>
        elif state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK |IBus.ModifierType.MOD4_MASK):
            return False
        #mechanism for shift system
        if keyval==IBus.KEY_Shift_L:
            self.shifttoggle=self.shifttoggle==False
            self.showtext(self.current_input)
            self.updatecandidatelistshortn()
            return True
        #if enter/return/newline key pressed then commit it natively aka return false
        elif keyval==IBus.KEY_Return:
            return False
        #if you click on the page up or down button then it moves up and down the suggestion list since candidates shown is limited to 9
        if keyval == IBus.Page_Down:
            return self.do_page_down()
        elif keyval == IBus.Page_Up:
            return self.do_page_up()
        #if you press delete then either current current_input loses one letter, if punctuationvariable exists then just remove punctuationvariable, if current_input not exist then return false so deletes in the "real world"
        elif keyval == IBus.BackSpace:
            return self.do_backspace()
        #turns keyval from an ibus text to a regular text. IBus.space !=" " automatically
        elif keyval==IBus.space:
            keyval=" "
        else:
            try:
                keyval=IBus.keyval_to_unicode(keyval)
            except:
                True  
        return self.do_regular_key(keyval)
    #what to do when the entered key is a word separator (ie -, _, space) now it functions like regular punctuation but it just commits directly. the use case is to not have to remove space
    def do_wordseparator(self,entered_word_separator):
        #if inputchar is space or - or _ then commit current_input with appendables without using shortnengine and if no current_input then just commit space
        #makes sure current_input isn't empty. if not empty then commits current_input+word_separator
        if self.current_input!="":
            #decodes current_input back to original alphabet
            self.current_input=self.overarchinglanguage.decoding(self.current_input)
            #adds appendables
            self.current_input=self.appendables(self.current_input, encodingchange=False)
            #commits current_input+wordseparator
            self.commit(str(self.current_input)+str(entered_word_separator))
        else:
            #if current_input is empty then just commit entered_word_separator
            self.commit(str(entered_word_separator))
        #we just commited something so turn off caps, reset setcand. but, if capitalize after commit is on, then turn shifttoggle on, and disabled capitalizeaftercommit
        self.shifttoggle=False
        self.cleareverything()
        if self.capitalizeaftercommit==True:
            self.shifttoggle=True
            self.capitalizeaftercommit=False
        self.updatecandidatelistshortn()
        return True
    #when inputchar is a punctuation
    #if inputchar is a regular punctuation then make it self.punctuationvariable (the punctuation variable). if current_input is empty then just commit punctuationvariable and call it a day. if current_input is not empty then nothing happens other than self.punctuationvariable being updated accordingly
    def do_punctuation(self,punctuationn):
        #there's a difference between .?! and ,;: because the former should capitalize the next word
        if punctuationn in {".", "?","!"}:
            self.capitalizeaftercommit=True
        #punctuationvariable is a global variable that appendables calls
        self.punctuationvariable=punctuationn
        #if you type a character in the list of common punctuation and curent input is empty then cleareverything and then capitalize 
        if self.current_input=="":
            self.commit(self.punctuationvariable+" ")
            self.cleareverything()
            if self.capitalizeaftercommit:
                self.capitalizeaftercommit=False
                self.shifttoggle=True
        else:
            self.showtext(self.current_input)
        self.updatecandidatelistshortn()
        return True
    
    #if you press delete then either current current_input loses one letter, if punctuationvariable exists then just remove punctuationvariable, if current_input not exist then return false so deletes in the "real world"
    def do_backspace(self):
        if not self.current_input:
            return False
        if self.punctuationvariable!=None and self.punctuationvariable!="":
            self.punctuationvariable=None
        else:
            self.update_current_input(drop=1)
        self.showtext(self.current_input)
        self.updatecandidatelistshortn()
        return True
    #what to do when engine sees you typed a number
    def do_number(self, keyval):
        #this is the thing to add a word to the dictionary natively when pressing 0
        if keyval==0:
            try:
                from .make_dict import add_to_dic_class
                add_to_dic_class.whattodo("add",[self.current_input], self.overarchinglanguage.dictionaryname[:-5])
            except Exception as p:
                p="failed to add to dictionary because of "+getattr(p, 'message', repr(p))
                self.commit(p)
            self.cleareverything
            return True
        #get candidate list
        if self.lookuptable.get_number_of_candidates():
            return self.do_select_candidate(keyval)
        return False

        
    #after do_process_key_event and you know it's a regular key so what to do with it
    def do_regular_key(self, inputchar):
        #if the thing is a number then treat it like selecting candidate index
        #this try except method is the best way to check if a str is a number
        try:
            a=int(inputchar)
            return self.do_number(a)
        except:
            True
        #pressing + or - moves up and down the shown suggestion list since candidates shown is limited to 9
        if inputchar=="+": return self.do_page_up()
        #commented out because typing "-" is already used as a wordseparator, and moving candidate list is already a niche feature that isn't gonna be used regularly. so having it conflicts with being able to type "-"
        #elif inputchar=="-": return self.do_page_down()
    
        #turns the current_input into lowercase. necessary for shortn_engine. keep in mind it's NOT converted into the injective latin set. so, it's   input->nocap(input) ->convert(nocap(input))->shortnengine(convert(nocap(input))) -> deconvert(shortnengine(convert(nocap(input))))->appendables(deconvert(shortnengine(convert(nocap(input))))))
        try:
            inputchar=self.nocap(inputchar)
        except:
            True
        #if the inputchar is neither in alphabet nor a common punctuation then let it commit natively aka return false. so like #$% etc
        if inputchar not in self.overarchinglanguage.originalalphabet and inputchar not in self.overarchinglanguage.punctuation and inputchar not in self.overarchinglanguage.wordseparator:
            return False
        #if typed character (inputchar) is in wordseparator then do the word_separator. ie space_- (this changes, for example in french we treat ' as a wordseparator to type l' (as in l'atmsphr-> commits l' then asks you to select atmsphr to make "l'atmosphère")
    
        if inputchar in self.overarchinglanguage.wordseparator:
            return self.do_wordseparator(inputchar)
        #if inputchar is a regular punctuation like ,.?;:!
        if inputchar in self.overarchinglanguage.punctuation:
            return self.do_punctuation(inputchar)
        #converts into injective latin set
        try:
            inputchar=self.overarchinglanguage.encoding(inputchar)
        except:
            True
        #since inputchar is a regular letter for shortnengine then append it to current_input
        self.update_current_input(append=inputchar)
        #from current_input ask shortnengine for a list of suggestions. if list not empty then display it. then show the current_input.
        self.updatecandidatelistshortn()
        #keep in mind showtext has appendables inside
        self.showtext(self.current_input)
        return True

#so EngineShortn is actually the default engine which is also english. making a new engine changes that like below
class EngineShortnfr(EngineShortn):
    #The Shortn FR engine.
    __gtype_name__ = "EngineShortnfr"
    __name__ = "shortnfr"
