from peewee import *
import requests
from scrapy import Selector
import json
from urllib import parse
from workpackage.mysql.wedo_basic import Base_Model
from collections import defaultdict
import pandas as pd

class Company(Base_Model):
    name = CharField()
    main_page = TextField()
    contact_page = TextField()
    addresss = TextField()
    contacter = CharField()
    telephone = CharField()
    mobile_phone = CharField()

Company.instance()


url = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=company_en&CatId=&SearchText=electric+bicycle'

headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "cookie":"cbc=GCCB11EC17C8CDD82A98E072904D742AC1D21CC00F793CBFAC5; umdata_=G642693075A0DA38B55D95BA80BD4D7CF883CE95FDF0FE2D36C; ali_apache_id=11.250.231.189.1629956957530.453539.3; acs_usuc_t=acs_rt=e3b1416dd9dc4458b5834a0f8806a0c0; cookie2=17696ebaaf6b6f73f9547552e336ac7c; t=be690e4185c2578dc2f0c5f2a546ea0d; _tb_token_=383b7e73dd153; cna=64BxGd65xAECAXccEpVCvR1X; xlly_s=1; _samesite_flag_=true; _csrf_token=1629957396941; c_csrf=996255a2-342a-440e-aee5-b8b702f781f1; _umdata=GD3B8C10EF2DAA9E71BBDB3FD9F7596202ED073; xman_us_f=x_locale=zh_CN&x_l=1&last_popup_time=1629958144005&x_user=CN|Yuyuko|Saigyouji|cnfm|253518143&no_popup_today=n; intl_locale=zh_CN; xman_i=aid=2202260948; sc_g_cfg_f=sc_b_currency=CNY&sc_b_locale=en_US&sc_b_site=CN; atm-whl=-1&0&0&0; atm-x=__ll=-1; ali_apache_tracktmp=W_signed=Y; history=company^236673469$200787106; _hvn_login=4; csg=6531a32b; xman_us_t=ctoken=18a__8y07garp&l_source=alibaba&x_user=gBiqJlWd9dTym0id4fJgb/WqDj5isQNbZtdlNRyhJkY=&x_lid=cn1543202428kjwo&sign=y&need_popup=y; intl_common_forever=jyJLV055nJm3pF26DOBNltrJd1JNTp5fql+ttZGumk5kkOkzKjM3zA==; xman_f=tR3qHp7p4Hnr25wWGkxoWugFVombyQ8XvdzlU5YYbiS/Sa2SjDO6uOzk+jYo8wvC5sbHjw2mZgk5ALoU9BRsRcmCIohxGqowv5uKiuLQGIURI51QlVHN8PrkDqKadL8agvN+o9zFPbIArqL7fLzz8QLmswewZZkV9gGCfS+BsRcfQqzB0xdexP1bnyY+3ceGJpcgTBP6xBSzx8nRw4MBvw+ITujTbBHrZAole6BLNr6KIuQOMMSzE20h73hRyPO1VQopTw57NykbQ8qN/Sw5fMXsTTsppTTBF2KRruDE/X4PvE1Wdc87TupNY3FZm2XSTKbB9A8gbtMFihgmdlKSNMaMMm7HVTeBrK3lnetpQNjUo5xdcs00+YnMjOY+KyiC3UqyXEi2UXOBHmghrLvKTgBEneHQq6IqdQB0jPFp4OU=; _m_h5_tk=8dbf7e8a35078720a4bbae96615dbc8f_1629974839272; _m_h5_tk_enc=bd724e31f368ac2c7babbc0ea5b2dd42; ali_apache_track=ms=|mt=2|mid=cn1543202428kjwo; JSESSIONID=8149161B6D1B07E33579FF89AD7A4051; xman_t=+gFCa1M0qRDNbTHc9oLdOew638m1Mb/S6ddwsQ0sK2b8hclcOLM4sr4w6B5ychxW3hioqQygHSIIqGoT5LZcXztjLbsDoqbzCfbFslbptj8QRFLObDRGauI7GaQSQDNng+MHeWeuAlaYdKvM2+g5YZrKlY5UhNCjHiouVdTtmiDtsrIAxwkv6y1Eai78HDf2pnNs5pf74AD6Tg/n/762/BzbnFl9oE5Mpq/08fuTwRzmmTM3gtVqYzcbFt/nH0srGp88GdwCBx5nAljUMqeoU23gtARetsZzb4mwq6KqrzsJ7ITGJCwyQpbLJBWpPBHLL016LnfWJq30qnOdeMN4/PbQBX/SRQwsEJEiAMFMppoBxaaFGK8ogZcmPHsmlWmtglET7Xy68iZYjUWdy62gLg5S+xKpCh/8HvaJWHsjVlgHleNBoTOYIQDLFU8d4ZxQ9oGr7BS/NNPfwil1RL/9bVzYkoF64vEfK8ROCEKTr96b+BgU0zNWdIXd6bwjoRz2OiG6i2Dci/E4Z0k3IdWG7dMHTpzKUL9lDX3/ssuFaivIIN+NetGE55qAMDs8Dez2zpmGT5q1ykxEwOKj6i9h2f/quoSapgR8kv3eJ+tIvknwwmQsubjfSjbRqAqihS1p0rn9f/mohwM/XIb6tjoVyIv976Eb9sFIWQQhiGnz/9CtaSKNWpgS4TCXMcnttVGnmBaTVgO5yL1Zc9s/IrPx8U9ykCGejEAt6FP9vG/V6+IQ1YXTdaQvoHdL8xmzPya3; tfstk=cagcBO1Ihmrbf9EoAEajgFXe897caVf4hkErzVK24w-gwKmQgsjd4MlFxtwrnVI1.; l=eBMNoncnga8uPB69BO5alurza77TPQRfhdVzaNbMiInca6dFQFtBxNCKqyUkYdtxgtfx2etPVKlOcRHv8cU38xTUnGGUTkwHkxv9-; isg=BJycPNDHEYgpU-VUDeldrTn3bbpOFUA_Gs6zjXafBAdqwTpLniT_zlwzICk55HiX"
}

