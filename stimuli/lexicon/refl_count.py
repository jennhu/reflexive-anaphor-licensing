import re
import nltk
from nltk import word_tokenize


refls = ['himself','herself','themselves']
count = 0

with open('refl_count.txt', 'w+') as outputfile:
    with open('train.txt', 'r') as txtfile:
        linelist = [line for line in txtfile.readlines()]
        for refl in refls:
            count = 0
            for line in linelist:
                if re.search(refl, line):
                    count += 1
            print(refl, count)
            outputfile.write(refl + ' ' + str(count) + '\n')


txtfile.close()
outputfile.close()
