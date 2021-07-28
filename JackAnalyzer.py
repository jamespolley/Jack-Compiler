# TO DO
#   Allow directory as input
#   Allow command line execution of JackAnalyzer
#   Create get_xml_file method

from CompilationEngineXML import CompilationEngineXML


class JackAnalyzer:
    def __init__(self, file_or_directory):
        self.comp_eng = None
        self.jack_files = []
        self.process_input(file_or_directory)
    
    def analyze(self):
        for jack_file in self.jack_files:
            with open(jack_file, 'r', encoding='utf-8') as f:
                raw_code = f.read()
                self.comp_eng = CompilationEngineXML(raw_code)
                self.comp_eng.compile()
            xml_file = (jack_file[:-5] + "Attempt.xml")
            with open(xml_file, "w", encoding='utf-8') as f:
                for line in self.comp_eng.xml:
                    f.write(line)
    
    def process_input(self, file_or_directory):
        self.jack_files.append(file_or_directory)