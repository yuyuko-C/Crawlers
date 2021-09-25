from core.api import Net
import scrapy
from urllib import parse
import json
import time
import pickle
import pandas as pd
from datetime import date,datetime,timedelta

class Wuliu88(Net):
    def __init__(self, **requests_kwargs):
        self.domain = 'https://www.5688.cn/news/'
        self.page = 1
        super().__init__(**requests_kwargs)


    def get_new_news_list(self):
        url = 'https://www.5688.cn/remotejson/getnews'
        headers = {
        # 'Accept':'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate, br','Accept-Language':'zh-CN,zh;q=0.9',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Host': 'www.5688.cn',
        # 'Origin': 'https://www.5688.cn',
        # 'Referer': 'https://www.5688.cn/news/',
        # 'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-origin',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
        data = {'pagination':str(self.page),'category':''}
        self.page+=1
        res  = self.requests_call('POST',url,headers,data=data)
        return json.loads(res.text)


    def parse_listpage(self, info:dict):
        page = {'news_list':[], 'next_page':''}
        sel = scrapy.Selector(text=info['list'])
        news_list = sel.xpath('//div[@class="news_list"]')
        for item in news_list:
            url = parse.urljoin(self.domain,item.xpath('./div[@class="text"]/h3/a/@href').extract_first())
            title = item.xpath('./div[@class="text"]/h3/a/text()').extract_first()
            tag = item.xpath('./a[@class="category"]/text()').extract_first()
            date_str = item.xpath('./div[@class="text"]/div[@class="meta"]/span[@class="time"]/text()').extract_first()
            page['news_list'].append({'title':title,'url':url,'tag':tag,'date_str':date_str})

        sel = scrapy.Selector(text=info['page'])
        next_page = sel.xpath('//a[contains(text(), "下一页")]/@rel').extract_first()
        if next_page:
            page['next_page'] = parse.urljoin(self.domain , next_page.strip('/'))
        else:
            page['next_page'] = ''
        return page


    def save_listpage(self,path:str='5688_listpage.pickle'):
        begin = time.time()
        title,url,tag,date_str = [],[],[],[]

        res =  self.get_new_news_list()
        list_page = self.parse_listpage(res)
        title.extend([news['title'] for news in list_page['news_list']])
        url.extend([news['url'] for news in list_page['news_list']])
        tag.extend([news['tag'] for news in list_page['news_list']])
        date_str.extend([news['date_str'] for news in list_page['news_list']])
        while list_page['next_page']:
            res =  self.get_new_news_list()
            list_page = self.parse_listpage(res)
            title.extend([news['title'] for news in list_page['news_list']])
            url.extend([news['url'] for news in list_page['news_list']])
            tag.extend([news['tag'] for news in list_page['news_list']])
            date_str.extend([news['date_str'] for news in list_page['news_list']])

        with open(path,'wb') as f:
            df = pd.DataFrame({'title':title,'url':url,'tag':tag,'date_str':date_str})
            pickle.dump(df,f)
            
        print(time.time()-begin)


    def parse_article(self,url:str):
        res = self.requests_call('GET',url)
        sel = scrapy.Selector(text=res.text)
        article = sel.xpath('//div[@class="news_content"]')
        title = article.xpath('./div[@class="art_header"]/h1/text()').extract_first()
        text = article.xpath('string(./div[@class="art_content"])').extract_first()
        return {'title':title,'text':text}


    def save_listpage(self,path:str='5688_article.pickle'):
        begin = time.time()
        title,text = [],[]

        with open('5688_listpage.pickle','rb') as f:
            list_page:pd.DataFrame = pickle.load(f)

        list_page['date'] = list_page['date_str'].apply(lambda x:datetime.strptime(x,'%Y-%m-%d').date())
        knowlege = list_page[list_page['tag'].isin(['出口认证','帮助中心','外贸知识'])]
        # print(knowlege)
        list_page.drop('date_str',axis=1,inplace=True)
        news = list_page[list_page['date']>date.today()-timedelta(days=90)]

        df = knowlege.append(news)
        print('文章条目：',len(df))

        index = 0
        for url in df['url']:
            article = self.parse_article(url)
            index += 1
            print(index,article['title'])
            title.append(article['title'])
            text.append(article['text'])

        with open(path,'wb') as f:
            df = pd.DataFrame({'title':title,'text':text})
            pickle.dump(df,f)

        print(time.time()-begin)
