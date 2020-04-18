# -*- coding: utf-8 -*
from requests_html import HTMLSession
import time
import re
import random
import pandas as pd

def get_request(url):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36"
    ]

    header = {
        'User-agent': random.choice(user_agent_list),
    }

    cookie = {
        'cookie': ''
    }

    # time.sleep(random.randint(2, 6))
    return session.get(url, headers=header, timeout=3, cookies=None)


def get_book_info(url):
    # douban_id pool
    try:
        item = get_request(url).json()
        books = item['data']['books']
        # test = pd.read_json(url)
        return books
    except:
        print('get_json_wrong')
        return


if __name__ == "__main__":
    # # 爬虫
    # session = HTMLSession()
    # # 优书网首页Request_url
    # init_url = 'https://www.yousuu.com/api/bookStore/books?page={}&t=1583202757213'
    # # 优书网都市页url
    # lifeStory_url = 'https://www.yousuu.com/api/bookStore/books?classId=6&page={}&t=1586957056841'
    # # 用DataFrame存储数据
    # df = pd.DataFrame()
    # for i in range(1, 20):
    #     print('已读取%d本小说' % (i*20))
    #     books = get_book_info(lifeStory_url.format(i))
    #     df = df.append(books, ignore_index=True)
    # df.to_excel('/Users/wen/百度云同步盘/科技研究/成品项目/优书网爬虫/life_top400_books.xlsx')

    df = pd.read_excel('/Users/wen/百度云同步盘/科技研究/成品项目/优书网爬虫/life_top400_books.xlsx')
    # 过滤掉评分低于7分，太监，评论数小于500的作品
    df1 = df[(df['score'] >= 6.5) & (df['status'] != 2)
             & (df['scorerCount'] >= 400)]
    # 截取更新时间的年份
    df1['updateAt'] = df1['updateAt'].map(lambda x: x[:4])
    # 把2020没更新的伪连载作品找出来
    df1['flag'] = df1.apply(lambda row: (eval(row['updateAt']) < 2020) & (row['status'] == 0), axis=1)
    df1 = df1[df1['flag'] == False]
    # print(df1['flag'])

    writer=pd.ExcelWriter('/Users/wen/百度云同步盘/科技研究/成品项目/优书网爬虫/life_filter_books.xlsx')
    df1.to_excel(writer)
    writer.save()



