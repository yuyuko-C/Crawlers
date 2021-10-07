import asyncio
import os
import encodings.idna
import aiohttp

from tools.ups.pdfmaker import PdfMaker
from tools.ups.upscrawler import UpsCrawler


async def flow(user_id:str, password:str, trackingNumber:str):
    if not trackingNumber:
        return
    async with aiohttp.ClientSession() as session:
        await UpsCrawler.login(session,user_id,password)
        info = await UpsCrawler.get_trackinginfo(session, trackingNumber)
        info['img'] = await UpsCrawler.get_trackingsignature(session, trackingNumber)
        pdf =  PdfMaker(os.path.join(pdf_folder,'{}.pdf'.format(trackingNumber)))
        pdf.draw_worker(info)
        pdf.save()
        pass


path_str = str(UpsCrawler.tracking_number_path)


if path_str != '.':
    with open(path_str, 'r') as f:
        folder = UpsCrawler.tracking_number_path.parent
        pdf_folder = folder.joinpath('pdf')
        pdf_folder.mkdir(exist_ok=True)
        img_folder = pdf_folder.joinpath('img')
        img_folder.mkdir(exist_ok=True)

        content = f.read().split('\n')
        userId=content[0].replace('userId:','').strip()
        password=content[1].replace('password:','').strip()
        trackings=content[3:]
        # trackings=[trackings[0]]
        
        tasks=[flow(userId,password,tracking.strip()) for tracking in trackings]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

