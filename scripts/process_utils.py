from xml.etree.ElementTree import parse
import re

def preprocess_news(sentence):
    # 
    sentence = re.sub(r"\b[A-Z][a-z]*\s[A-Z][a-z]*\b,? (reporter|correspondent)", "", sentence)
    sentence = re.sub(r"All rights reserved.", "", sentence)
    sentence = re.sub(r"[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "", sentence)  # Email removal
    sentence = re.sub(r"\([^)]*\)", "", sentence)  # Remove text in parentheses
    sentence = sentence.replace(",", "")

    return sentence

def read_text_from_xml(xml_dir: str):
    try:
        tree = parse(xml_dir)
        root = tree.getroot()
        text = " ".join([x.text for x in root.findall("text")[0].findall("p")])
        return text
    except Exception as e:
        return ''

def process_c4(text):
    splitted_text = text.split("\n")
    
    # Example checks for English text
    copyright_marks = ["Copyright", "©"]
    not_essential = ["Privacy Policy", "Terms of Service"]
    
    for i, t in enumerate(splitted_text):
        if any(mark in t for mark in copyright_marks) or any(ne in t for ne in not_essential):
            splitted_text[i] = ''  # Replace unwanted sections with empty string

    # Further processing as needed...

    return ' '.join(splitted_text)

# Example usage
text = read_text_from_xml("path_to_your_xml_file.xml")
#again you can use the trian tokinzer ig no use the above line of code
processed_text = preprocess_news(text)
