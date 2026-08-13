# ibus-shortn

https://github.com/user-attachments/assets/6dd0051c-056c-4096-b4c7-c2123ab6a111

The Shortn algorithm and its IME is quite simple. Type the word you want, but without all the vowels, except the first one, if there are too many results, type the last vowel at the end to refine them, then select it.

For example, to type "humanity", you would type "humnt". You would see two results appearing '[1] humanate', and '[2] humanity'. you can either add a 'y', thereby making it "humnty", refining the result to just "[1] humanity", and then tapping '1', or writing "humnt" and clicking 2. the IME then adds a space to prevent unnecessary strokes. in the end you will have typed "humnt2" instead of "humanity ", resulting in 3 less strokes typed. IE:

* "humanity "
vs
* "humnt2"
(the added space feature can be disabled)

# Commands
* pressing 'esc' disables the engine, thereby letting you type normally. repressing it enables it again. keep in mind that pressing 'esc' does not actually unload anything, the engine and dictionary are still running and active. in case of a bug, do ```pkill ibus``` which will disable all ibus IMEs but keep you with non-IME IBus keyboards (russian, french, english, etc). 
* pressing left shift once will capitalize the first letter of your word. clicking it again makes it all caps. clicking it again reverts to lower case. this is a workaround but it works for now. it is planned to allow you to hold shift to be able to capitalize only the first letter of your word. and to have caps lock work too.
* pressing ',.;: before validating your word will add it before your word and then add a space.  ie,  typing "humnty,1" will give "humanity, "



# installing

Dependencies :

```python3, git, ibus```

* debian: 

```sudo apt-get install ibus && sudo apt-get install python3 && sudo apt-get install git```

```sudo git clone https://github.com/BastienJeanQuemenerRXJ/ibus-shortn.git && cd ibus-shortn/ && cd .. && dpkg-deb --root-owner-group --build ibus-shortn && sudo dpkg -i ibus-shortn.deb && ibus restart```


Setting up:

* debian:

To launch it you can either do ```ibus engine shortn``` to launch it from the terminal, or, more natively, go to ubuntu settings, keyboard, add language, go to 'English-US', select 'shortn'.



# to do list
 * make a usable caps case system. -> add a detector for caps lock.     remove toggletime. make it such that shortn detects whether caps lock is enabled or not. automatic input conversion scheme to lower case (A->a, B->b). when word is committed with caps lock enabled, make the word committed in (conversion) caps. as for capitalizing only the first letter, add a variable that checks if the first letter of the word was typed in caps.

 * writing "mcknight?" will only show "mcknight" but still output "mcknight? " if you press space
 * fix 'enter' not working on ubuntu text editor
 * make it such that pressing caps makes the text in all caps (while accounting for the shortn algorithm) instead of needing to click left shift twice.
 * add english-dicmaker.py 
 * add frequency sorting for results
 * add customizable settings
 * add support for non ISO basic Latin alphabet languages (russian, french, german)->the issue is that non iso basic latin characters take way more place (for example a russian shortn dictionary takes 40mb while the english one takes 8mb. this is because the code for basic latin letters are short (latin 'a' in hex is '41', whereas cyrillic "а" is '0xD0 0xB0' which enhances necessary storage for cyrillic words. the idea is that non basic latin characters will be converted into latin as output and input. IE, Russian types "алфвт", IME converts it into alfvt, IME then searches alfvt into the russian dictionary, finds "alfvt->alfavit", then at the end converts alfavit into алфавит. since cyrillic has more letters than latin, and the conversion needs to be injective (1 to 1), case (a->A) can be used since it's not used in dictionaries (no difference between Алфавит and алфавит in the dictionary since case is inputted by the user). so the conversion scheme will look like "а <=> a", "б <=> b", "я <=> A", "в <=> v", "ю <=> U", "ъ <=> x", "ь <=> X" etc



