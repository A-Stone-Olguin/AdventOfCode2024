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
      
  def valid_configuration(self, total, rev_values, concat):
    # We should never have 0, since we remove a value one at a time
    if len(rev_values) == 0:
      return False

    # If our operation path is valid, we check if the result exists
    if len(rev_values) == 1:
      return total == rev_values[0]
    
    # Start the result as false
    result = False

    # Pre-computed values
    check_value = rev_values[0]
    rest_list = rev_values[1:]
    str_total = str(total)
    str_check = str(check_value)

    # Check concatenation first
    if concat and str_total.endswith(str_check):
      modified_total_str = str_total[:-len(str_check)]

      # If the total string is empty, that means this is only valid if the
      # rest of the list is all 1's (use multiplication)
      if len(modified_total_str) == 0:
        return reduce(lambda prev, current: prev and current == 1, rest_list, True)
      
      result = self.valid_configuration(int(modified_total_str), rest_list, concat)
    
    # Check multiplication next
    if not result and total % check_value == 0:
      result = self.valid_configuration(int(total / check_value), rest_list, concat)

    # Check addition last
    if not result:
      subtraction = total-check_value
      # If we subtracted too much, this isn't valid because the other operations aren't valid
      if subtraction < 0:
        return False
      result = self.valid_configuration(subtraction, rest_list, concat)

    return result

  def get_calibration(self, concat):
    lines = read_file(self.get_input_file_path())
    sum = 0
    for line in lines:
      total, values = self.get_total_and_nums(line)
      result = self.valid_configuration(total, values[::-1], concat)
      if result:
        sum += total
    return sum

  def part1(self):
    return self.get_calibration(concat=False)

  def part2(self):
    return self.get_calibration(concat=True)
