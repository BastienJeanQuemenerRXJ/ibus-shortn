#this defines how to handle the localization of languages in terms of shortn engine
#yes, it's better to convert every non basic latin unicode character into a basic latin character by using upper case basic latin (ie a:a, é:A) because it massively helps on dictionary size and reduces encodign issues. there's no issue since the base input is converted first into lowercase, then into the injective latin set, engineshortn uses it, gives you a list of suggestions, decode it back into original language(ie encodedfrench to regular french) and then uses appendables (capitalization, punctuation etc)
#so
#you type
#édctn
#turns into
#Mdctn
#shortn looks up Mdctn into the dictionary
#finds that Mdctn has Mducation
#converts Mducation into éducation
#shows you éducation
#if you have caps or something it will only apply caps thing at the end. (ie appendables)
#again. this is actually better. without this, dictionary size rises to astronomical levels (iirc russian dictionary size rises to 80mb instead of, now, 8mb) just make sure your new encoded latin set is injective (no collisions)
#again, even if you wanted to remove it, python3 has problems reading large json files with accents. so it would literally not work. if the language doesn't need this (ie the language already only uses the basic latin alphabet) then just set the encode and decode function as x:x to not break anything, like english does
class language:
    def __init__(self, originalalphabet, originalalphabetlowercasetouppercase, originalalphabetuppercasetolowercase, encodedvowel, punctuation, dictionaryname, wordseparator, encodelist, decodelist):
        #list of what the user types and it's recognized. 
        self.originalalphabet = originalalphabet
        #converts originalalphabet from lowercase to uppercase
        self.originalalphabetlowercasetouppercase = originalalphabetlowercasetouppercase
        self.originalalphabetuppercasetolowercase = originalalphabetuppercasetolowercase
        #vowel list in encoded latin set (ie a,e,i,y, M)
        self.encodedvowel = encodedvowel
        #punctuation at the end, like "Éducation,"
        self.punctuation = punctuation
        #name of the dictionary, called by the engine. named like en.json, ru.json, etc
        self.dictionaryname = dictionaryname
        #like punctuation but pressing it instantly commits without selection
        self.wordseparator=wordseparator
        #encode list    from original (ie éducation) to encoded (ie Mducation)
        self.encodelist=encodelist
        #decode list   reverse
        self.decodelist=decodelist

    #encodes into the injective new latin set
    def encoding(self, the):
        a=""
        for i in the:
            #if it can't find it then use 'i'  (    fyi  thing.get(a,b) returns b if thing.get(a) doesn't exist)
            a+= self.originalalphabetuppercasetolowercase.get(i,i)
        the=a
        a=""
        for i in the:
            a+= self.encodelist.get(i,i)
        return a
    #decodes
    def decoding(self, the):
        a=""
        for i in the:
            a+= self.decodelist.get(i,i)
        return a
    #initializes the language and dictionary based on engine name 'selfname' variable
    def givelanguageanddic(selfname):
        #if engine name is shortn then language is english, if not then it has to be of the form shortnLC, so cut down "shortn" to get LC which is the language code (fr, ru, de,es...)
        #overarchinglanguage is the language that the engine uses, dynamically changes whenever you change engine (shortnes->shortnfr etc). global variable
        #this is how we get the language code
        langcode= "en" if  selfname == "shortn" else selfname[6:]
        #getting the language config and loading it 
        import json
        with open("/usr/lib/python3/dist-packages/ibus_shortn/languagelist/"+langcode+"-config.json", 'r') as a:
            a=json.load(a)
            overarchinglanguage=language(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8])
            del a
        try:
            #obtaining the dictionary list and loading it
            with open("/usr/lib/python3/dist-packages/ibus_shortn/languagelist/"+langcode+".json", 'r') as a:
                dic=json.load(a)
                del a
        except:
            dic="dic not found"
        return overarchinglanguage, dic, langcode
