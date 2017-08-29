import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

import pandas as pd
import pandas.api.types as ptypes

from budget.chamber_of_deputies.text_file_parser import SC, TextFileParser


class TestTextFileParser(TestCase):
    def setUp(self):
        path = 'budget/tests/fixtures/amendment_attributes.csv'
        self.attributes = pd.read_csv(path, dtype=str)

    def fixture_by_index(self, index):
        return [attr
                for attr in self.attributes.iloc[index].values.tolist()
                if not isinstance(attr, float)]

    def test_attributes_single_page(self):
        subject = TextFileParser('budget/tests/fixtures/single_page.txt')
        self.assertEqual([self.fixture_by_index(10)],
                         subject.attributes())

    def test_attributes_multi_page(self):
        subject = TextFileParser('budget/tests/fixtures/multi_page.txt')
        expected = [self.fixture_by_index(11), self.fixture_by_index(12)]
        self.assertEqual(expected, subject.attributes())

    @patch('budget.chamber_of_deputies.text_file_parser.AmendmentParser')
    def test_dataframe(self, parser_mock):
        parser_mock.return_value.parse_page.return_value = {
            'file_generation_date': '30/12/2016',
            'author': '3841 - Jones Martins',
            'number': '38410001',
        }
        subject = TextFileParser('budget/tests/fixtures/multi_page.txt')
        result = subject.dataframe()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual((2, 3), result.shape)
        self.assertTrue(
            ptypes.is_datetime64_dtype(result['file_generation_date']))
