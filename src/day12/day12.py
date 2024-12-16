from utils.fileIO import read_file
from functools import reduce
import re
from baseDayClass import BaseDay

class Day12(BaseDay):
  def label_plant_locs(self):
    lines = read_file(self.get_input_file_path())
    all_locs = {}
    for row, line in enumerate(lines):
      for col, char in enumerate(line.strip()):
        all_locs[char] = all_locs.get(char, set()).union({f"{row},{col}"})
    return all_locs
  
  def get_grouped_set(self, character_locs, row, col):
    if len(character_locs) == 0:
      return set()

    positions = [(0,1), (1,0), (-1, 0), (0, -1)]
    new_set = {f"{row},{col}"}
    adjacents = []
    for rc, cc in positions:
      row_change = row + rc
      col_change = col + cc
      location = f"{row_change},{col_change}"
      if location in character_locs:
        new_set = new_set.union({location})
        adjacents.append((row_change, col_change))

    if len(new_set) <= 1:
      return new_set
    

    for (r, c) in adjacents:
      new_set = new_set.union(self.get_grouped_set(character_locs.difference(new_set), r, c))
  
    return new_set
  
  def get_groupings(self, all_locs):
    grouped_locs = {}
    for char in all_locs.keys():
      char_vals = set()
      sets = []
      for location in all_locs[char]:
        if location in char_vals:
          continue
        row, col = location.split(',')
        new_set = self.get_grouped_set(all_locs[char], int(row), int(col))
        sets.append(new_set)
        char_vals = char_vals.union(new_set)
      grouped_locs[char] = sets
    return grouped_locs
  
  def number_adjacent(self, locs, char, row, col):
    positions = [(0,1), (1,0), (-1, 0), (0, -1)]
    mapped_positions = map(lambda x: f"{row+x[0]},{col+x[1]}" in locs[char], positions)
    return reduce(lambda prev, current: prev + int(current), mapped_positions, 0)
  
  def calculate_perimeter_and_area(self, groupings, all_locs, char):
    perimeters = []
    areas = []
    for s in groupings[char]:
      perimeter_count = 0
      area_count = 0
      for location in s:
        row, col = [int(x) for x in location.split(',')]
        number_adjacent = self.number_adjacent(all_locs, char, row, col)
        perimeter_count += 4 - number_adjacent
        area_count += 1
      perimeters.append(perimeter_count)
      areas.append(area_count)
    return perimeters, areas
  
  ## Edges = Vertices from Euler's lemma
  def number_vertices(self, all_locs, char, row, col):
    returns = {0: 4, 1: 2, 4: 0}
    number_adjacent = self.number_adjacent(all_locs, char, row, col)
    if number_adjacent != 2 and number_adjacent != 3 and number_adjacent != 4:
      return returns[number_adjacent]
    
    char_locs = all_locs[char]
    in_row = f"{row-1},{col}" in char_locs and f"{row+1},{col}" in char_locs
    in_col = f"{row},{col-1}" in char_locs and f"{row},{col+1}" in char_locs

    if number_adjacent == 4:
      positions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
      diagonals = map(lambda x: f"{row+x[0]},{col+x[1]}" in char_locs, positions)
      number_diagonals = reduce(lambda prev, current: prev + int(current), diagonals, 0)
      return 4 - number_diagonals


    if number_adjacent == 2 and (in_row or in_col):
      return 0
    elif number_adjacent == 2 and f"{row-1},{col}" in char_locs:
      if f"{row},{col-1}" in char_locs:
        return 2 - int(f"{row-1},{col-1}" in char_locs)
      else:
        return 2 - int(f"{row-1},{col+1}" in char_locs)
    elif number_adjacent == 2 and f"{row+1},{col}" in char_locs:
      if f"{row},{col-1}" in char_locs:
        return 2 - int(f"{row+1},{col-1}" in char_locs)
      else:
        return 2 - int(f"{row+1},{col+1}" in char_locs)
    elif number_adjacent == 2:
      return 1
    
    # Check the "poked out part"
    if in_col and f"{row-1},{col}" in char_locs:
      return 2 - int(f"{row-1},{col-1}" in char_locs) - int(f"{row-1},{col+1}" in char_locs)
    elif in_col:
      return 2 - int(f"{row+1},{col-1}" in char_locs) - int(f"{row+1},{col+1}" in char_locs)
    
    if f"{row},{col-1}" in char_locs:
      return 2 - int(f"{row-1},{col-1}" in char_locs) - int(f"{row+1},{col-1}" in char_locs)
    else:
      return 2 - int(f"{row-1},{col+1}" in char_locs) - int(f"{row+1},{col+1}" in char_locs)



  
  def calculate_sides_and_area(self, groupings, all_locs, char):
    sides = []
    areas = []
    for s in groupings[char]:
      side_count = 0
      area_count = 0
      for location in s:
        row, col = [int(x) for x in location.split(',')]

        side_count += self.number_vertices(all_locs, char, row, col)
        area_count += 1
      sides.append(side_count)
      areas.append(area_count)
    return sides, areas

  def get_price(self, perimeter_check=True):
    all_locs = self.label_plant_locs()
    groupings = self.get_groupings(all_locs)
    total_price = 0
    for char in all_locs.keys():
      if perimeter_check:
        perimeter, area = self.calculate_perimeter_and_area(groupings, all_locs, char)
        vals = [perimeter[i]*area[i] for i in range(len(perimeter))]
        total_price += sum(vals)
      else:
        sides, area = self.calculate_sides_and_area(groupings, all_locs, char)
        vals = [sides[i]*area[i] for i in range(len(sides))]
        total_price += sum(vals)
    return total_price
      

  def part1(self):
    return self.get_price(perimeter_check=True)

  def part2(self):
    return self.get_price(perimeter_check=False)
