# ibus-shortn

The Shortn algorithm and its IME is quite simple. Type the word you want, but without all the vowels, except the first one, if there are too many results, type the last vowel at the end to refine them, then select it.

For example, to type "humanity", you would type "humnt". You would see two results appearing '[1]  humanate', and '[2] humanity'. you can either add a 'y', thereby making it "humnty", refining the result to just one, and then clicking 1. or clicking 2. the IME then adds a space to prevent unnecessary strokes. in the end you will have typed "humnt2" instead of "humanity ", resulting in 3 less strokes typed. IE:

* "humanity "
vs
* "humnt2"


# Commands
* pressing 'esc' disables the engine, thereby letting you type normally. repressing it enables it again. keep in mind that pressing 'esc' does not actually unload anything, the engine and dictionary are still running and active. in case of a bug, do ```pkill ibus``` which will disable all ibus IMEs but keep you with non-IME IBus keyboards (russian, french, english, etc). 
* pressing left shift once will capitalize the first letter of your word. clicking it again makes it all caps. clicking it again reverts to lower case. this is a workaround but it works for now. it is planned to allow you to hold shift to be able to capitalize only the first letter of your word. and to have caps lock work too.
* pressing ',.;: before validating your word will add it before your word and then add a space.  ie,  typing "humnty,1" will give "humanity, "
  


But let me show you that on camera: 

test


# installing
* debian: 

```
sudo apt-get install git && sudo apt-get install python3 && sudo apt-get install ibus && sudo git clone https://github.com/BastienJeanQuemenerRXJ/ibus-shortn.git && cd ibus-shortn/ && cd .. && dpkg-deb --root-owner-group --build ibus-shortn && sudo dpkg -i ibus-shortn.deb && ibus restart
```
if you have multiple keyboards (like russian, chinese, japanese, arabic...) it should add itself automatically to that as long as all your keyboards are on ibus

# to do list
 * writing "mcknight?" will only show "mcknight" but still output "mcknight? " if you press space
 * writing a word and then "." like "absltly." will cause a lag spike
 * fix 'enter' not working on ubuntu text editor
 * make it such that pressing caps makes the text in all caps (while accounting for the shortn algorithm) instead of needing to click left shift twice.
 * add frequency sorting for results
 * add customizable settings
 * add support for french
 * add support for russian
 * add support for more languages

