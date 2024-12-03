from utils.fileIO import read_file
import re
from functools import reduce
from baseDayClass import BaseDay

class Day1(BaseDay):
  def parse_lists(self):
    lines = read_file(self.get_input_file_path())
    leftList = []
    rightList = []
    for line in lines:
      left, right = re.findall(r'\d+', line)
      leftList.append(int(left))
      rightList.append(int(right))
    return leftList, rightList

  def parse_to_dict(self):
    lines = read_file(self.get_input_file_path())
    dict = {}
    leftList = []
    for line in lines:
      left, right = re.findall(r'\d+', line)
      leftList.append(int(left))
      dict[right] = dict.get(right, 0) + 1
    return leftList, dict

  def count_lists(self, leftList, dict):
    sum = 0
    for value in leftList:
      sum += value*dict.get(str(value), 0)
    return sum

  def pair_lists(self, leftList, rightList):
    leftList.sort()
    rightList.sort()
    differences = [abs(rightValue - leftList[i]) for i, rightValue in enumerate(rightList)]
    return reduce(lambda prev, current: prev + current, differences)

  def part1(self):
    leftList, rightList = self.parse_lists()
    return self.pair_lists(leftList, rightList)

  def part2(self):
    leftList, dict = self.parse_to_dict()
    return self.count_lists(leftList, dict)
