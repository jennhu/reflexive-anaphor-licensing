import re
import nltk
from nltk import word_tokenize

## singular nouns
males = ['boy','brother','father','grandfather','boyfriend','husband','actor','man','son','gentleman','king']
females = ['girl','sister','mother','grandmother','girlfriend','wife','actress','woman','daughter','lady','queen']
count = 0

with open('nouns_count.txt', 'w+') as outputfile:
    with open('train.txt', 'r') as txtfile:
        linelist = [line for line in txtfile.readlines()]
        for male in males:
            count = 0
            for line in linelist:
                if re.search(male, line):
                    count += 1
            print(male, count)
            outputfile.write(male + ' ' + str(count) + '\n')
        for female in females:
            count = 0
            for line in linelist:
                if re.search(female, line):
                    count += 1
            print(female, count)
            outputfile.write(female + ' ' + str(count) + '\n')

## plural nouns
males_pl = ['boys','brothers','fathers','grandfathers','boyfriends','husbands','actors','men','sons','gentlemen','kings']
females_pl = ['girls','sisters','mothers','grandmothers','girlfriends','wives','actresses','women','daughters','ladies','queens']
count = 0

with open('nouns_pl_count.txt', 'w+') as outputfile:
    with open('train.txt', 'r') as txtfile:
        linelist = [line for line in txtfile.readlines()]
        for male in males_pl:
            count = 0
            for line in linelist:
                if re.search(male, line):
                    count += 1
            print(male, count)
            outputfile.write(male + ' ' + str(count) + '\n')
        for female in females_pl:
            count = 0
            for line in linelist:
                if re.search(female, line):
                    count += 1
            print(female, count)
            outputfile.write(female + ' ' + str(count) + '\n')


txtfile.close()
outputfile.close()
