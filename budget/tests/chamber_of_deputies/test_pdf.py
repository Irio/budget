import shutil
import tempfile
from unittest import TestCase

from budget.chamber_of_deputies.pdf import PDF


class TestPDF(TestCase):
    def setUp(self):
        self.subject = PDF('budget/tests/fixtures/single_page.pdf')

    def test_extract_text_single_page(self):
        tempfolder = tempfile.mkdtemp()
        pdf_path = '{}/single_page.pdf'.format(tempfolder)
        shutil.copy('budget/tests/fixtures/single_page.pdf', pdf_path)
        PDF(pdf_path).extract_text()
        with open('budget/tests/fixtures/single_page.txt') as content_path:
            expected_content = content_path.read()
            with open(pdf_path.replace('.pdf', '.txt')) as result_path:
                result_content = result_path.read()
                self.assertEqual(expected_content, result_content)

    def test_content_multi_page(self):
        tempfolder = tempfile.mkdtemp()
        pdf_path = '{}/multi_page.pdf'.format(tempfolder)
        shutil.copy('budget/tests/fixtures/multi_page.pdf', pdf_path)
        PDF(pdf_path).extract_text()
        with open('budget/tests/fixtures/multi_page.txt') as content_path:
            expected_content = content_path.read()
            with open(pdf_path.replace('.pdf', '.txt')) as result_path:
                result_content = result_path.read()
                self.assertEqual(expected_content, result_content)

    def test_content_multi_documents(self):
        tempfolder = tempfile.mkdtemp()
        pdf_1_path = '{}/single_page.pdf'.format(tempfolder)
        shutil.copy('budget/tests/fixtures/single_page.pdf', tempfolder)
        pdf_2_path = '{}/multi_page.pdf'.format(tempfolder)
        shutil.copy('budget/tests/fixtures/multi_page.pdf', tempfolder)

        PDF('{}/*.pdf'.format(tempfolder)).extract_text()

        doc_1_fixture = open('budget/tests/fixtures/single_page.txt')
        expect_doct_1_content = doc_1_fixture.read()
        doc_1_fixture.close()
        doc_2_fixture = open('budget/tests/fixtures/multi_page.txt')
        expect_doct_2_content = doc_2_fixture.read()
        doc_2_fixture.close()

        with open(pdf_1_path.replace('.pdf', '.txt')) as result_path:
            result_content = result_path.read()
            self.assertEqual(expect_doct_1_content, result_content)
        with open(pdf_2_path.replace('.pdf', '.txt')) as result_path:
            result_content = result_path.read()
            self.assertEqual(expect_doct_2_content, result_content)
