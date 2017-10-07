#读入
with open('input1.txt') as f:
    text = f.read()

#分句
sents = text.split('. ')

#转换为小写，去掉一些标点 =_=
words = text.lower()
words = words.replace(',','')
words = words.replace('.','')
words = words.replace(';','')
words = words.replace('"','')
words = words.replace(':','')
words = words.replace("''",'')
words = words.replace('-','')
words = words.replace('``','')
words = words.split()

#用字典存储单词频率
freq = dict()
for word in words:
    if word not in freq:
        freq[word] = 1
    else:
        freq[word] += 1

#用列表嵌套存储句子权重
weights = []
n = 0
for sent in sents:
    weights.append([])
    for key in freq.keys():
        if key in sent.split():
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
with open('output1.txt','w') as f:
    for target in targets:
        f.write(sents[target]+'\n')
