import requests
from app.Config.config import google_api_key
from app.utils.constants import UrlEndPoints
from app.utils.helper2 import get_language

class Finder:

    def __init__(self):
        pass

    def api_call(self, request_data):
        ans = {'error': 0}
        try:
            url = UrlEndPoints.GOOGLE_URL + '/detect'
            params = {
                "q": request_data.get('source_text'),
                "key": google_api_key,
            }
            response = requests.post(url, params=params)
            print(response.json())
            if response.status_code == 200:
                response = response.json()
                ans['detected_language'] = get_language(response.get('data').get('detections')[0][0].get('language'))
                # return ans
            else:
                ans['error'] = 1
                ans['erro_message'] = 'Cannot able detect language'
        except Exception as e:
            ans['error'] = 1
            ans['error_message'] = 'Cannont able to connect with API'
        return ans
