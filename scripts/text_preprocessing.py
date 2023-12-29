import re
import regex
from dataclasses import dataclass

@dataclass
class TextPreprocessing:
    # Replace unneeded Data with mapping marks.
    @staticmethod
    def replace(text):
        replace_mark = {'\\n': "\n", "\\'": "'", "‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": "sqrt", "×": "x", "²": "2",
                        "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e",
                        '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta',
                        '∅': '', '³': '3', 'π': 'pi', '\u200b': '', '…': '.', '\ufeff': ''}

        for mark in replace_mark:
            text = text.replace(mark, replace_mark[mark])

        return text

    @staticmethod
    def sub(text):
        # Remove emails
        email_pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
        text = re.sub(email_pattern, "", text)

        # Remove links
        link_pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        text = re.sub(link_pattern, "", text)

        # Remove special characters
        special_word_pattern = '[#/\:^$@*※~&%ㆍ』\\‘|\(\)\[\]\<\>`…》]'
        text = re.sub(special_word_pattern, "", text)

        # Remove newline characters
        text = re.sub('\n', '', text)

        # Remove consecutive spaces
        text = re.sub(r"\s+", " ", text)

        return text

    @staticmethod
    def preprocess(text):
        text = TextPreprocessing.replace(text)
        text = TextPreprocessing.sub(text)

        return text
