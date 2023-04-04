#!/usr/bin/python
import os
import re
from warnings import warn
from datetime import datetime
from difflib import SequenceMatcher


class DataExtractor:
    """Extracts data from a list of words

    Args:
        words (list[str]): A list of words

    Attributes:
        BEFORE_GEMH_WORD (str): The word before the GEMH value
        BEFORE_DATE_WORD (str): The word before the date value
        BEFORE_WEBSITE_WORD (str): The word before the website value
        AFTER_DATE_WORD (str): The word after the date value
        DATE_FORMATS (list[str]): A list of possible date formats
        BEFORE_NAME_WORD (str): The word before the name value
        NAME_SYMBOLS (list[str]): A list of symbols that could be in a name
        NON_NAME_SYMBOLS (list[str]): A list of symbols that are not in a name
        NON_NAME_WORDS (list[str]): A list of words that are not in a name
        NAME_PATTERN (list[str]): A list of symbols that are used to
            separate names
        GEMH_PATTERN (str): A pattern that is used to find GEMH values
        DATE_PATTERN (str): A pattern that is used to find date values
        WEBSITE_PATTERN (str): A pattern that is used to find website values

    Methods:
        extract_data: Extracts the data from the list of words
        _extract_website_values: Extracts the website values
        _extract_gemh_values: Extracts the GEMH values
        _extract_date_values: Extracts the date values
        _extract_name_values: Extracts the name values
    """
    BEFORE_GEMH_WORD: str = 'ΓΕΜΗ'
    BEFORE_DATE_WORD: str = 'την'
    BEFORE_WEBSITE_WORD: str = 'ιστοσελιδασ'
    AFTER_DATE_WORD: str = 'καταχωρηθηκε'
    DATE_FORMATS: list[str] = ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']
    BEFORE_NAME_WORD: str = 'επωνυμια'
    NAME_SYMBOLS: list[str] = ['-', '&', '.']
    NON_NAME_SYMBOLS: list[str] = [',', ':', '«', '»']
    NON_NAME_WORDS: list[str] = ['ΔΙΑΚΡΙΤΙΚΟΣ']
    NAME_PATTERN: list[str] = [',', ':', ';',]
    GEMH_PATTERN: str = r'\d+'
    DATE_PATTERN: str = r'\d{1,2}[-/]\d{1,2}[-/]\d{4}'
    WEBSITE_PATTERN: str = (
        r'(?:https?://)?(?:www\.)?[a-zA-Z0-9_-]+\.'
        r'[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*'
        r'[a-zA-Z0-9_-]*(?:\?[a-zA-Z0-9_=-]*)?'
    )

    def _extract_website_values(self, words: list[str]) -> set[str]:
        """Extracts the website values
        :param words: A list of words
        :return: The website values
        """
        website_values = set()
        for index, word in enumerate(words):
            ratio = SequenceMatcher(
                None,
                self.BEFORE_WEBSITE_WORD.lower().replace('ς', 'σ'),
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

    def _extract_gemh_values(self, words: list[str]) -> set[int]:
        """Extracts the GEMH values
        :param words: A list of words
        :return: The GEMH values
        """
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
                gemh_values.add(int(next_word))

        return gemh_values

    def _extract_date_values(self, words: list[str]) -> set[str]:
        """Extracts the date values
        :param words: A list of words
        :return: The date values
        """
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
            after_date_word_ratio = SequenceMatcher(
                None,
                self.AFTER_DATE_WORD,
                next_next_word.lower()).ratio()
            if after_date_word_ratio > 0.5:
                date_obj = self._string_to_date(next_word)
                date_values.add(date_obj)

        return date_values

    def _extract_name_values(self, words: list[str]) -> set[str]:
        """Extracts the name values
        :param words: A list of words
        :return: The name values
        """
        name_values = set()
        for index, word in enumerate(words):
            before_name_word_ratio = SequenceMatcher(None,
                                                     self.BEFORE_NAME_WORD,
                                                     word.lower()).ratio()
            if before_name_word_ratio <= 0.5:
                continue

            name = []
            next_index = index + 1
            while index < len(words):
                next_word = words[next_index]
                if (next_word.isupper() or next_word in self.NAME_SYMBOLS) \
                    and next_word not in self.NON_NAME_WORDS:
                    name.append(next_word)
                    next_index += 1
                    continue
                elif name:
                    name = ' '.join(name)
                    for symbol in self.NON_NAME_SYMBOLS:
                        name = name.replace(symbol, '')
                    name_values.add(name)
                break

        return name_values

    def extract_data_from_file(self, filename: str) -> dict[str, str]:
        """Extracts the data from a file
        :param filename: The file name
        :return: The extracted data
        """
        data = {}
        with open(filename, 'r') as f:
            text = f.read()
            words = text.split()
        
        data = {
            'gemh': self._get_first_or_warn(
                self._extract_gemh_values(words),
                f'Duplicate ΓΕΜΗ values found in {filename}',
                f'No ΓΕΜΗ values found in {filename}'),
            'date': self._get_first_or_warn(
                self._extract_date_values(words),
                f'Duplicate date values found in {filename}',
                f'No date values found in {filename}'),
            'website': self._get_first_or_warn(
                self._extract_website_values(words),
                f'Duplicate website values found in {filename}',
                f'No website values found in {filename}'),
            'name': self._get_first_or_warn(
                self._extract_name_values(words),
                f'Duplicate name values found in {filename}',
                f'No name values found in {filename}')
        }
        
        return data
    
    def _get_first_or_warn(self, values: set[str], duplicate_warning: str, no_values_warning: str) -> str:
        """Gets the first value from a set or raises a warning
        :param values: The set of values
        :param duplicate_warning: The warning to raise if there are duplicate values
        :param no_values_warning: The warning to raise if there are no values
        :return: The first value
        """
        if len(values) > 1:
            warn(duplicate_warning)
        elif len(values) == 0:
            warn(no_values_warning)
            return ''
        return next(iter(values))

    def _string_to_date(self, date_str: str) -> datetime:
        """Converts a date string to a datetime object
        :param date_str: The date string
        :return: The datetime object
        """
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass
        raise ValueError(f'Unable to parse date string: {date_str}')


class FileProcessor:
    """Processes the text files
    """
    def __init__(self, folder: str='./txt'):
        self.folder = folder
        self.extractor = DataExtractor()

    def process_files(self):
        """Processes the files
        :return: The extracted data
        """
        if not os.path.isdir(self.folder):
            print(f'Error: {self.folder} is not a valid folder.')
            return

        files_count = 0
        results = []

        for filename in os.listdir(self.folder):
            if not filename.endswith('.txt'):
                continue

            file_path = os.path.join(self.folder, filename)
            if not os.path.isfile(file_path):
                continue

            files_count += 1
            data = self.extractor.extract_data_from_file(file_path)
            if data:
                results.append(data)

        print(f'Processed {files_count} files,'
              f'extracted data from {len(results)} files')
        return results


def main():
    fp = FileProcessor()
    fp.process_files()

if __name__ == '__main__':
    main()
