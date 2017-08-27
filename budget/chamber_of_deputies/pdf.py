import glob
import subprocess


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
