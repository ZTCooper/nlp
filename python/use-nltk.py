from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import *
from nltk.corpus import stopwords

with open(r'E:\Python\NLP\input1.txt') as f:
    text = f.read()

#将文本转换为token
sents = sent_tokenize(text)
tokens = word_tokenize(text.lower())

#过滤停用词和标点
sw = stopwords.words('english')
puncs = [',', '.', ':', ';', '?', '-', '"', "''", '``', '!']
cleans = []

for token in tokens:
    if token not in sw and token not in puncs:
        cleans.append(token)

freq = FreqDist(cleans)
#for k, v in freq.items():
#    print(str(k) + ':' + str(v))
#freq.plot(20, cumulative = False)

#用列表嵌套存储句子权重
weights = []
n = 0
for sent in sents:
    weights.append([])
    for key in freq.keys():
        if key in word_tokenize(sent):
            weights[n].append(sent.count(key))
        else:
            weights[n].append(0)
    n += 1

#计算d值，还是用列表存储
d = []
for i in range(n):
    d.append((sum([x*x for x in weights[i]])**.5))

#计算平均cos值
cos = []
total = 0
for i in range(n):
    for j in range(n):
        k = len(freq)
        total += (sum([weights[i][m] * weights[j][m] for m in range(k)]))/(d[i]*d[j])
    cos.append(total/n)
    total = 0

#取到最大的cos值
targets = []
sort = sorted(cos,reverse = 1)
for i in range(5):
    targets.append(cos.index(sort[i]))

#输出
with open('output2.txt','w') as f:
    for target in targets:
        f.write(sents[target]+'\n')
