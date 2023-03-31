import os
import re
import warnings
from difflib import SequenceMatcher
from typing import Dict


class DataExtractor:
    BEFORE_GEMH_WORD: str = "ΓΕΜΗ"
    BEFORE_DATE_WORD: str = "την"
    AFTER_DATE_WORD: str = "καταχωρηθηκε"
    BEFORE_WEBSITE_WORD: str = "ιστοσελιδασ"
    GEMH_PATTERN: str = r"\d+"
    DATE_PATTERN: str = r"\d{1,2}[-/]\d{1,2}[-/]\d{4}"
    WEBSITE_PATTERN: str = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

    def _extract_website_values(self, words: list[str]) -> set[str]:
        website_values = set()
        for index, word in enumerate(words):
            ratio = SequenceMatcher(
                None,
                self.BEFORE_WEBSITE_WORD.lower(),
                word.lower()).ratio()
            if ratio <= 0.5:
                continue

            next_index = index + 1
            if next_index >= len(words):
                continue

            next_word = str(words[next_index])
            if not re.match(self.WEBSITE_PATTERN, next_word):
                continue

            website_values.add(next_word)

        return website_values

    def _extract_gemh_values(self, words: list[str]) -> set[str]:
        gemh_values = set()
        for index, word in enumerate(words):
            gemh_ratio = SequenceMatcher(None,
                                         self.BEFORE_GEMH_WORD,
                                         word.replace('.', '')).ratio()

            if gemh_ratio <= 0.7:
                continue

            next_index = index + 1
            if next_index >= len(words):
                continue

            next_word = words[next_index]
            if re.match(self.GEMH_PATTERN, next_word):
                next_word = re.sub('\W+', '', next_word)
                gemh_values.add(next_word)

        return gemh_values

    def _extract_date_values(self, words: list[str]) -> set[str]:
        date_values = set()
        for index, word in enumerate(words):
            before_date_word_ratio = SequenceMatcher(None,
                                                     self.BEFORE_DATE_WORD,
                                                     word.lower()).ratio()
            if before_date_word_ratio <= 0.5:
                continue

            next_index = index + 1
            if next_index > len(words):
                continue

            next_word = words[next_index]
            if not re.match(self.DATE_PATTERN, next_word):
                continue

            if next_index + 1 >= len(words):
                continue

            next_next_word = words[next_index + 1]
            after_date_word_ratio = SequenceMatcher(None,
                                                    self.AFTER_DATE_WORD,
                                                    next_next_word.lower()).ratio()
            if after_date_word_ratio > 0.5:
                date_values.add(next_word)

        return date_values

    def extract_data_from_file(self, filename: str) -> Dict[str, str]:
        data = {}
        with open(filename, 'r') as f:
            text = f.read()
            words = text.split()

        gemh_values = self._extract_gemh_values(words)
        date_values = self._extract_date_values(words)
        website_values = self._extract_website_values(words)

        if len(gemh_values) > 1:
            warnings.warn(f"Warning: Duplicate ΓΕΜΗ values found in {filename}")
        elif len(gemh_values) == 1:
            data['gemh'] = list(gemh_values)[0]

        if len(date_values) > 1:
            warnings.warn(f"Warning: Duplicate date values found in {filename}")
        elif len(date_values) == 1:
            data['date'] = list(date_values)[0]

        if len(website_values) > 1:
            warnings.warn(f"Warning: Duplicate website values found in {filename}")
        elif len(website_values) == 1:
            data['website'] = list(website_values)[0]
        elif len(website_values) == 0:
            warnings.warn(f"Warning: No website values found in {filename}")
            data['website'] = ''

        return data


class FileProcessor:
    def __init__(self):
        self.cwd = os.getcwd()
        self.extractor = DataExtractor()
        
    def process_files(self):
        print(len(os.listdir(self.cwd)))
        files_count = 0
        results = []

        for filename in os.listdir(self.cwd):
            if not filename.endswith('.txt'):
                continue

            files_count += 1
            data = self.extractor.extract_data_from_file(filename)
            if data:
                results.append(data)

        print(f"Processed {files_count} files, extracted data from {len(results)} files")
        print(results, len(results))

def main():
    fp = FileProcessor()
    fp.process_files()

if __name__ == '__main__':
    main()
