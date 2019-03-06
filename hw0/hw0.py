#註解part 1
#新頭殼

import sys
import pickle
import requests
from datetime import datetime
from bs4 import BeautifulSoup


# node：節點
# strptime:把字串轉為datetime   #strftime:把datetime轉為str  #所以get_date會產出str
def get_date(news_block_node):
    date_string = news_block_node.find(class_="news_date").string.split('|')[0][2:-1]
    return datetime.strptime(date_string, '%Y.%m.%d').strftime('%Y-%m-%d')


#class_ = ＸＸ是否要看檔案長怎樣（欄位名稱？）
def get_title(news_block_node):
    return news_block_node.find(class_='news_title').a.string


# 取出 HTML 節點中，每個超連結的網址（即屬性為href)
def get_link(news_block_node):
    return news_block_node.find(class_="news_title").a.get('href')


# 取出網站中的新聞內文本體
def get_content(link):
    r = requests.get(link)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')    # 以BS解析HTML程式碼
    #  接下來所有資料的搜尋、萃取等都會透過soup進行
    article_node = soup.find(itemprop='articleBody')   # 元素屬性：內文本體
    article = article_node.get_text()
    return article.replace('\n', "")      # 把換行刪去（不換行）


# 產生字典info分類存取新聞資料
def get_news_info(each_news):
    date = get_date(each_news)
    title = get_title(each_news)
    link = get_link(each_news)
    content = get_content(link)

    info = {'date': date,
            'title': title,
            'link': link,
            'content': content}
    return info


# 產生news（list)存取超連結裡的文字
def get_page_news(page_url):
    r = requests.get(page_url)   # 獲取網頁URL  # r為response對象，可透過r為URL的query str傳遞數據
    r.encoding = "UTF-8"

    soup = BeautifulSoup(r.text, 'html.parser')
    news_blocks = soup.find_all(class_="news-list-item clearfix ")
    # find_all：找出所有特定的HTML標籤節點（超連結）

    news = []
    for each_news in news_blocks:
        try:
            news_info = get_news_info(each_news)
        #             print(get_title(each_news))  # 輸出超連結文字
        except:
            #             print('-------{}-------'.format())
            pass

        news.append(news_info)
    return news


# 產生data(list) 存取新聞內文（即函數get_page_news 傳回的news（list)中的新聞內容）
def get_new_talk_news(from_page=1, end_page=270, url="https://newtalk.tw/news/subcategory/2/政治/"):
    print("page_number from {} to {}".format(from_page, end_page - 1))    # 格式化輸出內容於{}中
    data = []
    for page_number in range(from_page, end_page):   # 跑1~269頁的政治新聞
        print("page_number: {}".format(page_number))
        data = data + get_page_news(url + str(page_number))
        # 組合list  # url + str(page_number):為新聞網址（從1~269頁的）

    print('done')
    return data


sys.setrecursionlimit(100000)    # 設定遞迴的層數（限制 interpreter stack 的 max depth 到 limit)
with open('data/new_talk.pkl', 'wb') as handle:
    pickle.dump(data, handle)   # 利用pickle.dump存取data至handle中（寫入）  # pickle 可壓縮保存字典或清單


