from datetime import date
from PIL import Image

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph,SimpleDocTemplate,PageTemplate
from reportlab.lib import  colors
from reportlab.pdfgen import canvas
from reportlab.pdfgen.textobject import PDFTextObject
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



class PdfMaker:
    pdfmetrics.registerFont(TTFont('Arial','C:\\Windows\\Fonts\\arial.ttf' ))
    pdfmetrics.registerFont(TTFont('Tahoma','C:\\Windows\\Fonts\\tahoma.ttf' ))
    pdfmetrics.registerFont(TTFont('Tahomabd','C:\\Windows\\Fonts\\tahomabd.ttf' ))


    def __init__(self, path:str) -> None:
        self.file = canvas.Canvas(path)
        self.left_margin = 43
        self.now_y = self.file._pagesize[1]
        self.x = self.file._pagesize[0]


    def draw_text(self, x:float, y:float, text:str, font_name:str, font_size:float):
        self.file.setFont(font_name,font_size)
        self.file.drawString(x,y,text)


    def draw_item(self, title:str, text:str):
        font_name, font_size='Tahomabd', 8.35
        self.now_y -= (font_size + 11)
        self.draw_text(self.left_margin, self.now_y, title, font_name, font_size)

        font_name, font_size='Tahoma', 8.35
        self.now_y -= (font_size + 6)
        text_split = text.split('\n')
        for i,text in enumerate(text_split):
            self.draw_text(self.left_margin, self.now_y, text, font_name, font_size)
            if len(text_split)>1 and i <len(text_split)-1:
                self.now_y -= (font_size + 1)


    def draw_head(self):
        font_name,font_size='Arial',8
        today = date.today()
        today_str='{}/{}/{}'.format(today.year,today.month,today.day)
        self.now_y -= (font_size + 13)
        self.draw_text(25, self.now_y, today_str, font_name, font_size)
        self.file.drawCentredString(self.x/2, self.now_y, 'Tracking | UPS - Canada')
        self.draw_text(self.x-38, 18, '1/1', font_name, font_size)


    def draw_title(self):
        font_name,font_size='Tahoma',19.1
        self.now_y -= (font_size + 16)
        self.draw_text(self.left_margin, self.now_y, 'Proof of Delivery', font_name, font_size)


    def draw_inform(self):
        font_name,font_size='Tahoma', 8.35
        self.now_y -= (font_size + 23)
        self.draw_text(self.left_margin, self.now_y, 'Dear Customer,', font_name, font_size)
        self.now_y -= (font_size + 7)
        self.draw_text(self.left_margin, self.now_y, 'This notice serves as proof of delivery for the shipment listed below.', font_name, font_size)


    def __analyze_toaddress(self, info:dict):
        shipToAddress=info['shipToAddress']
        lst=[shipToAddress['companyName'],shipToAddress['attentionName']]
        name = '\n'.join([item for item in lst if item])
        lst=[shipToAddress['streetAddress1'],shipToAddress['streetAddress2'],shipToAddress['streetAddress3']]
        address= '\n'.join([item for item in lst if item])
        lst=[shipToAddress['city'],shipToAddress['state'],shipToAddress['province'],shipToAddress['zipCode'],shipToAddress['country']]
        other = ', '.join([item for item in lst if item])
        return '\n'.join(item for item in [name,address,other] if item)


    def draw_end(self, info:dict):
        font_name,font_size='Tahoma', 8.35
        self.now_y -= (font_size + 11)
        text='Thank you for giving us this opportunity to serve you. Details are only available for shipments delivered within the last 120 days. Please'
        self.draw_text(self.left_margin,self.now_y,text,font_name,font_size)
        self.now_y -= (font_size + 1)
        text='print for your records if you require this information after 120 days.'
        self.draw_text(self.left_margin,self.now_y,text,font_name,font_size)
        self.now_y -= (font_size + 8)
        text='Sincerely,'
        self.draw_text(self.left_margin,self.now_y,text,font_name,font_size)
        self.now_y -= (font_size + 8)
        text='UPS'
        self.draw_text(self.left_margin,self.now_y,text,font_name,font_size)
        self.now_y -= (font_size + 8)
        text='Tracking results provided by UPS:'+info['trackedDateTime']
        self.draw_text(self.left_margin,self.now_y,text,font_name,font_size)


    def draw_worker(self,info:dict):
        self.draw_head()
        self.draw_title()
        self.draw_inform()
        
        self.draw_item('Tracking Number', info['trackingNumber'])
        self.draw_item('Weight', info['weight']+' '+info['weightUnit'])
        self.draw_item('Service', info['service']['serviceName'].replace('&#174;','®'))
        self.draw_item('Shipped / Billed On', info['shippedOrBilledDate'])
        self.draw_item('Additional Information', 'Signature Required')
        self.draw_item('Delivered On', info['deliveredDate']+' '+info['deliveredTime'])
        self.draw_item('Delivered To', self.__analyze_toaddress(info))
        self.draw_item('Received By', info['receivedBy'])
        self.now_y -= 44
        self.file.drawImage(info['img'], self.left_margin, self.now_y, 120, 40)
        self.draw_item('Left At', info['leftAt'])
        self.draw_item('Reference Number(s):', info['referenceNumbers'][0])

        self.draw_end(info)

    def save(self):
        self.file.save()