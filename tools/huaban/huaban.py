import asyncio
from core.api import Net
import requests
import json
from pathlib import Path
import aiohttp
import aiofiles

import re,os


class HuabanBoardCrawler(Net):
    download_count=1

    def __init__(self, boardUrl:str, **requests_kwargs):
        super().__init__(**requests_kwargs)
        self.boardUrl = boardUrl
        self.images = []
        self.pin_count = 0
        if not os.path.exists('./images'):
            os.mkdir('./images')

    def __get_board_info(self):
        html = self.requests_call('GET',self.boardUrl).text
        match=re.search(r'app\.page\["board"\] = (.*);',html)
        if match:
            board_info:dict=json.loads(match.group(1))
            return board_info

    def __load_more(self):
        """ ajax请求 """
        maxNo = str(self.images[-1]['pin_id'])
        url = self.boardUrl + "?ks30ksyv&max=" + maxNo + "&limit=100&wfl=1"
        return self.requests_call('GET',url).text

    def __save_image(self, imageName, content):
        """ 保存图片 """
        with open(imageName, 'wb') as fp:
            fp.write(content)

    def read_all_image(self):
        board_info = self.__get_board_info()
        # 添加画板初始化的图片信息
        self.images.extend(board_info['pins'])
        # 获取画板的采集数（因部分图片隐藏的原因，此数据不准确，仅做参考）
        self.pin_coun = board_info['pin_count']

        # 循环读取画板中所有内容
        ajax_count=1
        while True:
            board_info=self.__get_board_info(self.__load_more())
            print(f'第{ajax_count}次的ajax请求')
            if not board_info['pins']:
                print('ajax请求为空，结束采集')
                break
            else:
                self.images.extend(board_info['pins'])
            ajax_count+=1

        # 为下载做数据准备
        for index,img in enumerate(self.images):
            self.images[index]['url']='https://hbimg.huabanimg.com/'+img['file']['key']+'_fw658/format/webp'
            self.images[index]['suffix']=img["file"]["type"][6:]

    def download(self):
        if not self.images:
            self.read_all_image()

        for img in self.images:
            imageName = os.path.join("./images", str(img["pin_id"]) + "." + img['suffix'])
            content=self.session.get(img['url']).content
            self.__save_image(imageName,content)
            print(f'已下载{self.download_count}')
            self.download_count+=1



class HuanbanBoardCraowler_Async():
    def __init__(self) -> None:
        self.images=[]

    def __get_board_info(self,html:str):
        match=re.search(r'app\.page\["board"\] = (.*);',html)
        if match:
            board_info:dict=json.loads(match.group(1))
            return board_info

    def __get_ajax_url(self, boardUrl:str, maxNo:str):
        """ 刷新页面 """
        # ajax请求url
        return boardUrl + "?ks30ksyv&max=" + maxNo + "&limit=100&wfl=1"

    def __getMaxPinId(self,images:list):
        max_pinid=str(images[-1]['pin_id'])
        return max_pinid

    async def read_all_image(self,boardId:int):
        images=[]
        boardUrl='https://huaban.com/boards/'+str(boardId)+'/'
        async with aiohttp.ClientSession() as session:
            async with session.get(boardUrl) as res:
                #初始化画板
                board_info=self.__get_board_info(await res.text())
                images.extend(board_info['pins'])

                # pin_count=board_info['pin_count']
                # print(f'画板{boardId}共采集{pin_count}')

                #下拉刷新
                ajax_count=1
                while True:
                    async with aiohttp.ClientSession() as session:
                        url=self.__get_ajax_url(boardUrl, self.__getMaxPinId(images))
                        async with session.get(url) as res:
                            print(f'画板{boardId}的第{ajax_count}次的ajax请求')
                            board_info=self.__get_board_info(await res.text())
                            if not board_info['pins']:
                                print(f'画板{boardId}ajax请求为空，结束采集')
                                break
                            else:
                                images.extend(board_info['pins'])
                            ajax_count+=1

                #加入图片的url与后缀名，为下载做准备
                for index,img in enumerate(images):
                    images[index]['url']='https://hbimg.huabanimg.com/'+img['file']['key']+'_fw658/format/webp'
                    images[index]['name']=str(img['pin_id'])+'.'+img["file"]["type"][6:]

                #画板图片集加入类的图片集
                self.images.extend(images)


class FileDownload_Async():

    count=1

    def __init__(self,path:str) -> None:
        pth=Path(path).absolute()
        pth.mkdir(exist_ok=True)
        self.__download_folder=pth

    async def __saveFile(self,fileName:str,bytes_:bytes):
        file_path=str(self.__download_folder.joinpath(fileName))
        async with aiofiles.open(file_path,'wb') as f:
            await f.write(bytes_)

    async def downLoadFile(self,fileInfo:dict):
        url=fileInfo['url']
        name=fileInfo['name']
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as res:
                    await self.__saveFile(name,await res.read())
                    print(f'已下载{self.count}')
                    self.count+=1
            except aiohttp.ClientError:
                await self.downLoadFile(fileInfo)
            except aiohttp.ServerDisconnectedError:
                await self.downLoadFile(fileInfo)
                

if __name__ == '__main__':
    huaban=HuanbanBoardCraowler_Async()
    down = FileDownload_Async('./im')
    
    loop=asyncio.get_event_loop()
    boards=[63605775,71485844,62513781]
    # boards=[62513781]
    tasks=[huaban.read_all_image(boardId) for boardId in boards]
    loop.run_until_complete(asyncio.wait(tasks))
    
    print(len(huaban.images))
    tasks=[down.downLoadFile(img) for img in huaban.images]
    loop.run_until_complete(asyncio.wait(tasks))

    # huaban=HuabanBoardCrawler('https://huaban.com/boards/62513781/')
    # huaban.getImagesInfo()
    # huaban.downloadImage()

