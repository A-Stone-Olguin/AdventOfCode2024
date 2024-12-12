from utils.fileIO import read_file
from functools import reduce
import re
from baseDayClass import BaseDay
memoization = {}
class Day11(BaseDay):
  def get_stones(self):
    line = read_file(self.get_input_file_path())[0].strip()
    number_strings = re.findall(r'\d+', line)
    return [int(x) for x in number_strings]
  
  def rules(self, stone, max_blinks, n):
    if memoization.get(f"{stone},{n}", False):
      return memoization[f"{stone},{n}"]
    
    if n == max_blinks:
      return 0

    if stone == 0:
      recurse_value = self.rules(1, max_blinks, n+1)
      memoization[f"{stone},{n}"] = recurse_value
      return recurse_value
  
    string_stone = str(stone)
    if len(string_stone) % 2 == 0:
      halfway = len(string_stone)//2
      left = int(string_stone[:halfway])
      right = int(string_stone[halfway:])
      
      left_recurse = self.rules(left, max_blinks, n+1)
      right_recurse = self.rules(right, max_blinks, n+1)
      value = 1 + left_recurse + right_recurse
      memoization[f"{stone},{n}"] = value
      return value
    
    value = self.rules(stone*2024, max_blinks, n+1)
    memoization[f"{stone},{n}"] = value
    return value
  
  def blink_n_times(self, n):
    stones = self.get_stones()
    count = len(stones)
    for stone in stones:
      count += self.rules(stone, n, 0)
    return count

  def part1(self):
    return self.blink_n_times(25)

  def part2(self):
    return self.blink_n_times(75)
