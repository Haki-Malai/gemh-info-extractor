import os
import datetime

from data_extractor import DataExtractor


def test_extract_data_from_file():
    de = DataExtractor()

    filename = 'test_file.txt'
    with open(filename, 'w') as f:
        f.write('ΓΕΜΗ 123456\n'
                'την 01/01/2022 καταχωρηθηκε\n'
                'ΕΠΩΝΥΜΙΑ TEST COMPANY\n'
                'ΔΙΑΚΡΙΤΙΚΟΣ 1234\n'
                'ιστοσελιδασ https://www.example.com\n')
    data = de.extract_data_from_file(filename)

    assert data['gemh'] == 123456
    assert data['date'].strftime('%d/%m/%Y')
    assert data['name'] == 'TEST COMPANY'
    assert data['website'] == 'https://www.example.com'

    os.remove(filename)
