from utils.fileIO import read_file
from functools import reduce
import re
import itertools
from baseDayClass import BaseDay

class Day7(BaseDay):
  def get_total_and_nums(self, line):
    regex = r'(\d+)'
    nums = re.findall(regex, line)
    num_arr = [int(x) for x in nums]
    return num_arr[0], num_arr[1:]
  
  def get_operation_permutations(self, num_vals, concat=False):
    if concat:
      operations = ['+', '*', '||']
    else:
      operations = ['+', '*']

    return list(itertools.product(operations, repeat=num_vals))
  
  def use_operation(self, x, y, operation):
    match operation:
      case '+':
        return x + y
      case '*':
        return x * y
      case '||':
        return int(str(x) + str(y))
      case _:
        return 0
  
  def determine_possible_total(self, total, values, concat=False):
    operation_perms = self.get_operation_permutations(len(values), concat)
    for operation_perm in operation_perms:
      result = reduce(lambda prev, current, i=iter(operation_perm): self.use_operation(prev, current, next(i)), values)
      if result == total:
        return total
    return 0

  def get_calibration(self, concat=False):
    lines = read_file(self.get_input_file_path())
    sum = 0
    for line in lines:
      total, values = self.get_total_and_nums(line)
      sum += self.determine_possible_total(total, values, concat)
    return sum

  def part1(self):
    return self.get_calibration()

  def part2(self):
    return self.get_calibration(concat=True)
