import glob
import subprocess
import sys


class PDF:
    """
    Class to handle PDF files for amendments made by congresspeople from
    the Chamber of Deputies on the federal budget.
    """

    def __init__(self, pathname):
        """
        pathname: the path for the PDF file(s). It accepts Unix style pathname
            pattern expansion, like `/Documents/*.pdf`.
        """
        if sys.platform != 'darwin':
            raise (
                'Platform not supported. '
                'Only macOS version of `pdftotext` has the expected behavior.'
            )
        self.filenames = glob.glob(pathname)

    def extract_text(self):
        """
        Create a .txt file for every .pdf in the pathname.
        """
        for filename in self.filenames:
            text_filename = filename.replace('.pdf', '.txt')
            command = 'pdftotext -table -enc "UTF-8" {} {}'
            command = command.format(filename, text_filename)
            subprocess.run(command, shell=True)
