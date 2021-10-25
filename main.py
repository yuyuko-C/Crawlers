headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}

from tools.alibaba.alibaba import Ali
from tools.alibaba.login_cookies import cookies_json

api = Ali(cookies_json, headers=headers)

contact_urls = api.company_contact_page_urls("electric bicycle")

for url in contact_urls:
    res = api.contact_info(url)
    print(res)