params={
    'encryptAccountId':'IDX1qYsvguuL7wdu6IVKdDSW7kLchwHBfd8RhvO3l-NOXmerEPSENobYXJAyFlRUOX77',
    'ctoken':'18a__8y07garp',
    }



def parse_search_page(url):

    res = requests.get(url,headers=headers)

    sel = Selector(text=res.text)

    company_info=defaultdict(list)
    company_search = sel.xpath('//h2[@class="title ellipsis"]')
    for com in company_search:
        name = com.xpath('.//a[@target="_blank"]/text()').extract()[0].replace(u'\xa0\xa0','')
        company_info['name'].append(name)
        main = com.xpath('.//a[@target="_blank"]//@href').extract()[0].replace('company_profile.html#top-nav-bar','')  
        company_info['main_url'].append(main)
        contact_url=parse.urljoin(main,'/contactinfo.html')
        company_info['contact_url'].append(contact_url)
        contact_api=main+'event/app/contactPerson/showContactInfo.htm'
        print(main)


    next_page = sel.xpath('//a[@class="next"]//@href').extract()
    if next_page:
        next_page = parse.urljoin (main,next_page[0])
    else:
        next_page = ''

    return pd.DataFrame(company_info),next_page


# ret, next_page=parse_search_page(url)


# contact_api='https://chinakaicheng.en.alibaba.com/event/app/contactPerson/showContactInfo.htm'

# res = requests.get(contact_api,params=params,headers=headers)
# print(res.text)
# exit()


# for i in range(4):
#     print(i)
#     companys, next_page=parse_search_page(next_page)
#     ret = ret.append(companys,True)
# print(ret)



