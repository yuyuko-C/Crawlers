from core.api import Net
import requests
import scrapy
from urllib import parse


class Edoc2(Net):

    def __init__(self, host:str, **requests_kwargs):
        super().__init__(**requests_kwargs)
        self.current_path=''
        self.current_id=''
        self.host = host


    def login(self,user_id:str,password:str) -> None:

        login_url=f'{self.host}/ocm/Api/Auth/Login'
        data={
            'account':user_id,
            'password':password
        }
        res = self.requests_call('POST',login_url,data=data)
        if '注销' in res.text:
            print('登录成功')
            self._user_id=user_id
            self._password=password
            self._domain=res.url
        else:
            print('登录失败')


    def createFolder(self, parent_folder:dict, folder_name:str):
        params={'_hrc_':'30'}
        data={
            'jueAction':'postBack',
            'jueUid':'webClient',
            'jueEvt':'CreateFolder',
            'AddFolder_txtFolderName':folder_name,
            'AddFolder_txtParentFolderName':parent_folder['name'],
            'AddFolder_txtParentFolderId':parent_folder['id'],
            'AddFolder_txtFolderRemark':'',
            'AddFolder_txtFolderCode':'',
            }
        self.requests_call('POST',self._domain,params=params,data=data)
        

    def deleteFolder(self,folder_id:str):
        params={'_hrc_':'9'}
        data={
            'jueAction':'postBack',
            'jueUid':'webClient',
            'jueEvt':'DeleteFolderFiles',
            'folders':folder_id,
            'files':'',
            'remark':'',
            }
        self.requests_call('POST',self._domain,params=params,data=data)

