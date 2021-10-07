
import aiofiles
import json
from pathlib import Path
from aiohttp.client import ClientSession
from scrapy import Selector
from tkinter.filedialog import askopenfilename



class UpsCrawler:

    IMAGE_WIDTH,IMAGE_HEIGHT = 595, 842
    tracking_number_path = Path(askopenfilename(filetypes=[('TXT','.txt')]))
    # tracking_number_path=Path('E:\\Python_Project\\简单的网页爬虫\\使用模板.txt')

    @classmethod
    async def login(cls, session:ClientSession, user_id:str, password:str):

        login_url = 'https://www.ups.com/lasso/login'

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'origin':'https://www.ups.com',
            'referer':'https://www.ups.com/lasso/login?loc=en_CA&returnto=https%3A%2F%2Fwww.ups.com%2Fca%2Fen%2FHome.page',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9'
        }

        data = {
            'CSRFToken':'',
            'loc':'en_CA',
            'returnto':'https%3A%2F%2Fwww.ups.com%2Ftrack%3Floc%3Dzh_CN%26Requester%3Dlasso',
            # 'forgotpassword':'YZ',
            # 'connectWithSocial':'YZ',
            'userID':user_id,
            'password':password,
            'getTokenWithPassword':'',
        }

        async def get_csrf_token(session:ClientSession):
            headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'referer':'https://www.ups.com/ca/en/Home.page?loc=en_CA',
            }

            params={
                'loc':'en_CA',
                'returnto':'https://www.ups.com/ca/en/Home.page',
            }

            async with session.get(login_url,params=params,headers=headers) as res:
                html = await res.text()
                if 'CSRFToken' in html:
                    sel = Selector(text=html)
                    csrf_token = sel.xpath('//input[@name="CSRFToken"]/@value').extract_first()
                    global cookies
                    cookies =res.cookies
                    return csrf_token
                else:
                    raise ValueError('not found CSRFToken.')
        
        data['CSRFToken'] = await get_csrf_token(session)
        async with session.post(login_url,data=data,headers=headers,cookies=cookies) as res:
            html = await res.text()
            if 'Log In' not in html:
                print('登录成功')

    @classmethod
    async def get_trackinginfo(cls, session:ClientSession, trackingNumber:str):
        print('正在获取跟踪单号：',trackingNumber,'的数据')

        async def get_xsrf_token(session:ClientSession, trackingNumber:str):
            search_url='https://www.ups.com/track?loc=en_CA&tracknum={}&requester=ST/trackdetails'.format(trackingNumber)
            headers = {
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                # 'origin':'https://www.ups.com',
                'referer':'https://www.ups.com/track?loc=en_CA&requester=ST/tracksummary',
                'accept':'application/json, text/plain, */*',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.9',
                'content-type':'application/json',
                # 'x-xsrf-token':cookies['X-XSRF-TOKEN-ST']
            }
            params={
                'loc':'en_CA',
                'tracknum':trackingNumber,
                'requester':'ST/trackdetails'
                }
            async with session.post(url=search_url,headers=headers,params=params) as res:
                global cookies
                cookies = res.cookies
                return cookies['X-XSRF-TOKEN-ST'].value
            # print(res.text)

        prove_url='https://www.ups.com/track/api/Track/GetPOD'

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'origin':'https://www.ups.com',
            'referer':'https://www.ups.com/track?loc=en_CA&tracknum={}&requester=ST/trackdetails'.format(trackingNumber),
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'content-type':'application/json',
            'x-xsrf-token':await get_xsrf_token(session,trackingNumber)
        }

        params={'loc':'en_CA'}
        
        data={
            'ActCode':'D',
            'Locale':'en_CA',
            'TrackingNumber':[trackingNumber]
        }

        async with session.post(url=prove_url,headers=headers,data=json.dumps(data),params=params,cookies=cookies) as res:
            return json.loads(await res.text())

    @classmethod
    async def get_trackingsignature(cls, session:ClientSession, trackingNumber:str):
        url = 'https://wwwapps.ups.com/SignatureClient/SignatureRequest'
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            # 'origin':'https://www.ups.com',
            'referer':'https://www.ups.com',
            'accept':'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'content-type':'application/json',
        }
        params = {
            'Requester':'TrackHTML',
            'tracknum':trackingNumber,
        }
        async with session.get(url,headers=headers,params=params,cookies=cookies) as res:
            file_path = str(cls.tracking_number_path.parent.joinpath('pdf','img',f'{trackingNumber}.jpg'))
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(await res.read())
                return file_path

