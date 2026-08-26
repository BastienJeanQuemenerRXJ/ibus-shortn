class language:
    def __init__(self, originalalphabet, originalalphabetlowercasetouppercase, originalalphabetuppercasetolowercase, encodingfromoriginal, decodingtooriginal, encodedvowel, punctuation, dictionaryname, wordseparator):
        #list of what the user types and it's recognized. 
        self.originalalphabet = originalalphabet
        #converts originalalphabet from lowercase to uppercase
        self.originalalphabetlowercasetouppercase = originalalphabetlowercasetouppercase
        self.originalalphabetuppercasetolowercase = originalalphabetuppercasetolowercase
        #from original (ie éducation) to encoded (ie Mducation)
        self.encodingfromoriginal = encodingfromoriginal
        #reverse
        self.decodingtooriginal = decodingtooriginal
        #vowel list in encoded latin set (ie a,e,i,y, M)
        self.encodedvowel = encodedvowel
        #punctuation at the end, like "Éducation,"
        self.punctuation = punctuation
        #name of the dictionary, called by the engine. named like en.json, ru.json, etc
        self.dictionaryname = dictionaryname
        #like punctuation but pressing it instantly commits without selection
        self.wordseparator=wordseparator
    #encodes into the injective new latin set
    def encoding(self, the,scheme):
        a=""
        for i in the:
            a+= self.originalalphabetuppercasetolowercase.get(i,i)
        the=a
        a=""
        for i in the:
            a+= scheme.get(i,i)
        return a
    #decodes
    def decoding(self, the, scheme):
        a=""
        for i in the:
            a+= scheme.get(i,i)
        return a
        
def loaddic():
    import json
    with open("fr-config.json",'r') as dic:
        return json.load(dic)
print(loaddic())

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
#english doesnt need a remapping because it doesn't have accents (basic latin)

fr=language(
    {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ö", "ä", "ü", "ï", "ë", "ù", "è", "à", "ç", "ô", "â", "ê", "î", "û", "é", "'"},
    { "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O","p": "P", "q": "Q", "r": "R", "s": "S", "t": "T","u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "'":"'", " ": " ","ö":"Ö","ä":"Ä","ü":"Ü","ï":"Ï","ë":"Ë","ù":"Ù","è":"È","à":"À","ç":"Ç","ô":"Ô","â":"Â","ê":"Ê","î":"Î","û":"Û","é":"É" },
    {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n", "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t","U": "u", "V": "v", "W": "w", "X": "x", "Y": "y","Z": "z", "'": "'", " ": " ", "Ö":"ö","Ä":"ä","Ü":"ü","Ï":"ï","Ë":"ë","Ù":"ù","È":"è","À":"à","Ç":"ç","Ô":"ô","Â":"â","Ê":"ê","Î":"î","Û":"û","É":"é"},
    lambda x : fr.encoding(x, {"ö":"O", "ä":"A", "ü":"U", "ï":"I", "ë":"E", "ù":"Y", "è":"R", "à":"W", "ç":"C", "ô":"K", "â":"S", "ê":"F", "î":"V", "û":"N", "é":"M"}),
    lambda x : fr.decoding(x, {"O":"ö", "A":"ä", "U":"ü", "I":"ï", "E":"ë", "Y":"ù", "R":"è", "W":"à", "C":"ç", "K":"ô", "S":"â", "F":"ê", "V":"î", "N":"û", "M":"é"}),
    {'a', 'e', 'i', 'o', 'u', 'y', "O", "A", "U", "I", "E", "Y", "R", "W", "K", "S", "F", "V", "N", "M"},
    {"?", "!", ".", ";", ","},
    "fr.json",
    {" ", "'", "_", "-"}
    )
#list of language configs. TODO: del all the other unused languages whenever engine switches
langlist={"fr":fr, "en":en}
