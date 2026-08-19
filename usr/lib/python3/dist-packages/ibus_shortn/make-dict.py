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



class language:
    def __init__(self, originalalphabet, originalalphabetlowercasetouppercase, originalalphabetuppercasetolowercase, encodingfromoriginal, decodingtooriginal, encodedvowel, punctuation, dictionaryname):
        self.originalalphabet = originalalphabet  
        self.originalalphabetlowercasetouppercase = originalalphabetlowercasetouppercase
        self.originalalphabetuppercasetolowercase = originalalphabetuppercasetolowercase
        self.encodingfromoriginal = encodingfromoriginal
        self.decodingtooriginal = decodingtooriginal
        self.encodedvowel = encodedvowel
        self.punctuation = punctuation
        self.dictionaryname = dictionaryname
    def encoding(self, the,scheme):
        a=""
        for i in the:
            try:
                a+= self.originalalphabetuppercasetolowercase.get(i)
            except:
                a+=i
        the=a
        a=""
        for i in the:
            try:
                a+= scheme.get(i)
            except:
                a+=i
        return a
    def decoding(self, the, scheme):
        a=""
        for i in the:
            try:
                a+= scheme.get(i)
            except:
                a+=i
        return a
        

english=language(
    {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "'"},
    { "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O","p": "P", "q": "Q", "r": "R", "s": "S", "t": "T","u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "'":"'", " ": " "},
    {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n", "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t","U": "u", "V": "v", "W": "w", "X": "x", "Y": "y","Z": "z", "'": "'", " ": " "},
    lambda x:x,
    lambda x:x,
    {'a', 'e', 'i', 'o', 'u', 'y'},
    {"?", "!", ".", ";", ","},
    "en-dic.json"
    )


french=language(
    {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ö", "ä", "ü", "ï", "ë", "ù", "è", "à", "ç", "ô", "â", "ê", "î", "û", "é", "'"},
    { "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O","p": "P", "q": "Q", "r": "R", "s": "S", "t": "T","u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "'":"'", " ": " ","ö":"Ö","ä":"Ä","ü":"Ü","ï":"Ï","ë":"Ë","ù":"Ù","è":"È","à":"À","ç":"Ç","ô":"Ô","â":"Â","ê":"Ê","î":"Î","û":"Û","é":"É" },
    {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n", "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t","U": "u", "V": "v", "W": "w", "X": "x", "Y": "y","Z": "z", "'": "'", " ": " ", "Ö":"ö","Ä":"ä","Ü":"ü","Ï":"ï","Ë":"ë","Ù":"ù","È":"è","À":"à","Ç":"ç","Ô":"ô","Â":"â","Ê":"ê","Î":"î","Û":"û","É":"é"},
    lambda x : french.encoding(x, {"ö":"O", "ä":"A", "ü":"U", "ï":"I", "ë":"E", "ù":"Y", "è":"R", "à":"W", "ç":"C", "ô":"K", "â":"S", "ê":"F", "î":"V", "û":"N", "é":"M"}),
    lambda x : french.decoding(x, {"O":"ö", "A":"ä", "U":"ü", "I":"ï", "E":"ë", "Y":"ù", "R":"è", "W":"à", "C":"ç", "K":"ô", "S":"â", "F":"ê", "V":"î", "N":"û", "M":"é"}),
    {'a', 'e', 'i', 'o', 'u', 'y', "O", "A", "U", "I", "E", "Y", "R", "W", "C", "K", "S", "F", "V", "N", "M"},
    {"?", "!", ".", ";", ","},
    "fr-dic.json"
    )

overarchinglanguage=french



#list of words to add to dictionary
in_=overarchinglanguage.dictionaryname[:7]+"txt"
#preexisting dictionary to add from
supportdic=None
#target dictionary to write as
out=overarchinglanguage.dictionaryname
import json
if supportdic!=None:
    with open(supportdic,'r') as dic:
        dicvar=json.load(dic)
else:
    dicvar={"lolcn":["pedophile", "lolicon"]}



vowel=overarchinglanguage.encodedvowel

def generate_shortcut(word):
    global dicvar
    vowc=0
    ret=""
    print(word)
    word=overarchinglanguage.encodingfromoriginal(word)
    print(word)
    for i in word:
        if i in vowel and vowc!=1:
            ret+=i
            vowc+=1
        elif i not in vowel:
            ret+=i
    try:
        dicvar[ret]+=[word]
    except:
        dicvar[ret]=[word]

with open(in_, 'r') as f:
    words = [line.strip() for line in f if line.strip()]

for i in words:
    generate_shortcut(i)

with open(out, 'w',) as f:
    json.dump(dicvar, f)
    


