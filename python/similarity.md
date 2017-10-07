在做[show-me-the-code 0006](https://github.com/Show-Me-the-Code/show-me-the-code)的时候突然想起大一下学期被程序设计课支配的恐惧，大概内容就是提取[文章](https://github.com/ZTCooper/nlp-get-center/blob/master/python/input1.txt)的中心句，于是现在想用Python来试一下 XD   
  
欢迎大家交流自己的方法和代码！[README](https://github.com/ZTCooper/nlp-get-center)  
  

（主要计算每两句之间的cos值，取平均值最接近1的句子）  
  

### 首先硬碰硬：  
[string.py](https://github.com/ZTCooper/nlp-get-center/blob/master/python/string.py)   
* 读入  
```python
with open('input1.txt') as f:
    text = f.read()
 ```
* 分句  
```python
sents = text.split('. ')        
```
* 转换为小写，去掉一些标点 =\_=  最低级的文本处理方法 [string](https://github.com/ZTCooper/fragmented-py/blob/master/string.md)
```python
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
```
* 用字典存储单词频率
```python
freq = dict()
for word in words:
    if word not in freq:
        freq[word] = 1
    else:
        freq[word] += 1             
```
* 用列表嵌套存储句子权重
```python
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
```
* 计算d值，还是用列表存储
```python
d = []
for i in range(len(weights)):
    d.append((sum([x*x for x in weights[i]])**.5))
```
* 计算平均cos
```python
cos = []
total = 0
for i in range(n):
    for j in range(n):
        k = len(freq)
        total += (sum([weights[i][m] * weights[j][m] for m in range(k)]))/(d[i]*d[j])
    cos.append(total/n)
    total = 0
```
* 取到最大的cos值
```python
targets = []
sort = sorted(cos,reverse = 1)
for i in range(5):
    targets.append(cos.index(sort[i]))
```
* 终于可以输出了
```python
with open('output1.txt','w') as f:
    for target in targets:
        f.write(sents[target]+'\n')
```  
47行代码，所有文本处理都手动来  
最终得到了输出结果：    
[output1.txt](https://github.com/ZTCooper/nlp-get-center/blob/master/python/output1.txt)    
  

然而这一点都不*pythonic*，既然python自带电池，来试一下：  
### 用到`nltk` (Natural Language Toolkit)   
[use-nltk.py](https://github.com/ZTCooper/nlp-get-center/blob/master/python/use-nltk.py)  
首先将文本转换为tokens：  
```python
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

sents = sent_tokenize(text)
tokens = word_tokenize(text)
```
统计频率：  
```python
from nltk.probability import *

freq = FreqDist(tokens)
```
输出看一下:  
```python
for k, v in freq.items():
    print(str(k) + ':' + str(v))
```  
![](https://github.com/ZTCooper/nlp-get-center/blob/master/python/1.png)  
用matplotlib看一下：  
```python
freq.plot(20, cumulative=False)
```
![](https://github.com/ZTCooper/nlp-get-center/blob/master/python/2.png)  
能看到比较高频的基本上都是标点和停用词，来过滤一下： 
```python
from nltk.corpus import stopwords

sw = stopwords.words('english')
puncs = [',', '.', ':', ';', '?', '-', '"', "''", '``', '!']
clean = []

for token in tokens:
    if token not in sw and token not in puncs:
        clean.append(token)
```
这样就差不多了 XD  
![](https://github.com/ZTCooper/nlp-get-center/blob/master/python/3.png)  
然后还是用一样的方法计算cos值  
这样看起来文本预处理简单了一些，但还是有43行代码，几乎所有的数据存储都用到列表，那么就来用
### **列表推导式**简化一下 XD   
[simp.py](https://github.com/ZTCooper/nlp-get-center/blob/master/python/simp.py)
```python
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import *
from nltk.corpus import stopwords

with open(r'E:\Python\NLP\input1.txt') as f:
    text = f.read()

sents = sent_tokenize(text)
tokens = word_tokenize(text.lower())

sw = stopwords.words('english')
puncs = [',', '.', ':', ';', '?', '-', '"', "''", '``', '!']
cleans = [token for token in tokens if (token not in sw) and (token not in puncs)]

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
```
在Sublime中打开是这样的：  
![](https://github.com/ZTCooper/nlp-get-center/blob/master/python/code.png)   
很漂亮吧！
这样只有21行了！不过太复杂的列表推导式会降低代码的可读性，这可能有悖于python之禅([The Zen of Python](https://www.python.org/dev/peps/pep-0020/))  
   
如果是[爬虫](https://github.com/ZTCooper/crawler-scrapy)从网络上抓取下来的html页面，可能还需要先用[beautifulsoup](https://github.com/ZTCooper/fragmented-py/blob/master/beautifulsoup.md)或者[regular-expression](https://github.com/ZTCooper/fragmented-py/tree/master/regular_expression)来处理  
  
（代码可能还存在bug，因为[output2](https://github.com/ZTCooper/nlp-get-center/blob/master/python/output2)和[output3](https://github.com/ZTCooper/nlp-get-center/blob/master/python/output3)的结果不一样 =\_=   
  

欢迎来交流你自己的代码！[README](https://github.com/ZTCooper/nlp-get-center) XD