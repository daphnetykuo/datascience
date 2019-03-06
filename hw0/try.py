from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import numpy as np
from collections import Counter


text_from_file_with_apath = open(r'mayday_lyrics.txt', "r", encoding = 'utf-8').read()


#設定字典
jieba.set_dictionary('dict.txt.big')
#設定自訂的字典
jieba.load_userdict(r'userdict_Mayday.txt')

#設定停用詞，ex.Oh，喔
with open(r'stopWord.txt', 'r', encoding='utf-8') as f:
    stops = f.read().split('\n')

#開始斷詞與排序
terms = [t for t in jieba.cut(text_from_file_with_apath, cut_all=True) if t not in stops]
sorted(Counter(terms).items(), key=lambda x:x[1], reverse = True)

#文字雲字體
font = r'SignPainter.ttc'
#文字雲圖示
mask = np.array(Image.open(r""))


