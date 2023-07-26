import requests
import asyncio
import aiohttp
import time
from requests_cache import CachedSession
from app.Config.config import google_api_key, lacto_api_key, rapid_api_key
from app.utils.constants import UrlEndPoints
from app.utils.helper import split_text_into_chunks
from app.utils.helper2 import get_code


class Translator:

    def __init__(self):
        self.api_call_limit = 5000

    def api_call(self, request_data, translate_with):
        response = None
        ans = {'error': 0, 'source_language': request_data.get('source_language')}

        source_language = get_code(request_data.get('source_language'))
        target_language = get_code(request_data.get('target_language'))
        text = request_data.get('source_text')
        try:
            if translate_with == "google":
                params = {
                    "q": text,
                    "target": target_language,
                    "key": google_api_key,
                }
                session = CachedSession(cache_name='cache', allowable_methods=['GET', 'POST'], expire_after=86400)
                response = session.post(UrlEndPoints.GOOGLE_URL, params=params, timeout=5)

            elif translate_with == 'lacto':
                headers = {
                    'X-API-Key': lacto_api_key,
                    'Content-Type': 'json',
                    'Accept': 'json'}
                url = UrlEndPoints.LACTO_URL
                data = {'texts': [text],
                        "to": [target_language],
                        "from": source_language}

                session = CachedSession(cache_name='cache', allowable_methods=['GET', 'POST'], expire_after=86400)
                response = session.post(UrlEndPoints.LACTO_URL, headers=headers, data=json.dumps(data), timeout=5)
            else:
                payload = {
                    "source_language": source_language,
                    "target_language": target_language,
                    "text": request_data.get('source_text')
                }
                headers = {
                    "content-type": "application/x-www-form-urlencoded",
                    "X-RapidAPI-Key": rapid_api_key,
                    "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
                }
                session = CachedSession(cache_name='cache', allowable_methods=['GET', 'POST'], expire_after=86400)
                response = session.post(UrlEndPoints.RAPID_URL, data=payload, headers=headers, timeout=5)

            if response.from_cache:
                print("Data was served from the cache.")
            else:
                print("Data was fetched from the API.")

            if response.status_code == 200:
                response = response.json()
                if translate_with == "google":
                    ans['target_text'] = response['data']['translations'][0]['translatedText']
                elif translate_with == 'lacto':
                    ans['target_text'] = response.get('translations')[0].get('translated')[0]
                else:
                    ans['target_text'] = response.get('data').get('translatedText')
            else:
                ans['error'] = 1
                ans['error_message'] = 'Cannot able to translate'
        except requests.exceptions.Timeout:
            ans['error'] = 1
            ans['error_message'] = 'Timeout'
        except:
            ans['error'] = 1
            ans['error_message'] = 'Cannont able to connect Google API'
        return ans
