import re
import nltk
from nltk import word_tokenize


refls = ['himself','herself','themselves']
count = 0
refl_sentence = []

with open('refl_sent_count.txt', 'w+') as outputfile:
    with open('train.txt', 'r') as txtfile:
        linelist = [line for line in txtfile.readlines()]
        for refl in refls:
            count = 0
            for line in linelist:
                if re.search(refl, line):
                    #print(line)
                    refl_sentence.append(line) 
                    outputfile.write(line + '\n')

with open('refl_verb_count.txt', 'w+') as outputfile2: 
    refl_verb = []
    for line in refl_sentence:
        tokenized_line = word_tokenize(line)
        for i in range(len(tokenized_line)):
            if tokenized_line[i] == 'himself' or tokenized_line[i] == 'herself' or tokenized_line[i] == 'themselves':
                print(tokenized_line[i-1])
                refl_verb.append(tokenized_line[i-1])
    for verb in refl_verb:
        outputfile2.write(verb + '\n')
            
txtfile.close()
outputfile.close()
outputfile2.close()
