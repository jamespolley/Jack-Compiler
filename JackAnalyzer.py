# TO DO
#   Allow command line execution of JackAnalyzer
#   Create docstrings
from CompilationEngineXML import CompilationEngineXML
import sys
import os


class JackAnalyzer:
    def __init__(self, input, output_file_tag = ""):
        self.jack_files = self.get_files(input)
        self.xml_files = []
        self.output_file_tag = output_file_tag
        self.comp_eng = None
    
    def analyze(self):
        for jack_file in self.jack_files:
            with open(jack_file, 'r', encoding='utf-8') as f:
                raw_code = f.read()
                self.comp_eng = CompilationEngineXML(raw_code)
                self.comp_eng.compile()
            xml_file = self.get_output_file(
                jack_file, self.output_file_tag)
            with open(xml_file, "w", encoding='utf-8') as f:
                for line in self.comp_eng.xml:
                    f.write(line)
            self.xml_files.append(xml_file)

    
    @staticmethod
    def get_files(file_or_directory_path):
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
        return jack_file[:-5] + file_tag + ".xml"