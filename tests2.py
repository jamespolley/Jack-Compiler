"""
Simple test script that runs JackCompiler and compares resulting .vm files (___Test.vm) to the .vm files provided by Nand to Tetris course (___.vm).
"""
from JackCompiler import JackCompiler
import filecmp


file_directories = [
  "assets2\Seven",
  "assets2\ConvertToBin",
  "assets2\Square",
  "assets2\Average",
  "assets2\Pong",
  "assets2\ComplexArrays"]

print("\nTEST OUTCOMES")
print("=============\n")

test_count = 1
for program in file_directories:
  jc = JackCompiler(program, "Test")
  jc.analyze()
  for i in range(len(jc.vm_files)):
    analyzed_file = jc.vm_files[i]
    compare_file = jc.get_output_file(jc.jack_files[i])
    check = filecmp.cmp(analyzed_file, compare_file, False)
    outcome = ("FAILED", "PASSED")[check]
    print("Test {0}: {1}".format(test_count, outcome))
    print("Compared {0} to {1}\n".format(analyzed_file, compare_file))
    test_count += 1