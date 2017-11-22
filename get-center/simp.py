from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import *
from nltk.corpus import stopwords

with open(r'E:\Python\NLP\input1.txt') as f:
    text = f.read()

sents = sent_tokenize(text.lower())
tokens = word_tokenize(text.lower())

sw = stopwords.words('english')
puncs = [',', '.', ':', ';', '?', '-', '"', "''", '``', '!']
cleans = [token for token in tokens if ((token not in sw) and (token not in puncs))]

freq = FreqDist(cleans)

weights = [[sent.count(key) if key in sent.split() else 0 for key in freq.keys()]  for sent in sents]
n = len(sents)

d = [(sum([x*x for x in weights[i]])**.5) for i in range(n)]

k = len(freq)
cos = [[sum([(sum([weights[i][m] * weights[j][m] for m in range(k)]))/(d[i]*d[j]) for j in range(n)])/n] for i in range(n)]

targets = [cos.index(sorted(cos,reverse = 1)[i]) for i in range(5)]

with open('output3.txt','w') as f:
    for target in targets:
        f.write(sents[target]+'\n')
