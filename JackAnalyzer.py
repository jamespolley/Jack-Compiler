from ParserXML import ParserXML
import sys
import os


class JackAnalyzer:
    """
    Main analyzer class. Accepts a file or directory path as an input. Drives analysis process and writes to output file(s).
    """
    
    def __init__(self, input, output_file_tag=""):
        self.jack_files = self.get_files(input)
        self.xml_files = []
        self.output_file_tag = output_file_tag
        self.parser = None
    
    def analyze(self):
        """Reads Jack file(s), drives analysis process, and writes to XML file(s)."""
        for jack_file in self.jack_files:
            with open(jack_file, 'r', encoding='utf-8') as f:
                raw_code = f.read()
                self.parser = ParserXML(raw_code)
                self.parser.compile()
            xml_file = self.get_output_file(
                jack_file, self.output_file_tag)
            with open(xml_file, "w", encoding='utf-8') as f:
                for line in self.parser.xml:
                    f.write(line)
            self.xml_files.append(xml_file)
    
    @staticmethod
    def get_files(file_or_directory_path):
        """Returns a list of files, given either a relative file or directory path."""
        jack_files = []
        if os.path.isdir(file_or_directory_path):
            directory = os.listdir(file_or_directory_path)
            for f in directory:
                if f.endswith(".jack"):
                    jack_file = os.path.join(file_or_directory_path, f)
                    jack_files.append(jack_file)
        elif os.path.isfile(file_or_directory_path):
            jack_files.append(file_or_directory_path)
        else:
            raise Exception(
                "INVALID INPUT: '{}' is not a relative path to a file \
                or directory."\
                .format(file_or_directory_path))
        return jack_files
    
    @staticmethod
    def get_output_file(jack_file, file_tag=""):
        """Returns the .xml file path that corresponds with a given Jack file. A file tag can be added (e.g. to distinguish from a compare file)."""
        return jack_file[:-5] + file_tag + ".xml"