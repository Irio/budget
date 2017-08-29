import itertools
import pandas as pd
from pyspark import SparkContext
import re

from .amendment_parser import AmendmentParser


SC = SparkContext()


class TextFileParser(object):
    """
    Class to read text version of PDFs and parse amendments from them.
    """

    def __init__(self, pathname):
        """
        pathname: the path for the text file(s). It accepts Unix style pathname
            pattern expansion, like `/Documents/*.txt`.
        """
        self.pathname = pathname

    def attributes(self):
        """
        Return a list of attributes for every amendment page.
        """
        result = SC.textFile(self.pathname) \
            .map(lambda line: line.strip()) \
            .filter(lambda line: line != '') \
            .flatMap(lambda line: re.split(r'\s{2,}', line)) \
            .map(lambda line: '---' if line == 'CONGRESSO NACIONAL' else line)
        values = result.collect()
        return [list(g)
                for k, g in itertools.groupby(values, lambda x: x == '---')
                if not k]

    def dataframe(self):
        pages = [AmendmentParser(attr).parse_page()
                 for attr in self.attributes()]
        data = pd.DataFrame(pages)
        data['file_generation_date'] = pd.to_datetime(
            data['file_generation_date'], dayfirst=True)
        return data
