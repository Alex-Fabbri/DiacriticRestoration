# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 13:44:49 2016

@author: alexfabbri
"""



import unicodedata
import pickle
from nltk.tokenize import word_tokenize

def removeAccents(file):
    
    with open(file, 'r',encoding='utf-8') as accents, open (file + ".noaccent", 'w', encoding='utf-8') as noaccents:
        count = 0  
        trainAccents = []
        trainNoAccents = []
        testAccents  = []
        testNoAccents = []

        for line in accents:
            print(count)
            
            
            # Remove accents
            
            nfkdTransform = unicodedata.normalize('NFKD', str(line))
            #noaccents.write(nfkdTransform)
            #print(nfkdTransform)
            '''
            unicodedata documentation: "
            The normal form KD (NFKD) will apply the compatibility decomposition,
            i.e. replace all compatibility characters with their equivalents." 

            '''     
            
            noaccents.write(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]))
            
            '''
            unicodedataa.combining(char) is true when we are referring to diacritic words: the line
             below contains the accents removed
           print(u"".join([c for c in nfkd_form if unicodedata.combining(c)]))
           '''
            #accentsArr.append(line.strip('\n'))
          #  noAccentsArr.append(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n'))
            if count % 10 == 0:
                testAccents.append(line.strip('\n'))
                testNoAccents.append(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n'))
            else:
                trainAccents.append(line.strip('\n'))
                trainNoAccents.append(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n'))
            
            count +=1
    
    pickle.dump(trainAccents, open("trainAccentsFR.p", 'wb'))
    pickle.dump(trainNoAccents, open("trainNoAccentsFR.p", 'wb'))
    pickle.dump(testAccents, open("testAccentsFR.p", 'wb'))
    pickle.dump(testNoAccents, open("testNoAccentsFR.p", 'wb'))
    return [trainAccents,trainNoAccents, testAccents, testNoAccents]
    


def getFrequencyDict(trainAccents, trainNoAccents):

    dictnoAccents = {}
    err = 0
    errList = []
    for i in range(len(trainAccents)):
        
        sentenceAccents = trainAccents[i]
        sentenceNoAccents = trainNoAccents[i]
        
        tokensAccents = word_tokenize(sentenceAccents)
        #print(tokensAccents)
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
        else:
            err +=1
            errList.append(trainAccents[i])
    pickle.dump(dictnoAccents, open("frequenciesFR.p", 'wb'))   
    pickle.dump(errList,open("oddSetences.p", 'wb'))    
    print("DONE")
    return dictnoAccents    
    
[trainAccents,trainNoAccents, testAccents, testNoAccents] =     removeAccents('europarl-v7.fr-en.fr')
dictnoAccents = getFrequencyDict(trainAccents, trainNoAccents)  

punctuation = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
count = 0
correct = 0
for i in range(len(testNoAccents)):
    sentenceAccents = trainAccents[i]
    sentenceNoAccents = trainNoAccents[i]
        
    tokensAccents = word_tokenize(sentenceAccents)
    tokensNoAccents = word_tokenize(sentenceNoAccents)
    
    if len(tokensAccents) == len(tokensNoAccents):
        for j in range(len(tokensAccents)):
            tA = tokensAccents[j]
            tNA = tokensNoAccents[j]
            if tokensNoAccents not in punctuation and not tokensNoAccents.isdigit():
                
                count +=1
                print("HI")
            

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
        