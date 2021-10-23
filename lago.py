from core.api import Net


class Lago(Net):
    def __init__(self, **requests_kwargs):
        super().__init__(**requests_kwargs)
        res = self.requests_call(
            "GET",
            "https://www.lagou.com/gongsi/v1/j/69d8b84392d928ed2202d586a3e843999974728eeb9799d6.html"
        )
        print(res.cookies)

    def searchPosition(self, companyId: int, page: int, type="全部"):
        url = "https://www.lagou.com/gongsi/searchPosition.json"
        data = {
            "companyId": companyId,
            "positionFirstType": type,
            "city": "",
            "salary": "",
            "workYear": "",
            "schoolJob": False,
            "pageNo": page,
            "pageSize": 10,
        }
        res = self.requests_call('POST', url, data=data)
        print(res.text)

        # return self.parse_json(res.text)


headers = {
    "accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":
    "gzip, deflate, br",
    "accept-language":
    "zh-CN,zh;q=0.9",
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
}

a = Lago(headers=headers)
res = a.searchPosition(7872, 1)
print(res)