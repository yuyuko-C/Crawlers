import json
import scrapy

from datetime import datetime
from urllib import parse
from core.api import Net
from workpackage.mysql.wedo_basic import Wedo_Customer,Wedo_CustomerSaler,Wedo_Member

class UserSystem_Paser(Net):
    def __init__(self, **requests_kwargs):
        self.domain='http://uc.wedoexpress.com/'
        super().__init__(**requests_kwargs)


    def __getSaler(self,td_text_list:list):
        tmpA=td_text_list[td_text_list.index('运德仓储')+1].replace('未分配','').strip()
        tmpB=td_text_list[td_text_list.index('运德物流')+1].replace('未分配','').strip()
        saler=tmpA or tmpB
        if saler=='李倩':
            saler='李倩c'
        elif saler=='张徐':
            saler='张徐b'
        elif saler=='张涛':
            saler='张涛d'    
        return saler

    def login(self):

        username='huangxinc@sailvan.com'
        password= 'Remilia1'


        login_url='http://uc.wedoexpress.com/index.php?mod=public&act=userLogin'

        post_data={
            'username': username,
            'password': password
        }
        res = self.requests_call('POST',login_url,data=post_data)
        res_json=json.loads(res.text)
        if  res_json['errCode']==200:
            print('登录成功')
            return True
        else:
            print('登录失败')
            return False

    def parse_userinfo(self, url:str):
        res =  self.requests_call('GET',url)
        sel=scrapy.Selector(text=res.text)
        tds = sel.xpath('//table[@class="grey-tbody"]/tbody')


        user_info = {}
        for td in tds:
            td_text_list:list=td.xpath('.//tr//td').xpath('string(.)').extract()
            number,reg_person,reg_company,reg_date=td_text_list[1],td_text_list[2],td_text_list[4],td_text_list[11]
            number,reg_person,reg_company,reg_date=number.strip(),reg_person.strip(),reg_company.strip(),reg_date.strip()
            reg_date=datetime.strptime(reg_date,'%Y-%m-%d%H:%M:%S')
            user_info[number]= {'number':number,'reg_person':reg_person,'reg_company':reg_company,"reg_date":reg_date,"saler":self.__getSaler(td_text_list)}

        next_page=sel.xpath('//a[@class="lastpage"]/@href').extract_first()
        if  next_page:
            next_page=parse.urljoin(self.domain,next_page)
        else:
            next_page=''

        return {'user_info':user_info, 'next_page':next_page}

    def get_user_info(self,page:int):
        url = 'http://uc.wedoexpress.com/index.php?mod=UserInfo&act=index&page={}'.format(page)
        return self.parse_userinfo(url)



def update_userinfo():
    maxnumber = Wedo_Customer.select().order_by(Wedo_Customer.id.desc()).get().number

    us = UserSystem_Paser()
    if us.login():
        user_info = {}
        page = 1
        while maxnumber not in user_info:
            user_info.update(us.get_user_info(page=page)['user_info'])
            page += 1
        range_start = int(maxnumber[2:])+1
        range_end = max([int(number[2:]) for number in user_info])+1
        user_number = ['cn'+'0'*(8-len(str(i)))+str(i)  for i in range(range_start,range_end)]
        user_info = [user_info[number] for number in user_info if number in user_number]
        user_info.sort(key = lambda x: x['number'])
        cs_key = [{'number':user['number'],'saler':user['saler']} for user in user_info]
        for user in user_info:
            del user['saler']
            user['name'] = user['reg_company'] if user['reg_company'] else user['reg_person'] 

        Wedo_Customer.insert_many(user_info).execute()
        cs_key = [{'customer':Wedo_Customer.get(number=user['number']),'saler':Wedo_Member.get(name=user['saler'])} for user in cs_key]
        Wedo_CustomerSaler.insert_many(cs_key).execute()


