from utils.fileIO import read_file
import re
from functools import reduce
from baseDayClass import BaseDay

class Day2(BaseDay):

  def reduce_safe(self, tuple, second_value):
    truth, value, increase_sum = tuple
    return ( \
      truth and abs(value - second_value) >= 1 and abs(value - second_value) < 4, \
      second_value, \
      increase_sum + int(second_value - value > 0) \
      )
  
  def determine_safeness(self, numbers):
    truth, _, sum = reduce( \
      lambda prevVal, current: self.reduce_safe(prevVal, current), \
      numbers, \
      (True, numbers[0] + 1, 0)\
    )
    is_safe = (truth and (sum == (len(numbers)-1) or sum == 0))
    return is_safe
  
  def check_with_dampener(self, numbers):
    # Test each sublist
    for i in range(len(numbers)):
      sublist = numbers[:i] + numbers[i+1:]
      if self.determine_safeness(sublist):
        return True
    return False


  def check_list(self, check_with_dampener=False):
    lines = read_file(self.get_input_file_path())
    safe_count = 0
    for line in lines:
      numbersStrings = re.findall(r'\d+', line)
      numbers = [int(x) for x in numbersStrings]
      is_safe = self.determine_safeness(numbers)

      if check_with_dampener and not is_safe:
        is_safe = self.check_with_dampener(numbers)

      safe_count += int(is_safe)
    return safe_count

  


  def part1(self):
    return self.check_list(False)

  def part2(self):
    return self.check_list(True)
