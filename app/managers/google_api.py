import requests
import asyncio
import aiohttp
import time

from app.Config.config import google_api_key
from app.utils.constants import UrlEndPoints
from app.utils.helper import split_text_into_chunks
from app.utils.helper2 import get_code


class Google_translator:

    def __init__(self):
        self.api_call_limit = 5000
        self.url = UrlEndPoints.GOOGLE_URL

    #TODO: Can call apis in try/except clause
    def api_call(self, request_data):
        ans = {}
        ans['error'] = 0
        ans['source_language'] = request_data.get('source_language')
        target_language = get_code(request_data.get('target_language'))
        try:
            base_url = "https://translation.googleapis.com/language/translate/v2"
            params = {
                "q": request_data.get('source_text'),
                "target": target_language,
                "key": google_api_key,
            }
            response = requests.post(base_url, params=params)
            print(response)
            if response.status_code==200:
                response = response.json()
                ans['target_text']=response['data']['translations'][0]['translatedText']
            else:
                ans['error'] = 1
                ans['error_message'] = 'Cannot able to translate'
        except Exception as e:
            print("except block")
            ans['error'] = 1
            # ans['error_message'] = 'Cannont able to connect Google API'
            ans['error_message'] = str(e)
        print(ans)
        return ans
    
    async def make_request(self,session, text, target_language):
        '''
        This make async request to the google api
        '''
        params = {
            'key': google_api_key,
            'q': text,
            'target': target_language,
        }
        async with session.get(self.url, params=params) as response:
            data = await response.json()
            return data['data']['translations'][0]['translatedText']
    
    async def async_api_call(self,text,target_language):
        async with aiohttp.ClientSession() as session:
            translated_text = await self.make_request(session, text, target_language)
            return translated_text

    async def translate_file(self,input_file,output_file,target_language):
        ans = {}
        ans['error'] = 0
        st = time.time()
        try: 
            with open(input_file, 'r') as file:
                input_text = file.read()
        except:
            ans['error'] = 1
            ans['error_message'] = 'File doesnot exist'
            return ans
        chunks = split_text_into_chunks(input_text, self.api_call_limit)
        translated_chunks = []
        tasks = []
        target_language = get_code(target_language)
        #loop = asyncio.get_running_loop()
        for chunk in chunks:
            task = self.async_api_call(chunk,target_language)
            tasks.append(task)
        translated_chunks =  await asyncio.gather(*tasks,return_exceptions=True)
        translated_text = " ".join(translated_chunks)
        with open(output_file, 'w') as file:
            file.write(translated_text)
        ans['time_taken'] = time.time() - st
        ans['output_file'] = output_file
        return ans


    