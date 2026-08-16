#list of words to add to dictionary
in_="custom-words.txt"
#preexisting dictionary to add from
supportdic="en-dic.json"
#target dictionary to write as
out="en-dic.json"
import json
if supportdic!=None:
    with open(supportdic,'r') as dic:
        dicvar=json.load(dic)
else:
    dicvar={"lolcn":["pedophile", "lolicon"]}



vowel={'a', 'e', 'i', 'o', 'u', 'y'}

def generate_shortcut(word):
    global dicvar
    vowc=0
    ret=""
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

with open(in_, 'r', encoding="latin-1") as f:
    words = [line.strip() for line in f if line.strip()]

for i in words:
    generate_shortcut(i)

with open(out, 'w',) as f:
    json.dump(dicvar, f)
    


