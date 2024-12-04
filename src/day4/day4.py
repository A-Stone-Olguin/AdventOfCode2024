from utils.fileIO import read_file
from functools import reduce
from baseDayClass import BaseDay

class Day4(BaseDay):    
  def check_character(self, lines, row_start, col_start, row_change, col_change):
    chars = ['M', 'A', 'S']
    found = True
    try:
      for i, character in enumerate(chars):
        new_row = row_start + (i+1)*row_change
        new_col = col_start + (i+1)*col_change
        if new_row < 0 or new_col < 0:
          return False
        
        found = found and (lines[new_row][new_col] == character)
      return found
    except IndexError as _:
      return False
    
  def check_direction(self, lines, direction, row_start, col_start):
    match direction:
      case 'r':
        row_change, col_change = 0, 1
      case 'l':
        row_change, col_change = 0, -1
      case 'u':
        row_change, col_change = 1, 0
      case 'd':
        row_change, col_change = -1, 0
      case 'ru':
        row_change, col_change = 1, 1
      case 'rd':
        row_change, col_change = -1, 1
      case 'lu':
        row_change, col_change = 1, -1
      case 'ld':
        row_change, col_change = -1, -1
      case _:
        return False
    return self.check_character(lines, row_start, col_start, row_change, col_change) 
      

  def search_for_xmas(self):
    lines = read_file(self.get_input_file_path())
    xmas_count = 0
    directions = ['r', 'l', 'd', 'u', 'ld', 'lu', 'ru', 'rd']
    for row_num, line in enumerate(lines):
      for col_num, char in enumerate(line):
        if char != 'X':
          continue
        xmas_count += reduce(lambda prev, current: prev + int(self.check_direction(lines, current, row_num, col_num)), directions, 0)
    return xmas_count
  

  def check_corners(self, lines, row_num, col_num):
    try:
      corners = {}
      if row_num-1 < 0 or col_num -1 < 0:
        return {}
      
      # Make sure that there are no matching diagonals
      if lines[row_num-1][col_num-1] == lines[row_num+1][col_num+1]:
        return {}
      
      corner_vals =[
        lines[row_num-1][col_num-1],
        lines[row_num-1][col_num+1],
        lines[row_num+1][col_num-1],
        lines[row_num+1][col_num+1]
      ]
      for corner_val in corner_vals:
        corners[corner_val] = corners.get(corner_val, 0) + 1
      return corners
    except IndexError as _:
      return {}

  def search_for_x_mas(self):
    lines = read_file(self.get_input_file_path())
    x_mas_count = 0
    for row_num, line in enumerate(lines):
      for col_num, char in enumerate(line):
        if char != 'A':
          continue
      
        corners = self.check_corners(lines, row_num, col_num)
        x_mas_count += int(corners.get('M', 0) == 2 and corners.get('S', 0) == 2)
    return x_mas_count




  def part1(self):
    return self.search_for_xmas()

  def part2(self):
    return self.search_for_x_mas()
