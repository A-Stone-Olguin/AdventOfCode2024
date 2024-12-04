from utils.fileIO import read_file
import re
from functools import reduce
from baseDayClass import BaseDay

class Day3(BaseDay):
  def get_muls(self, line):
    regex = r'mul\((\d{1,3}),(\d{1,3})\)'
    sum = 0
    tuples = re.findall(regex, line)
    for (numStr1, numStr2) in tuples:
      sum += int(numStr1) * int(numStr2)
    return sum


  def check_for_muls(self):
    lines = read_file(self.get_input_file_path())
    sum = 0
    for line in lines:
      sum += self.get_muls(line)
    return sum
  

  def inactive_muls(self):
    lines = read_file(self.get_input_file_path())
    regex1 = r'don\'t\(\).*?do\(\)'
    sum = 0

    # Put lines into single line
    line = ''.join(lines)
    active_line = ''.join(re.split(regex1, line.replace('\n', '')))
    sum = self.get_muls(active_line)
    return sum


  def part1(self):
    return self.check_for_muls()

  def part2(self):
    return self.inactive_muls()