cookie1="cbc=GCCB11EC17C8CDD82A98E072904D742AC1D21CC00F793CBFAC5; umdata_=G642693075A0DA38B55D95BA80BD4D7CF883CE95FDF0FE2D36C; ali_apache_id=11.250.231.189.1629956957530.453539.3; acs_usuc_t=acs_rt=e3b1416dd9dc4458b5834a0f8806a0c0; cookie2=17696ebaaf6b6f73f9547552e336ac7c; t=be690e4185c2578dc2f0c5f2a546ea0d; _tb_token_=383b7e73dd153; cna=64BxGd65xAECAXccEpVCvR1X; xlly_s=1; _samesite_flag_=true; _csrf_token=1629957396941; xman_us_f=x_locale=zh_CN&x_l=1&last_popup_time=1629958144005&x_user=CN|Yuyuko|Saigyouji|cnfm|253518143&no_popup_today=n; intl_locale=zh_CN; xman_i=aid=2202260948; sc_g_cfg_f=sc_b_currency=CNY&sc_b_locale=en_US&sc_b_site=CN; atm-whl=-1&0&0&0; atm-x=__ll=-1; ali_apache_tracktmp=W_signed=Y; history=company^236673469$200787106; _hvn_login=4; csg=6531a32b; xman_us_t=ctoken=18a__8y07garp&l_source=alibaba&x_user=gBiqJlWd9dTym0id4fJgb/WqDj5isQNbZtdlNRyhJkY=&x_lid=cn1543202428kjwo&sign=y&need_popup=y; intl_common_forever=jyJLV055nJm3pF26DOBNltrJd1JNTp5fql+ttZGumk5kkOkzKjM3zA==; xman_f=tR3qHp7p4Hnr25wWGkxoWugFVombyQ8XvdzlU5YYbiS/Sa2SjDO6uOzk+jYo8wvC5sbHjw2mZgk5ALoU9BRsRcmCIohxGqowv5uKiuLQGIURI51QlVHN8PrkDqKadL8agvN+o9zFPbIArqL7fLzz8QLmswewZZkV9gGCfS+BsRcfQqzB0xdexP1bnyY+3ceGJpcgTBP6xBSzx8nRw4MBvw+ITujTbBHrZAole6BLNr6KIuQOMMSzE20h73hRyPO1VQopTw57NykbQ8qN/Sw5fMXsTTsppTTBF2KRruDE/X4PvE1Wdc87TupNY3FZm2XSTKbB9A8gbtMFihgmdlKSNMaMMm7HVTeBrK3lnetpQNjUo5xdcs00+YnMjOY+KyiC3UqyXEi2UXOBHmghrLvKTgBEneHQq6IqdQB0jPFp4OU=; _m_h5_tk=8dbf7e8a35078720a4bbae96615dbc8f_1629974839272; _m_h5_tk_enc=bd724e31f368ac2c7babbc0ea5b2dd42; ali_apache_track=mt=2|mid=cn1543202428kjwo; xman_t=NxXEF8jE55lh1sOFnkPvbt7gIrGEXUDTLrWrOUhBLzPJRISeOZYx4f9z7iL+41Vc6oWj8nW6t7CyOif62uNmtjkFqHU9vty3gG/J53YUZaCzWpn+j+KsQ6t0+c9V2BTr/vgNxXdIcOeHJms1EQ+imAmfZMlBn0le3DpEc+IRWGf873/b+MVD60PUU6GfEv2ArS9h/n8UQ+VReTLgdg4Z50gpXu/ycmFY6qI4uj8qqXfJm9HbBWQkl/WYlcO5cDXNpfeNUSEHwo6ZbhcITlM54VtTQ0H6je5f77hQ8jo9xyN0l0SzfEtMLC8PS2hvik9EMNimN78lCL4EOnqhFhB+fAyKMuR/hXGV5AQ9cIdr9PaPDcDQsKIIUo5HZTqjgqiyWCyHKR0lQr/ZkVezic40XTSCfQfd/SeyPeZ74lGZs0zfcmY3d29FUin8Aasp+QSRpZ1ivvCk9573pscDRxFVwlQKEVo6gKBIlvJKn+54AXFpTz90WEBGRtPqZ4Hh227hK3FsoXueEm+pO9/lxFy7DzrR1t6/pLGeEVKLW1ONlzC0OfLQizColWQtHUmeiYJ35st978n7kAVeb8hcU5GymznNtxpy7KIFI//CrIep2Hvxjamp3t9qTSjpGsdtH3rea4yNl93Lb4rhWyl8aL9G/kaZPpFrm365KHkeq5LaMQhsYyQoLHFXgVjKlRbtV3X7Y2VhpM+G5rbhKCI6zstQ8KRA7R+eTLJgyZ6miqlbB+kJ6q2a3aKUEZcYRU9zFy0W; isg=BOzsPM9hoZghV7Wk3XmtXckHvcoepZBPSj5DnUYt-Bc6UYxbbrVg3-LgcBlpCcin; l=eBMNoncnga8uPr6JBOfwlurza77OSIRxHuPzaNbMiOCPOxCw5ILdW6nuwnYeC3hVh6m6R3SW3fIbBeYBqQd-nxv9kloV96Hmn; tfstk=cb3GBbfSCcr_t6EnVFas_EfCMtuGaZ5aCuEE8qKNtrE0w9u8_sjRYglPqOwEIqIf."
cookie2="cbc=GCCB11EC17C8CDD82A98E072904D742AC1D21CC00F793CBFAC5; umdata_=G642693075A0DA38B55D95BA80BD4D7CF883CE95FDF0FE2D36C; ali_apache_id=11.250.231.189.1629956957530.453539.3; acs_usuc_t=acs_rt=e3b1416dd9dc4458b5834a0f8806a0c0; cookie2=17696ebaaf6b6f73f9547552e336ac7c; t=be690e4185c2578dc2f0c5f2a546ea0d; _tb_token_=383b7e73dd153; cna=64BxGd65xAECAXccEpVCvR1X; xlly_s=1; _samesite_flag_=true; _csrf_token=1629957396941; xman_us_f=x_locale=zh_CN&x_l=1&last_popup_time=1629958144005&x_user=CN|Yuyuko|Saigyouji|cnfm|253518143&no_popup_today=n; intl_locale=zh_CN; xman_i=aid=2202260948; sc_g_cfg_f=sc_b_currency=CNY&sc_b_locale=en_US&sc_b_site=CN; atm-whl=-1&0&0&0; atm-x=__ll=-1; ali_apache_tracktmp=W_signed=Y; history=company^236673469$200787106; _hvn_login=4; csg=6531a32b; xman_us_t=ctoken=18a__8y07garp&l_source=alibaba&x_user=gBiqJlWd9dTym0id4fJgb/WqDj5isQNbZtdlNRyhJkY=&x_lid=cn1543202428kjwo&sign=y&need_popup=y; intl_common_forever=jyJLV055nJm3pF26DOBNltrJd1JNTp5fql+ttZGumk5kkOkzKjM3zA==; xman_f=tR3qHp7p4Hnr25wWGkxoWugFVombyQ8XvdzlU5YYbiS/Sa2SjDO6uOzk+jYo8wvC5sbHjw2mZgk5ALoU9BRsRcmCIohxGqowv5uKiuLQGIURI51QlVHN8PrkDqKadL8agvN+o9zFPbIArqL7fLzz8QLmswewZZkV9gGCfS+BsRcfQqzB0xdexP1bnyY+3ceGJpcgTBP6xBSzx8nRw4MBvw+ITujTbBHrZAole6BLNr6KIuQOMMSzE20h73hRyPO1VQopTw57NykbQ8qN/Sw5fMXsTTsppTTBF2KRruDE/X4PvE1Wdc87TupNY3FZm2XSTKbB9A8gbtMFihgmdlKSNMaMMm7HVTeBrK3lnetpQNjUo5xdcs00+YnMjOY+KyiC3UqyXEi2UXOBHmghrLvKTgBEneHQq6IqdQB0jPFp4OU=; _m_h5_tk=8dbf7e8a35078720a4bbae96615dbc8f_1629974839272; _m_h5_tk_enc=bd724e31f368ac2c7babbc0ea5b2dd42; ali_apache_track=ms=|mt=2|mid=cn1543202428kjwo; JSESSIONID=8149161B6D1B07E33579FF89AD7A4051; xman_t=+gFCa1M0qRDNbTHc9oLdOew638m1Mb/S6ddwsQ0sK2b8hclcOLM4sr4w6B5ychxW3hioqQygHSIIqGoT5LZcXztjLbsDoqbzCfbFslbptj8QRFLObDRGauI7GaQSQDNng+MHeWeuAlaYdKvM2+g5YZrKlY5UhNCjHiouVdTtmiDtsrIAxwkv6y1Eai78HDf2pnNs5pf74AD6Tg/n/762/BzbnFl9oE5Mpq/08fuTwRzmmTM3gtVqYzcbFt/nH0srGp88GdwCBx5nAljUMqeoU23gtARetsZzb4mwq6KqrzsJ7ITGJCwyQpbLJBWpPBHLL016LnfWJq30qnOdeMN4/PbQBX/SRQwsEJEiAMFMppoBxaaFGK8ogZcmPHsmlWmtglET7Xy68iZYjUWdy62gLg5S+xKpCh/8HvaJWHsjVlgHleNBoTOYIQDLFU8d4ZxQ9oGr7BS/NNPfwil1RL/9bVzYkoF64vEfK8ROCEKTr96b+BgU0zNWdIXd6bwjoRz2OiG6i2Dci/E4Z0k3IdWG7dMHTpzKUL9lDX3/ssuFaivIIN+NetGE55qAMDs8Dez2zpmGT5q1ykxEwOKj6i9h2f/quoSapgR8kv3eJ+tIvknwwmQsubjfSjbRqAqihS1p0rn9f/mohwM/XIb6tjoVyIv976Eb9sFIWQQhiGnz/9CtaSKNWpgS4TCXMcnttVGnmBaTVgO5yL1Zc9s/IrPx8U9ykCGejEAt6FP9vG/V6+IQ1YXTdaQvoHdL8xmzPya3; tfstk=cagcBO1Ihmrbf9EoAEajgFXe897caVf4hkErzVK24w-gwKmQgsjd4MlFxtwrnVI1.; l=eBMNoncnga8uPB69BO5alurza77TPQRfhdVzaNbMiInca6dFQFtBxNCKqyUkYdtxgtfx2etPVKlOcRHv8cU38xTUnGGUTkwHkxv9-; isg=BJycPNDHEYgpU-VUDeldrTn3bbpOFUA_Gs6zjXafBAdqwTpLniT_zlwzICk55HiX"
cookie3="cbc=GCCB11EC17C8CDD82A98E072904D742AC1D21CC00F793CBFAC5; umdata_=G642693075A0DA38B55D95BA80BD4D7CF883CE95FDF0FE2D36C; ali_apache_id=11.250.231.189.1629956957530.453539.3; acs_usuc_t=acs_rt=e3b1416dd9dc4458b5834a0f8806a0c0; cookie2=17696ebaaf6b6f73f9547552e336ac7c; t=be690e4185c2578dc2f0c5f2a546ea0d; _tb_token_=383b7e73dd153; cna=64BxGd65xAECAXccEpVCvR1X; xlly_s=1; _samesite_flag_=true; _csrf_token=1629957396941; xman_us_f=x_locale=zh_CN&x_l=1&last_popup_time=1629958144005&x_user=CN|Yuyuko|Saigyouji|cnfm|253518143&no_popup_today=n; intl_locale=zh_CN; xman_i=aid=2202260948; sc_g_cfg_f=sc_b_currency=CNY&sc_b_locale=en_US&sc_b_site=CN; c_csrf=44c8e9e9-2c19-4f9e-a973-7ba459a100f5; atm-whl=-1&0&0&0; atm-x=__ll=-1; ali_apache_tracktmp=W_signed=Y; history=company^236673469$200787106; _hvn_login=4; csg=6531a32b; xman_us_t=ctoken=18a__8y07garp&l_source=alibaba&x_user=gBiqJlWd9dTym0id4fJgb/WqDj5isQNbZtdlNRyhJkY=&x_lid=cn1543202428kjwo&sign=y&need_popup=y; intl_common_forever=jyJLV055nJm3pF26DOBNltrJd1JNTp5fql+ttZGumk5kkOkzKjM3zA==; xman_f=tR3qHp7p4Hnr25wWGkxoWugFVombyQ8XvdzlU5YYbiS/Sa2SjDO6uOzk+jYo8wvC5sbHjw2mZgk5ALoU9BRsRcmCIohxGqowv5uKiuLQGIURI51QlVHN8PrkDqKadL8agvN+o9zFPbIArqL7fLzz8QLmswewZZkV9gGCfS+BsRcfQqzB0xdexP1bnyY+3ceGJpcgTBP6xBSzx8nRw4MBvw+ITujTbBHrZAole6BLNr6KIuQOMMSzE20h73hRyPO1VQopTw57NykbQ8qN/Sw5fMXsTTsppTTBF2KRruDE/X4PvE1Wdc87TupNY3FZm2XSTKbB9A8gbtMFihgmdlKSNMaMMm7HVTeBrK3lnetpQNjUo5xdcs00+YnMjOY+KyiC3UqyXEi2UXOBHmghrLvKTgBEneHQq6IqdQB0jPFp4OU=; _m_h5_tk=8dbf7e8a35078720a4bbae96615dbc8f_1629974839272; _m_h5_tk_enc=bd724e31f368ac2c7babbc0ea5b2dd42; ali_apache_track=mt=2|mid=cn1543202428kjwo; JSESSIONID=0053937DD7B459DD5D64417AD361BB40; xman_t=NxXEF8jE55lh1sOFnkPvbt7gIrGEXUDTLrWrOUhBLzPJRISeOZYx4f9z7iL+41Vc6oWj8nW6t7CyOif62uNmtjkFqHU9vty3gG/J53YUZaCzWpn+j+KsQ6t0+c9V2BTr/vgNxXdIcOeHJms1EQ+imAmfZMlBn0le3DpEc+IRWGf873/b+MVD60PUU6GfEv2ArS9h/n8UQ+VReTLgdg4Z50gpXu/ycmFY6qI4uj8qqXfJm9HbBWQkl/WYlcO5cDXNpfeNUSEHwo6ZbhcITlM54VtTQ0H6je5f77hQ8jo9xyN0l0SzfEtMLC8PS2hvik9EMNimN78lCL4EOnqhFhB+fAyKMuR/hXGV5AQ9cIdr9PaPDcDQsKIIUo5HZTqjgqiyWCyHKR0lQr/ZkVezic40XTSCfQfd/SeyPeZ74lGZs0zfcmY3d29FUin8Aasp+QSRpZ1ivvCk9573pscDRxFVwlQKEVo6gKBIlvJKn+54AXFpTz90WEBGRtPqZ4Hh227hK3FsoXueEm+pO9/lxFy7DzrR1t6/pLGeEVKLW1ONlzC0OfLQizColWQtHUmeiYJ35st978n7kAVeb8hcU5GymznNtxpy7KIFI//CrIep2Hvxjamp3t9qTSjpGsdtH3rea4yNl93Lb4rhWyl8aL9G/kaZPpFrm365KHkeq5LaMQhsYyQoLHFXgVjKlRbtV3X7Y2VhpM+G5rbhKCI6zstQ8KRA7R+eTLJgyZ6miqlbB+kJ6q2a3aKUEZcYRU9zFy0W; l=eBMNoncnga8uPj_CBO5a-urza77TNIObzxFzaNbMiInca6LfLFd3hNCKq7ZvbdtxgtfbLeKPVKlOcR3p82438jDDBeYC1RiJxxv9-; isg=BCcnGd8kChknXY6VwqA2vO5etlvxrPuOjfeYjPmVarbR6EWqAH1I3zygC-j2UtMG; tfstk=cf2PBBv-HTBrXMMC6YMFFgOxN_Y5a423C_nKZSKyjMylPpcS7sAJJmVenzUEWtcl."


print(cookie1==cookie2)
print(cookie2==cookie3)
print(cookie3==cookie1)