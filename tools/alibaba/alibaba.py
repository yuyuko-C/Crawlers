import re
import json
from urllib import parse
from http.cookiejar import MozillaCookieJar, Cookie

from peewee import *
from scrapy import Selector

from workpackage.mysql.wedo_basic import Base_Model

from core.api import Net, JsonDict
from .login_cookies import cookies_json


class Company(Base_Model):
    name = CharField()
    main_page = TextField()
    contact_page = TextField()
    addresss = TextField()
    contacter = CharField()
    telephone = CharField()
    mobile_phone = CharField()


Company.instance()
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}


class Ali(Net):
    def __init__(self, cookies_json: str, **requests_kwargs):
        cookies = self.__make_cookies(cookies_json)
        super().__init__(cookies=cookies, **requests_kwargs)

    def __make_cookies(self, cookies_json):
        cookie_jar = MozillaCookieJar()
        cookies_info = json.loads(cookies_json)
        for c in cookies_info:
            cookie_jar.set_cookie(
                Cookie(version=0,
                       name=c['name'],
                       value=c['value'],
                       port=None,
                       port_specified=False,
                       domain=c['domain'],
                       domain_specified=False,
                       domain_initial_dot=False,
                       path=c['path'],
                       path_specified=True,
                       secure=c['secure'],
                       expires=None,
                       discard=True,
                       comment=None,
                       comment_url=None,
                       rest={'HttpOnly': c['httpOnly']},
                       rfc2109=False))
        return cookie_jar

    def serach_company(self, keyword: str, indexarea="company_en"):
        keyword = keyword.strip().replace(" ", "+")
        url = (
            'https://www.alibaba.com/trade/search?fsb=y&IndexArea={}&CatId=&SearchText={}'
            .format(indexarea, keyword))
        res = self.requests_call("GET", url)
        return self.unquote(res.text)

    def company_contact_page_urls(self, keyword: str, indexarea="company_en"):
        html = self.serach_company(keyword, indexarea)
        sel = Selector(text=html)
        parse_format = '//h2[@class="title ellipsis"]//a[@target="_blank"]//@href'
        domains = sel.xpath(parse_format)
        contact_urls = []
        for main in domains:
            url = main.extract()
            url = url.replace('company_profile.html#top-nav-bar', '')
            url = parse.urljoin(url, '/contactinfo.html')
            contact_urls.append(url)
        return contact_urls

    def __get_company_info(self, html: str):
        info = JsonDict()
        sel = Selector(text=html)
        parse_format = '//div[@class="icbu-mod-wrapper with-border company-contact"]//table[@class="contact-table"]/tr[@class="info-item"]'
        table = sel.xpath(parse_format)
        for row in table:
            key_format = './th[@class="item-title"]/span[@class="title-text"]/text()'
            value_format = './td[@class="item-value"]/text()'
            key = row.xpath(key_format).extract_first()
            value = row.xpath(value_format).extract_first()
            info[key] = value
        return info

    def __get_encrypt_account_id(self, html: str):
        match = re.compile(r'"encryptAccountId":"(.+?)"').findall(html)
        if match:
            return match[0]

    def __get_ctoken(self):
        for i in self.requests_kwargs["cookies"]:
            if i.name == "xman_us_t":
                if "ctoken" in i.value:
                    for p in i.value.split("&"):
                        if "ctoken" in p:
                            return p.strip("ctoken=")

    def __get_tel_info(self, info_url: str, html: str):
        en_id = self.__get_encrypt_account_id(html)
        ctoken = self.__get_ctoken()
        # info_url = "https://leilicn.en.alibaba.com/event/app/contactPerson/showContactInfo.htm"
        params = {
            "encryptAccountId": en_id,
            "ctoken": ctoken,
        }
        res = self.requests_call("GET", info_url, params=params)
        return self.parse_json(res.text)

    def contact_page(self, url: str):
        res = self.requests_call("GET", url)
        return self.unquote(res.text)

    def contact_info(self, contact_api: str):

        html = self.contact_page(contact_api)

        url_info = parse.urlparse(contact_api)
        contact_api = parse.urlunparse(
            (url_info.scheme, url_info.netloc,
             "/event/app/contactPerson/showContactInfo.htm", "", "", ""))

        tel = self.__get_tel_info(contact_api, html).contactInfo
        info = self.__get_company_info(html)
        tel.update(info)
        print(tel)

        return tel


if __name__ == "__main__":
    api = Ali(cookies_json, headers=headers)

    contact_urls = api.company_contact_page_urls("electric bicycle")

    for url in contact_urls:
        res = api.contact_info(url)
