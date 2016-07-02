# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 13:44:49 2016

@author: alexfabbri
"""



import unicodedata
import pickle
from nltk.tokenize import word_tokenize
punctuation = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
def run(file):   
    [trainAccents,trainNoAccents, testAccents, testNoAccents, dictnoAccents, err, words] =     removeAccents(file)
    #dictnoAccents = getFrequencyDict(trainAccentsFR, trainNoAccentsFR)  
    [incorrect,accuracy, wordCount, nonWordCount] = test(testAccents, testNoAccents, dictnoAccents)



'''
Francais
le nombre de mots dans l'apprentissage: 46842403
le nombre de points de ponctuation et de nombrs dans l'apprentissage: 5347956
Le nombre de mot dans le corpus: 5207310
Le nombre de ponctuation et de nombres dans le corpus: 594551
Nombre au total de changements/non changements possibles 5207310
Nombre au total de decisions correctes 5133026
Accuracy: 0.9857346691477942'''

'''Polonais
le nombre de mots dans l'apprentissage: 11399024
le nombre de points de ponctuation et de nombrs dans l'apprentissage: 1789941
Le nombre de mot dans le corpus: 1264088
Le nombre de ponctuation et de nombres dans le corpus: 197909
Nombre au total de changements/non changements possibles 1264088
Nombre au total de decisions correctes 1239834
Accuracy: 0.9808130446614476'''

def runReady():
    testAccentsFR = pickle.load(open("testAccentsfr.p", 'rb'))
    testNoAccentsFR = pickle.load(open("testNoAccentsfr.p", 'rb'))
    DictFR = pickle.load(open("frequenciesfr.p",'rb'))
    #otherDictFR = makeFreq('fr.txt')
    [incorrect,accuracy, wordCount, nonWordCount] = test(testAccentsFR, testNoAccentsFR, DictFR)
    return accuracy
    
def removeAccents(file):
    
    with open(file, 'r',encoding='utf-8') as accents, open (file + ".noaccent", 'w', encoding='utf-8') as noaccents:
        count = 0  
        trainAccents = []
        trainNoAccents = []
        testAccents  = []
        testNoAccents = []
        dictnoAccents = {}
        
        words = {}
        err = 0
        errList = []
        
        fileExtension = file[-2:]
        wordsCount = 0
        nonWordsCount = 0
        for line in accents:
            
            #print(line)
            '''if count >10:
                break
            
            print(count)'''
           
            
            
            # Remove accents
            
            nfkdTransform = unicodedata.normalize('NFKD', str(line))
            #noaccents.write(nfkdTransform)
            #print(nfkdTransform)
            '''
            unicodedata documentation: "
            The normal form KD (NFKD) will apply the compatibility decomposition,
            i.e. replace all compatibility characters with their equivalents." 

            '''     
            
            noaccents.write(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).replace(u'\xad','-'))
            
            '''
            unicodedataa.combining(char) is true when we are referring to diacritic words: the line
             below contains the accents removed
           print(u"".join([c for c in nfkd_form if unicodedata.combining(c)]))
           '''
         
            if count % 10 == 0:
                #print("TEST")
                testAccents.append(line.replace(u'\xad','-').strip('\n'))
              
                testNoAccents.append(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n').replace(u'\xad','-'))
            
            else:
                #print("HIIIIIII")
                sentenceAccents= line.replace(u'\xad','-').strip('\n')
                sentenceNoAccents = u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n').replace(u'\xad','-')
                
                trainAccents.append(sentenceAccents)                
                trainNoAccents.append(sentenceNoAccents)
                
                tokensAccents = word_tokenize(sentenceAccents)
                tokensNoAccents = word_tokenize(sentenceNoAccents)
                
                if len(tokensAccents) == len(tokensNoAccents):
                    for j in range(len(tokensAccents)):
                        
                        tA = tokensAccents[j]
                        tNA = tokensNoAccents[j]
                        if tNA not in punctuation and not tNA.isdigit():
                            wordsCount +=1
                            if tA not in words.keys():
                                words[tA] =1
                            else:
                                words[tA] +=1
                        else:
                            nonWordsCount +=1
                        if tNA not in dictnoAccents.keys():
                            dictnoAccents[tNA] = {tA:1}
                                #print("HI")
                        else:
                            if tA not in dictnoAccents[tNA].keys():
                                dictnoAccents[tNA][tA] =1
                            else:
                                dictnoAccents[tNA][tA] +=1
                    
                else:
                    err +=1
                    errList.append(sentenceAccents)
                    
            count +=1
    print("le nombre de mots dans l'apprentissage: " + str(wordsCount))
    print("le nombre de points de ponctuation et de nombres dans l'apprentissage: " + str(nonWordsCount))
    trainAccFileName = "trainAccents" + fileExtension + ".p"   
    trainNoAccFileName = "trainNoAccents" + fileExtension + ".p"
    testAccFileName = "testAccents" + fileExtension + ".p"
    testNoAccFileName = "testNoAccents" + fileExtension + ".p"
    dictFileName = "frequencies" + fileExtension + ".p"
    errFileName = "oddSentences" + fileExtension + ".p"
    wordsFileName = "words" + fileExtension + ".p"
    
    pickle.dump(trainAccents, open(trainAccFileName , 'wb'))
    pickle.dump(trainNoAccents, open(trainNoAccFileName, 'wb'))
    pickle.dump(testAccents, open(testAccFileName, 'wb'))
    pickle.dump(testNoAccents, open(testNoAccFileName, 'wb'))
    pickle.dump(dictnoAccents, open(dictFileName, 'wb'))   
    pickle.dump(errList,open(errFileName, 'wb'))
    pickle.dump(words,open(wordsFileName, 'wb'))
    
    return [trainAccents,trainNoAccents, testAccents, testNoAccents, dictnoAccents, err, words]



def getFrequencyDict(trainAccents, trainNoAccents):

    dictnoAccents = {}
    err = 0
    errList = []
    for i in range(len(trainAccents)):
        
        sentenceAccents = trainAccents[i]
        sentenceNoAccents = trainNoAccents[i]
        
        tokensAccents = word_tokenize(sentenceAccents)
        tokensNoAccents = word_tokenize(sentenceNoAccents)
        #print(tokensNoAccents)
        if len(tokensAccents) == len(tokensNoAccents):
            
            for j in range(len(tokensAccents)):
                tA = tokensAccents[j]
                tNA = tokensNoAccents[j]
                #print(tokensAccents[j])
                #print(tokensNoAccents[j])
                
                if tNA not in dictnoAccents.keys():
                    dictnoAccents[tNA] = {tA:1}
                        #print("HI")
                else:
                    if tA not in dictnoAccents[tNA].keys():
                        dictnoAccents[tNA][tA] =1
                    else:
                        dictnoAccents[tNA][tA] +=1  
                '''else:
                    if tNA not in dictnoAccents.keys():
                        dictnoAccents[tNA] = {tNA:1}
                    else:
                        if tA not in dictnoAccents[tNA].keys():
                            dictnoAccents[tNA][tNA] =1
                        else:
                            dictnoAccents[tNA][tNA] +=1  '''
                        #dictnoAccents[tNA] +=1
        else:
            err +=1
            errList.append(trainAccents[i])
        print(i)
    pickle.dump(dictnoAccents, open("frequenciesFR.p", 'wb'))   
    pickle.dump(errList,open("oddSetences.p", 'wb'))    
    print("Fini")
    return dictnoAccents    

def makeFreq(file):
    newDictNoAccents = {}
    with open(file,'r',encoding='utf-8') as largeDictFile:
        for line in largeDictFile:
            line = line.split()
            word = line[0]
            freq = line[1]
            nfkdTransform = unicodedata.normalize('NFKD', str(word))
            noAcc = u"".join([char for char in nfkdTransform if not unicodedata.combining(char)])
            
            if noAcc not in newDictNoAccents.keys():
                newDictNoAccents[noAcc] = {word:freq}
                           
            else:
                print(noAcc)
                newDictNoAccents[noAcc][word] = freq
            '''else:
                if noAcc not in newDictNoAccents.keys():
                    newDictNoAccents[noAcc] = {noAcc:freq}
                else:
                    newDictNoAccents[noAcc][noAcc] = freq'''
    #print("DONE")
    return newDictNoAccents          

def test(testAccents, testNoAccents, dictnoAccents):
    
    count = 0
    correct = 0
    notWord = []
    result = []
    incorrect = {}
    wordCount = 0
    nonWordCount = 0
    for i in range(len(testAccents)):
       
       
        sent = ""
        sentenceAccents = testAccents[i]
        sentenceNoAccents = testNoAccents[i]
            
        tokensAccents = word_tokenize(sentenceAccents)
        tokensNoAccents = word_tokenize(sentenceNoAccents)
        
        if len(tokensAccents) == len(tokensNoAccents):
            for j in range(len(tokensAccents)):
                tA = tokensAccents[j]
                tNA = tokensNoAccents[j]
                if tNA not in punctuation and not tNA.isdigit():
                    wordCount +=1
                    if tNA in dictnoAccents.keys():
                        
                        newToken = max(dictnoAccents[tNA], key=dictnoAccents[tNA].get)
                        #print(newToken)
                        #print("YES")
                    else:
                        newToken = tNA
                    if newToken == tA:
                        correct +=1
                    else:
                        incorrect[newToken] = tA
                       # print(newToken)
                       # print(tA)
                    count +=1
                    
                    #print("HI")
                    if j != 0:
                        newToken = " " + newToken
                else:   
                    
                    nonWordCount  +=1
                   
                    
                    notWord.append(tNA)
                    newToken = tNA
                sent = sent + newToken
       
            result.append(sent)
      
    print("Le nombre de mot dans le corpus: " + str(wordCount) )
    print("Le nombre de ponctuation et de nombres dans le corpus: " + str(nonWordCount))
    print("Nombre au total de changements/non changements possibles " + str(count ))
    print("Nombre au total de decisions correctes " + str(correct))
    print("Accuracy: " + str(correct/count) )
    return([incorrect,correct/count, wordCount, nonWordCount])
    




 

 
 
 
 
 
 
         
'''for token in tokens:
        print(token)'''
'''if token in dictTrain.keys:
            tokens[token] +=1
        else:
            tokens[token] = 1'''
'''    
[accentsArr, noAccentsArr] = removeAccents('europarl-v7.fr-en.fr')
pickle.dump(accentsArr, open("accentsFR.p", 'wb'))
pickle.dump(noAccentsArr,open("noAccentsFR.p", 'wb'))
accentsArr = pickle.load( open( "accentsFR.p", "rb" ) )
noAccentsArr = pickle.load( open( "noAccentsFR.p", "rb" ) )

test = np.array(accentsArr)
'''
#X_train, X_test, y_train, y_test = train_test_split( noAccentsArr, accentsArr, test_size=0.10, random_state=42)
# above was given some weird results with apostrophes in the splits

'''
size = len(accentsArr)
nums = [x for x in range(size)]
random.seed(10)
random.shuffle(nums)
border = math.ceil(size*.9)
trainNums = nums[0:border]
testNums = nums[border:]

trainAccents = []
trainNoAccents = []
testAccents  = []
testNoAccents = []

for num in range(size):
    print(num)
    if num in train:
        trainAccents.append(accentsArr[num])
        trainNoAccents.append(noAccentsArr[num])
    else:
        testAccents.append(accentsArr[num])
        testNoAccents.append(noAccentsArr[num])
'''
'''
size = len(accentsArr)
indices = sample(range(size),math.ceil(size*.9))
noAccentsArr = np.array(noAccentsArr )
accentsArr = np.array(accentsArr)
trainNoAccents = noAccentsArr[indices]
trainAccents = accentsArr[indices]

testNoAccents = np.delete(noAccentsArr,indices)
testAccents = np.delete(accentsArr,indices)
'''

            
'''  
from nltk.tokenize import wordpunct_tokenize
print(wordpunct_tokenize(sentence))
'''
        