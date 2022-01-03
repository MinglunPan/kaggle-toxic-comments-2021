import re
from bs4 import BeautifulSoup
from functools import lru_cache

class TextCleaner:
    def __init__(self, procedure):
        self.action_dict = {
            'remove':TextRemover(),
        }
        self.__procedure_func_list = []

        self.procedure = procedure

    @property
    def procedure(self):
        return self.__procedure
    @procedure.setter
    def procedure(self, procedure):
        self.__procedure_func_list = []
        for action, obj in procedure:
            self.__procedure_func_list.append(self.action_dict[action].get_func(obj))
        return self.__procedure_func_list  
    def clean(self, text):
        for func in self.__procedure_func_list:
            text = func(text)
        return text
    
class TextRemover:
    def __init__(self):
        self.__func_dict = {
            'HTMLTags':self._removeHTMLTags,
            'URL':self._removeURL,
            'Emoji':self._removeEmoji,
            'SpecialCharacters':self._removeSpecialCharacters,
            'ExtraSpaces':self._removeBegingEndSpace,
            'BegingEndSpace':self._removeBegingEndSpace
            }
    def get_func(self, func_name):
        return self.__func_dict[func_name]
    def _removeHTMLTags(self, text):
        soup = BeautifulSoup(text, 'lxml') #Removes HTML tags
        text = soup.get_text()
        return text
    def _removeURL(self, text):
        template = re.compile(r'https?://\S+|www\.\S+') #Removes website links
        text = template.sub(r'', text)
        return text
    def _removeEmoji(self, text):
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        return text
    def _removeSpecialCharacters(self, text):
        text = re.sub(r"[^a-zA-Z\d]", " ", text)
        return text
    def _removeExtraSpaces(self, text):
        text = re.sub(' +', ' ', text) #Remove Extra Spaces
        return text #Remove Extra Spaces
    def _removeBegingEndSpace(self, text):
        return text.strip()