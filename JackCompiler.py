from CompilationEngine import CompilationEngine
import sys
import os


# NOTE -- mostly doesn't work...
class JackCompiler:
  """
  Main compiler class. Accepts a file or directory path as an input. Drives compilation process and writes to output file(s).
  """

  def __init__(self, input, output_file_tag=""):
    self.jack_files = self.get_files(input)
    self.vm_files = []
    self.output_file_tag = output_file_tag
    self.compilation_engine = None
  
  def compile(self):
    """Reads Jack file(s), drives compilation process, and writes to VM file(s)."""
    for jack_file in self.jack_files:
      vm_code = None
      with open(jack_file, 'r', encoding='utf-8') as f:
        raw_code = f.read()
        self.compilation_engine = CompilationEngine(raw_code) # doesn't work
        vm_code = self.compilation_engine.compile() # doesn't work
      vm_file = self.get_output_file(
        jack_file, self.output_file_tag)
      with open(vm_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(vm_code))
      self.vm_files.append(vm_file)

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
      """Returns the .vm file path that corresponds with a given Jack file. A file tag can be added (e.g. to distinguish from a compare file)."""
      return jack_file[:-5] + file_tag + ".vm"