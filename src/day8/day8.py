from utils.fileIO import read_file
from functools import reduce
import re
import itertools
from baseDayClass import BaseDay

class Day8(BaseDay):
  def get_signal_locations(self):
    lines = read_file(self.get_input_file_path())
    signal_locations = {}
    bounds = {}
    for row_num, line in enumerate(lines):
      for col_num, val in enumerate(line.strip()):
        bounds[f"{row_num},{col_num}"] = True
        if val != '.':
          signal_locations[val] = signal_locations.get(val, []) + [(row_num, col_num)]
    return signal_locations, bounds
  
  def get_every_distance(self, ordered_pairs):
    combinations = list(itertools.combinations(ordered_pairs, 2))
    antinodes = []
    for ((first_row, first_col), (second_row, second_col)) in combinations:
      distance = (second_row-first_row, second_col-first_col)

      antinode1 = (second_row + distance[0], second_col + distance[1])
      antinode2 = (first_row - distance[0], first_col - distance[1])



      antinodes += [antinode1, antinode2]
    return antinodes
  
  def get_every_antinode(self, ordered_pairs, bounds):
    combinations = list(itertools.combinations(ordered_pairs, 2))
    antinodes = []
    for ((first_row, first_col), (second_row, second_col)) in combinations:
      distance = (second_row-first_row, second_col-first_col)
      row, col = second_row, second_col
      while(bounds.get(f"{row},{col}", False)):
        antinodes.append((row, col))
        row, col = row + distance[0], col + distance[1]
      row, col = first_row, first_col

      while(bounds.get(f"{row},{col}", False)):
        antinodes.append((row, col))
        row, col = row - distance[0], col - distance[1]

    return antinodes
    
    

  
  def find_anti_nodes(self):
    signal_locations, bounds = self.get_signal_locations()
    unique_antinodes = {}
    for signal_coords in signal_locations.values():
      antinodes = self.get_every_distance(signal_coords)
      for (row, col) in antinodes:
        if bounds.get(f"{row},{col}", False):
          unique_antinodes[f"{row},{col}"] = True
    return len(unique_antinodes.keys())
  
  def find_all_anti_nodes(self):
    signal_locations, bounds = self.get_signal_locations()
    antinodes = {}
    for signal_coords in signal_locations.values():
      possible_antinodes = self.get_every_antinode(signal_coords, bounds)
      for (row, col) in possible_antinodes:
        antinodes[f"{row},{col}"] = True
    return len(antinodes.keys())




  def part1(self):
    return self.find_anti_nodes()

  def part2(self):
    return self.find_all_anti_nodes()
