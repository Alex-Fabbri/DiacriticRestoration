# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 13:44:49 2016

@author: alexfabbri
"""



import unicodedata
import pickle
import random
import math
from nltk.tokenize import word_tokenize
from sklearn.cross_validation import train_test_split
import numpy as np
from random import sample

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
            noAccentsArr.append(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n'))
            if count % 10 == 0:
                testAccents.append(line.strip('\n'))
                testNoAccents.append(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n'))
            else:
                trainAccents.append(line.strip('\n'))
                trainNoAccents.append(u"".join([char for char in nfkdTransform if not unicodedata.combining(char)]).strip('\n'))
            
            count +=1
    return [trainAccents,trainNoAccents, testAccents, testNoAccents]
    
[trainAccents,trainNoAccents, testAccents, testNoAccents] =     removeAccents('europarl-v7.fr-en.fr')
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


dictTrain = {}
for sentence in train:
    print(sentence)
    '''tokens = word_tokenize(sentence)
    print(tokens)'''
    '''for token in tokens:
        print(token)'''
        '''if token in dictTrain.keys:
            tokens[token] +=1
        else:
            tokens[token] = 1'''
            
'''  
from nltk.tokenize import wordpunct_tokenize
print(wordpunct_tokenize(sentence))
'''
        