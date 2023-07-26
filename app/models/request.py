from app.utils.helper2 import valid_language
from app.managers.find_language import Finder
from app.managers.api_call import Translator


class Request:
    def __init__(self):
        pass

    def request_handeler(self, request_data, api_name):
        ans = {'error': 0}
        source_language = request_data.get("source_language").lower().strip()
        print("google_apit called")

        finder = Finder()
        translated_txt = finder.api_call(request_data)
        if translated_txt['error']:
            return translated_txt
        detected_language = translated_txt['detected_language']

        # Checking if source language is given
        if len(source_language.strip()) > 0:
            # Checking for valid language
            if not valid_language(source_language):
                ans['error'] = 1
                ans["error_message"] = "API does not support {} language as source language".format(source_language)
                return ans
            elif detected_language.lower() != source_language.lower():
                ans['error'] = 1
                ans['error_message'] = 'Detected Language doesnot match with Source Language'
                return ans
        ans['source_language'] = detected_language
        request_data['source_language'] = detected_language
        target_language = request_data.get('target_language').lower().strip()
        ans['target_language'] = target_language
        # checking if target language is valid or not
        if not valid_language(target_language):
            ans['error'] = 1
            ans["error_message"] = "API does not support {} language as target language".format(target_language)

        if ans['error'] == 1:
            return ans

        translator = Translator()
        if api_name == 'google':
            response_ = translator.api_call(request_data, "google")
            return response_

        elif api_name == 'lacto':
            response_ = translator.api_call(request_data, "lacto")
            return response_

        else:
            response_ = translator.api_call(request_data, "rapid")
            return response_



