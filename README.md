# ibus-shortn
A deterministic IME to type faster in alphabetic-using languages containing on average more consonants than vowels per word. gplv3, Forked from ibus-cangjie


https://github.com/user-attachments/assets/6dd0051c-056c-4096-b4c7-c2123ab6a111

The Shortn algorithm and its IME is quite simple. Type the word you want, but without all the vowels, except the first one, if there are too many results, type the last vowel at the end to refine them, then select it.

For example, to type "humanity", you would type "humnt". You would see two results appearing '[1] humanate', and '[2] humanity'. you can either add a 'y', thereby making it "humnty", refining the result to just "[1] humanity", and then tapping '1', or writing "humnt" and clicking 2. the IME then adds a space to prevent unnecessary strokes. in the end you will have typed "humnt2" instead of "humanity ", resulting in 3 less strokes typed. IE:

* "humanity "
vs
* "humnt2"


# languages 
* Fully functional in French (traditional-canadian-qwerty keyboard, better azerty configuration coming soon). Video coming soon. 
* Russian is almost ready.
* Spanish, German are planned
# Commands
* pressing 'shift +space' disables the engine, thereby letting you type normally. repressing it enables it again. keep in mind that pressing 'shift+space' does not actually unload anything, the engine and dictionary are still running and active. in case of a bug, do ```pkill ibus``` which will disable all ibus IMEs but keep you with non-IME IBus keyboards (russian, french, english, etc). 
* pressing left shift makes it such that the first letter of your word will be capitalized. right shift functions normally (ie pressing right shift +1 makes ! but right shift +a still makes a, it doesn't capitalize).
* pressing ,.;:!? before validating your word will add it after your word and then add a space.  ie,  typing "humnty,1" will give "humanity, "
* pressing .!? specifically will capitalize the next word automatically, ie typing "undrsttd.1hello " will give "understated. Hello "
* pressing -_space before validating a word will automatically commit what you exactly inputted but capitalized and with the punctuation at the end.
* to add a word to the dictionary, type the full word (ie:"malware") and press 0.



# installing

Dependencies :

```python3, git, ibus```

* debian: 

```sudo apt-get install ibus && sudo apt-get install python3 && sudo apt-get install git```

```cd && sudo git clone https://github.com/BastienJeanQuemenerRXJ/ibus-shortn.git && cd ibus-shortn/ && sudo dpkg -i ibus-shortn.deb && ibus restart```


Setting up:

* debian:

To launch it you can either do ```ibus engine shortn[languagecode, if english then just write shortn]``` to launch it from the terminal, or, more natively, go to ubuntu settings, keyboard, add language, go to 'English-US', select 'shortn',  for french go to 'French-FR', select 'raccrcr' or 'shortnfr' or 'shortn'

will add fedora and arch soon

# Copyright

 Copyright (c) 2012-2013 - The IBus Cangjie authors (https://gitlab.freedesktop.org/cangjie/ibus-cangjie/)

 list of English words upon which the shortn dictionary uses is https://github.com/dwyl/english-words/blob/master/words_alpha.txt

 Copyright (c) 2026 - Bastien Jean Quemener <shortn@bastien.live>  (github.com/BastienJeanQuemerRXJ/ibus-shortn)

 This file is part of ibus-shortn, the IBus Shortn input method engine, forked from ibus-cangjie.

 ibus-shortn is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 ibus-shortn is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with ibus-shortn.  If not, see <http://www.gnu.org/licenses/>.
