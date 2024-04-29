
# jieba 介绍
- github地址：https://github.com/fxsjy/jieba/
- “结巴”中文分词：做最好的 Python 中文分词组件
- "Jieba" (Chinese for "to stutter") Chinese text segmentation: built to be the best Python Chinese word segmentation module.

# 特点
1. 支持四种分词模式：
- 精确模式，试图将句子最精确地切开，适合文本分析；
- 全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
- 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
- paddle模式，利用PaddlePaddle深度学习框架，训练序列标注（双向GRU）网络模型实现分词。同时支持词性标注。  
  paddle模式使用需安装 paddlepaddle-tiny，`pip install paddlepaddle-tiny==1.6.1`。  
  目前paddle模式支持jieba v0.40及以上版本。jieba v0.40以下版本，请升级jieba，`pip install jieba --upgrade` 。
  [PaddlePaddle官网](https://www.paddlepaddle.org.cn/)

2. 支持繁体分词
3. 支持自定义词典 
4. MIT 授权协议
5. 代码对 Python 2/3 均兼容



主要功能
=======
1. 分词
--------
* `jieba.cut` 方法接受四个输入参数: 需要分词的字符串；cut_all 参数用来控制是否采用全模式；HMM 参数用来控制是否使用 HMM 模型；use_paddle 参数用来控制是否使用paddle模式下的分词模式，paddle模式采用延迟加载方式，通过enable_paddle接口安装paddlepaddle-tiny，并且import相关代码；
* `jieba.cut_for_search` 方法接受两个参数：需要分词的字符串；是否使用 HMM 模型。该方法适合用于搜索引擎构建倒排索引的分词，粒度比较细
* 待分词的字符串可以是 unicode 或 UTF-8 字符串、GBK 字符串。注意：不建议直接输入 GBK 字符串，可能无法预料地错误解码成 UTF-8
* `jieba.cut` 以及 `jieba.cut_for_search` 返回的结构都是一个可迭代的 generator，可以使用 for 循环来获得分词后得到的每一个词语(unicode)，或者用
* `jieba.lcut` 以及 `jieba.lcut_for_search` 直接返回 list
* `jieba.Tokenizer(dictionary=DEFAULT_DICT)` 新建自定义分词器，可用于同时使用不同词典。`jieba.dt` 为默认分词器，所有全局分词相关函数都是该分词器的映射。

代码示例

```python
# encoding=utf-8
import jieba

jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
strs=["我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学"]
for str in strs:
    seg_list = jieba.cut(str,use_paddle=True) # 使用paddle模式
    print("Paddle Mode: " + '/'.join(list(seg_list)))

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))
```

输出:

    【全模式】: 我/ 来到/ 北京/ 清华/ 清华大学/ 华大/ 大学

    【精确模式】: 我/ 来到/ 北京/ 清华大学

    【新词识别】：他, 来到, 了, 网易, 杭研, 大厦    (此处，“杭研”并没有在词典中，但是也被Viterbi算法识别出来了)

    【搜索引擎模式】： 小明, 硕士, 毕业, 于, 中国, 科学, 学院, 科学院, 中国科学院, 计算, 计算所, 后, 在, 日本, 京都, 大学, 日本京都大学, 深造

2. 添加自定义词典
----------------

### 载入词典

* 开发者可以指定自己自定义的词典，以便包含 jieba 词库里没有的词。虽然 jieba 有新词识别能力，但是自行添加新词可以保证更高的正确率
* 用法： `jieba.load_userdict(file_name)` # file_name 为文件类对象或自定义词典的路径
* 词典格式和 `dict.txt` 一样，一个词占一行；每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒。`file_name` 若为路径或二进制方式打开的文件，则文件必须为 UTF-8 编码。
* 词频省略时使用自动计算的能保证分出该词的词频。

**例如：**

```
创新办 3 i
云计算 5
凱特琳 nz
台中
```

* 更改分词器（默认为 `jieba.dt`）的 `tmp_dir` 和 `cache_file` 属性，可分别指定缓存文件所在的文件夹及其文件名，用于受限的文件系统。

* 范例：

  * 自定义词典：https://github.com/fxsjy/jieba/blob/master/test/userdict.txt

  * 用法示例：https://github.com/fxsjy/jieba/blob/master/test/test_userdict.py


        * 之前： 李小福 / 是 / 创新 / 办 / 主任 / 也 / 是 / 云 / 计算 / 方面 / 的 / 专家 /

        * 加载自定义词库后：　李小福 / 是 / 创新办 / 主任 / 也 / 是 / 云计算 / 方面 / 的 / 专家 /

### 调整词典

* 使用 `add_word(word, freq=None, tag=None)` 和 `del_word(word)` 可在程序中动态修改词典。
* 使用 `suggest_freq(segment, tune=True)` 可调节单个词语的词频，使其能（或不能）被分出来。

* 注意：自动计算的词频在使用 HMM 新词发现功能时可能无效。

代码示例：

```pycon
>>> print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
如果/放到/post/中将/出错/。
>>> jieba.suggest_freq(('中', '将'), True)
494
>>> print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
如果/放到/post/中/将/出错/。
>>> print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
「/台/中/」/正确/应该/不会/被/切开
>>> jieba.suggest_freq('台中', True)
69
>>> print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
「/台中/」/正确/应该/不会/被/切开
```

* "通过用户自定义词典来增强歧义纠错能力" --- https://github.com/fxsjy/jieba/issues/14

3. 关键词提取
-------------
### 基于 TF-IDF 算法的关键词抽取

`import jieba.analyse`

* jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
  * sentence 为待提取的文本
  * topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
  * withWeight 为是否一并返回关键词权重值，默认值为 False
  * allowPOS 仅包括指定词性的词，默认值为空，即不筛选
* jieba.analyse.TFIDF(idf_path=None) 新建 TFIDF 实例，idf_path 为 IDF 频率文件

代码示例 （关键词提取）

https://github.com/fxsjy/jieba/blob/master/test/extract_tags.py

关键词提取所使用逆向文件频率（IDF）文本语料库可以切换成自定义语料库的路径

* 用法： jieba.analyse.set_idf_path(file_name) # file_name为自定义语料库的路径
* 自定义语料库示例：https://github.com/fxsjy/jieba/blob/master/extra_dict/idf.txt.big
* 用法示例：https://github.com/fxsjy/jieba/blob/master/test/extract_tags_idfpath.py

关键词提取所使用停止词（Stop Words）文本语料库可以切换成自定义语料库的路径

* 用法： jieba.analyse.set_stop_words(file_name) # file_name为自定义语料库的路径
* 自定义语料库示例：https://github.com/fxsjy/jieba/blob/master/extra_dict/stop_words.txt
* 用法示例：https://github.com/fxsjy/jieba/blob/master/test/extract_tags_stop_words.py

关键词一并返回关键词权重值示例

* 用法示例：https://github.com/fxsjy/jieba/blob/master/test/extract_tags_with_weight.py

### 基于 TextRank 算法的关键词抽取

* jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')) 直接使用，接口相同，注意默认过滤词性。
* jieba.analyse.TextRank() 新建自定义 TextRank 实例

算法论文： [TextRank: Bringing Order into Texts](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)

#### 基本思想:

1. 将待抽取关键词的文本进行分词
2. 以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图
3. 计算图中节点的PageRank，注意是无向带权图

#### 使用示例:

见 [test/demo.py](https://github.com/fxsjy/jieba/blob/master/test/demo.py)

4. 词性标注
-----------
* `jieba.posseg.POSTokenizer(tokenizer=None)` 新建自定义分词器，`tokenizer` 参数可指定内部使用的 `jieba.Tokenizer` 分词器。`jieba.posseg.dt` 为默认词性标注分词器。
* 标注句子分词后每个词的词性，采用和 ictclas 兼容的标记法。
* 除了jieba默认分词模式，提供paddle模式下的词性标注功能。paddle模式采用延迟加载方式，通过enable_paddle()安装paddlepaddle-tiny，并且import相关代码；
* 用法示例

```pycon
>>> import jieba
>>> import jieba.posseg as pseg
>>> words = pseg.cut("我爱北京天安门") #jieba默认模式
>>> jieba.enable_paddle() #启动paddle模式。 0.40版之后开始支持，早期版本不支持
>>> words = pseg.cut("我爱北京天安门",use_paddle=True) #paddle模式
>>> for word, flag in words:
...    print('%s %s' % (word, flag))
...
我 r
爱 v
北京 ns
天安门 ns
```

paddle模式词性标注对应表如下：

paddle模式词性和专名类别标签集合如下表，其中词性标签 24 个（小写字母），专名类别标签 4 个（大写字母）。

| 标签 | 含义     | 标签 | 含义     | 标签 | 含义     | 标签 | 含义     |
| ---- | -------- | ---- | -------- | ---- | -------- | ---- | -------- |
| n    | 普通名词 | f    | 方位名词 | s    | 处所名词 | t    | 时间     |
| nr   | 人名     | ns   | 地名     | nt   | 机构名   | nw   | 作品名   |
| nz   | 其他专名 | v    | 普通动词 | vd   | 动副词   | vn   | 名动词   |
| a    | 形容词   | ad   | 副形词   | an   | 名形词   | d    | 副词     |
| m    | 数量词   | q    | 量词     | r    | 代词     | p    | 介词     |
| c    | 连词     | u    | 助词     | xc   | 其他虚词 | w    | 标点符号 |
| PER  | 人名     | LOC  | 地名     | ORG  | 机构名   | TIME | 时间     |


5. 并行分词
-----------
* 原理：将目标文本按行分隔后，把各行文本分配到多个 Python 进程并行分词，然后归并结果，从而获得分词速度的可观提升
* 基于 python 自带的 multiprocessing 模块，目前暂不支持 Windows
* 用法：
  * `jieba.enable_parallel(4)` # 开启并行分词模式，参数为并行进程数
  * `jieba.disable_parallel()` # 关闭并行分词模式

* 例子：https://github.com/fxsjy/jieba/blob/master/test/parallel/test_file.py

* 实验结果：在 4 核 3.4GHz Linux 机器上，对金庸全集进行精确分词，获得了 1MB/s 的速度，是单进程版的 3.3 倍。

* **注意**：并行分词仅支持默认分词器 `jieba.dt` 和 `jieba.posseg.dt`。

6. Tokenize：返回词语在原文的起止位置
----------------------------------
* 注意，输入参数只接受 unicode
* 默认模式

```python
result = jieba.tokenize(u'永和服装饰品有限公司')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
```

```
word 永和                start: 0                end:2
word 服装                start: 2                end:4
word 饰品                start: 4                end:6
word 有限公司            start: 6                end:10

```

* 搜索模式

```python
result = jieba.tokenize(u'永和服装饰品有限公司', mode='search')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
```

```
word 永和                start: 0                end:2
word 服装                start: 2                end:4
word 饰品                start: 4                end:6
word 有限                start: 6                end:8
word 公司                start: 8                end:10
word 有限公司            start: 6                end:10
```


# 实战之高频词提取
高频词一般是指文档中出现频率较高且非无用的词语，其一定程度上代表了文档的焦点所在。  
针对单篇文档，可以作为一种关键词来看。对于如新闻这样的多篇文档，可以将其作为热词，发现舆论焦点。  

高频词提取其实就是自然语言处理中的TF（Term Frequency）策略。其主要有以下干扰项：
- 标点符号：一般标点符号无任何价值，需要去除。  
- 停用词：诸如“的”“是”“了”等常用词无任何意义，也需要剔除。  

```python

# 读取文件内容
def get_content(path):
    with open(path, 'r', encoding='gbk', errors='ignore') as f:
        content = ''
        for l in f:
            l = l.strip()
            content += l
        return content

# 获取高频词
def get_TF(words, topK=10):
  tf_dic = {}
  for w in words:
    tf_dic[w] = tf_dic.get(w, 0) + 1
  return sorted(tf_dic.items(), key = lambda x: x[1], reverse=True)[:topK]

# 获取高频词(写法二)
def get_TF2(words, topK=10):
  from collections import Counter
  import string

  # 停用词列表，你可以根据需要自定义
  stop_words = set(["的", "了", "是", "我", "你", "喜欢", "非常", "不错","手机"])

  # 去除标点和停用词，并统计词频
  word_count = Counter()
  for word in words:
    # 去除标点
    word = word.strip(string.punctuation)
    # 去除停用词和长度为1的词
    if word and word not in stop_words and len(word) > 1:
      word_count[word] += 1

  # 取词频最高的前 topK 个词
  top_words = word_count.most_common(topK)
  # tokenized_comments = [{"name": word, "value": count} for word, count in top_words]
  return sorted(top_words, key = lambda x: x[1], reverse=True)[:topK]

# 主函数
def main():
  import glob
  import random
  import jieba

  files = glob.glob('./data/news/C000013/*.txt')  # 文件源
  corpus = [get_content(x) for x in files]

  sample_inx = random.randint(0, len(corpus))
  split_words = list(jieba.cut(corpus[sample_inx]))
  print('样本之一：'+corpus[sample_inx])
  print('样本分词效果：'+'/ '.join(split_words))
  print('样本的topK(10)词：'+str(get_TF(split_words)))
```

