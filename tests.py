"""
Simple test script that runs JackAnalyzer and compares resulting .xml files (___Test.xml) to the .xml files provided by Nand to Tetris course (___.xml).
"""
from JackAnalyzer import JackAnalyzer
import filecmp


files_and_directories = [
  "assets\ArrayTest\Main.jack",
  "assets\ExpressionLessSquare",
  "assets\Square"]


print("\nTEST OUTCOMES")
print("=============\n")

test_count = 1
for program in files_and_directories:
  ja = JackAnalyzer(program, "Test")
  ja.analyze()
  for i in range(len(ja.xml_files)):
    analyzed_file = ja.xml_files[i]
    compare_file = ja.get_output_file(ja.jack_files[i])
    check = filecmp.cmp(analyzed_file, compare_file, False)
    outcome = ("FAILED", "PASSED")[check]
    print("Test {0}: {1}".format(test_count, outcome))
    print("Compared {0} to {1}\n".format(analyzed_file, compare_file))
    test_count += 1