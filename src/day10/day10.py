from utils.fileIO import read_file
from functools import reduce
import re
from baseDayClass import BaseDay

class Day10(BaseDay):
  def get_slopes(self):
    return read_file(self.get_input_file_path())
  
  def valid_at_location(self, lines, row, col, value):
    if row < 0 or col < 0 or row >= len(lines) or col >= len(lines[0].strip()) or value < 0:
      return False
    return value == int(lines[row][col])
  
  def accessible_slopes(self, lines, row, col, number):
    directions = [(0,1), (1,0), (-1,0), (0,-1)]
    locations = list(map(lambda x: (row + x[0], col + x[1]), directions))
    filtered_locations = list(filter(lambda x: self.valid_at_location(lines, x[0], x[1], number-1), locations))
    return list(map(lambda x: f"{x[0]},{x[1]}", filtered_locations))

  def find_slopes(self):
    lines = self.get_slopes()
    accesses = {}
    values = {}
    trailends = []
    for row, line in enumerate(lines):
      for col, number_str in enumerate(line.strip()):
        number = int(number_str)
        index = f"{row},{col}"
        if number == 9:
          trailends.append(index)
        accesses[index] = self.accessible_slopes(lines, row, col, number)
        values[index] = number

    return accesses, trailends, values
  
  def num_accessible(self, accesses, values, check):
    possibilities = accesses[check]

    if len(possibilities) == 0:
      return set()
    
    hit_trailheads = set()
    for possibility in possibilities:
      if values[possibility] == 0:
        hit_trailheads.add(possibility)
      else:
        hit_trailheads = hit_trailheads.union(self.num_accessible(accesses, values, possibility))
    return hit_trailheads
  
  def count_accesses(self):
    accesses, trailends, values = self.find_slopes()
    trailhead_count = {}
    for trailend in trailends:
      hit_trailheads = self.num_accessible(accesses, values, trailend)
      for hit_trailhead in hit_trailheads:
        trailhead_count[hit_trailhead] = trailhead_count.get(hit_trailhead, 0) + 1
    return reduce(lambda prev, current: prev + current, trailhead_count.values(), 0)
      
        
  # Same as num accessible, just now counting the distinct possibilities
  def num_paths(self, accesses, values, check):
    possibilities = accesses[check]

    if len(possibilities) == 0:
      return 0
    
    count = 0
    for possibility in possibilities:
      if values[possibility] == 0:
        count +=1
      else:
        count += self.num_paths(accesses, values, possibility)
    return count
  
  def count_paths(self):
    accesses, trailends, values = self.find_slopes()
    sum = 0
    for trailend in trailends:
      sum += self.num_paths(accesses, values, trailend)
    return sum


  def part1(self):
    return self.count_accesses()

  def part2(self):
    return self.count_paths()
