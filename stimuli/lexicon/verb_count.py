import re
import nltk
from nltk import word_tokenize


#verbs = ['disappointed', 'hurt', 'enjoyed']
verbs = ['disappointed', 'hurt', 'enjoyed', 'pleased', 'cleaned', 'taught', 'behaved','amused', 'helped', 'convinced', 'repeated', 'proved', 'confused', 'examined','talked to','hated','killed','cut','dried','introduced','prepared','blamed','expressed','distanced','found','helped','saw','changed','stopped','drove','denied','encouraged','paid','distinguished','committed','suited','explained','dressed','burnt','called','licked','satisfied','chocked','surprised','pushed','relied on','surpassed','forgave','rinsed','washed','loved']
count = 0

with open('verbs_count.txt', 'w+') as outputfile:
    with open('train.txt', 'r') as txtfile:
        linelist = [line for line in txtfile.readlines()]
        for verb in verbs:
            count = 0
            for line in linelist:
                if re.search(verb, line):
                    count += 1
            print(verb, count)
            outputfile.write(verb + ' ' + str(count) + '\n')



txtfile.close()
outputfile.close()
