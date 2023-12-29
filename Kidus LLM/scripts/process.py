import json
import os
import re 
import glob
from multiprocessing import Pool
import tqdm
import gzip
from pathlib import Path
import os
import re
import json
import zipfile
import pandas as pd
import regex

from process_utils import read_text_from_txt, preprocess_news
# add read_text_from_xml  if not using the trian you tokinzer script, which is simplier
from text_preprocessing import TextPreprocessing



cpu_cores = os.cpu_count()
clean_text = lambda x: TextPreprocessing.preprocess(x)

class Preprocess():
    def __init__(self, dataset_folder: Path):
        self.result_dir = Path("../../")
        self.result_dir.parent.mkdir(exist_ok=True)

        self.target_files = glob.glob(str(dataset_folder/"*"))
        self.total_files = len(self.target_files)

    def read(self, file_dir: str):
        return NotImplemented

    def write(self, text):
        mode = "a" if self.result_dir.exists() else "w"
        with open(str(self.result_dir), mode, encoding="utf-8") as f:
            f.write(f"{text}\n")

    def multiprocessing(self):
        pool = Pool(cpu_cores-1)

        print(len(self.target_files))
        with tqdm.tqdm(total=self.total_files) as pbar:
            for _ in tqdm.tqdm(pool.imap_unordered(self.read, self.target_files)):
                pbar.update()

        pool.close()
        pool.join()

    def normal(self):
        for file_dir in self.target_files:
            self.read(file_dir)

    def __str__(self):
        return f"Total File: {self.total_files}"
    
    

class Malmunchi_book(Preprocess):
    def __init__(self):
        self.result_dir = Path("../../")
        self.result_dir.parent.mkdir(exist_ok=True)

        self.target_files = glob.glob("../../")
        self.total_files = len(self.target_files)

    def read(self, file_dir):
       # text = read_text_from_xml(file_dir)
        text = text.strip()
        if len(text) < 200:
            return 

        self.write(text)



class Munu(Preprocess):
    def __init__(self):
        dataset_dir = Path(".")
        super().__init__(dataset_dir)

    def read(self, file_dir):
        with open(file_dir, "r", encoding="utf-8") as f:
            jsonString = json.load(f)
        paragraph = jsonString["document"][0]["paragraph"]
        text = " ".join([clean_text(data["form"]) for data in paragraph])
        text = text.strip()
        if len(text) < 200:
            return 

        self.write(text)



class EnormousBookCorpus(Preprocess):
    def __init__(self):
        dataset_folder = Path("")
        self.result_dir = Path("")
        self.result_dir.parent.mkdir(exist_ok=True)

        self.target_files = glob.glob(str(dataset_folder/"*"/"*.json"))
        self.total_files = len(self.target_files)

    def unzip(self, zip_dir):
        path_to_zip_file = Path(zip_dir)
        directory_to_extract_to = Path("")
        directory_to_extract_to.mkdir(exist_ok=True)

        with zipfile.ZipFile(str(path_to_zip_file), 'r') as zip_ref:
            zip_ref.extractall(str(directory_to_extract_to))

    def read(self, file_dir):
        if "INFO" in file_dir: return
        with open(file_dir, "r", encoding="utf-8") as f:
            jsonString = json.load(f)
        paragraphs = jsonString["paragraphs"]

        text = ""
        for paragraph in paragraphs:
            sentences = paragraph["sentences"]
            text += " ".join([data["text"] if data["word_count"] >= 9 else "" for data in sentences]) + " "

        text = clean_text(text).strip()
        if len(text) < 200:
            return

        self.write(text)


class Expertise(Preprocess):
    def __init__(self):
        dataset_folder = Path("..")
        super().__init__(dataset_folder)

    def read(self, file_dir):
        with open(file_dir, "r", encoding="utf-8") as f:
            jsonString = json.load(f)
        datas = jsonString["data"]

        for data in datas:
            rows = data["rows"]
            text = " ".join([row["text"] for row in rows])
            text = clean_text(text).strip()

            if len(text) < 200:
                continue 

            self.write(text)



class PaperSumary(Preprocess):
    def __init__(self):
        dataset_folder = Path("")
        super().__init__(dataset_folder)

    def read(self, file_dir):
        with open(file_dir, "r", encoding="utf-8")  as f:
            jsonString = json.load(f)

        datas = jsonString["data"]

        for data in datas:
            summary_section = data["summary_section"][0]
            text = clean_text(summary_section["orginal_text"])
            text = text.strip()
            
            if len(text) < 200:
                continue

            self.write(text)

class Essay(Preprocess):
    def __init__(self):
        dataset_folder = Path("")
        self.result_dir = Path("")
        self.result_dir.parent.mkdir(exist_ok=True)

        self.target_files = glob.glob(str(dataset_folder/""))
        self.total_files = len(self.target_files)
    def read(self, file_dir):
        if "INFO" in file_dir: return
        with open(file_dir, "r", encoding="utf-8") as f:
            jsonString = json.load(f)
        paragraphs = jsonString["paragraph"]

        text =  " ".join([data["paragraph_txt"] for data in paragraphs])
        text = text.replace("", "")

        text = clean_text(text).strip()
        if len(text) < 200:
            return

        self.write(text)


class NAMU(Preprocess):
    def __init__(self):
        self.result_dir = Path("t")
        self.result_dir.parent.mkdir(exist_ok=True)
        from datasets import load_dataset
        self.dataset = load_dataset("")[""]
        self.total_files = len(self.dataset)

    def process_namu(self, data):
        text = data["text"]
        title = data["title"]

        text = clean_text(text)

        to_delete_prefix = ["width", "heigh"]

        splitted_text = text.split("\n")
        def isitin(t): 
            for prefix in to_delete_prefix:
                if prefix in t:
                    return False
            return True

        result = " ".join(filter(isitin, splitted_text))
        self.write(f"<s> {title} Hi {result} </s>")

    def multiprocessing(self):
        pool = Pool(cpu_cores-1)

        with tqdm.tqdm(total=self.total_files) as pbar:
            for _ in tqdm.tqdm(pool.imap_unordered(self.process_namu, self.dataset)):
                pbar.update()

        pool.close()
        pool.join()

    def normal(self):
        for data in self.dataset:
            self.process_namu(data)



if __name__ == "__main__":
    # Done
    # process1 = Malmunchi_book()
    # process1.multiprocessing()

    # Done
    # process2 = Munu()
    # process2.multiprocessing()

    # Done
    process3 = EnormousBookCorpus()
    process3.multiprocessing()

    # process4 = Expertise()
    # print(process4)
    # process4.multiprocessing()
    # process5 = PaperSumary()
    # process5.multiprocessing()
    # process6 = NAMU()
    # process6.multiprocessing()

    process7 = Essay()
    process7.multiprocessing()