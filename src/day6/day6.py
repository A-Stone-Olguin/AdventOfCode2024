from utils.fileIO import read_file
from functools import reduce
import copy
from baseDayClass import BaseDay

class Day6(BaseDay):
  def turn_right(self, direction):
    match direction:
      case 'u':
        return 'r'
      case 'r':
        return 'd'
      case 'd':
        return 'l'
      case 'l':
        return 'u'
      case _:
        return ''
  
  def direction_to_path(self, direction):
    match direction:
      case 'u':
        return -1, 0
      case 'r':
        return 0, 1
      case 'd':
        return 1, 0
      case 'l':
        return 0, -1
      case _:
        return 0, 0
      
  def get_start_position(self, lines):
    for row_num, line in enumerate(lines):
      for col_num, char in enumerate(line):
        if char == '^':
          return row_num, col_num
        
  def is_out_of_bounds(self, lines, row, col):
    return col < 0 or row < 0 or row >= len(lines) or col >= len(lines[row]) or row == '\n' or col == '\n'
        
  def walk_and_mark(self, lines, row_num, col_num, direction):
    marked_path = set()
    while(True):
      # mark the values
      marked_path.add(f"{row_num},{col_num}")

      row_change, col_change = self.direction_to_path(direction)
      next_y_step = row_num + row_change
      next_x_step = col_num + col_change
      if self.is_out_of_bounds(lines, next_y_step, next_x_step):
        return marked_path
      
      next_step = lines[next_y_step][next_x_step]
      if next_step == '#':
        direction = self.turn_right(direction)
      else:
        row_num = next_y_step
        col_num = next_x_step

  def walk_and_detect_loop(self, lines, row_num, col_num, direction, obstruction):
    marked_path = {}
    row_obs, col_obs = obstruction
    while(True):
      # Return if we already came here (looped)
      if direction in marked_path.get(f"{row_num},{col_num}", []):
        return 1

      # mark the values
      marked_path[f"{row_num},{col_num}"] = marked_path.get(f"{row_num},{col_num}", []) + [direction]

      row_change, col_change = self.direction_to_path(direction)
      next_y_step = row_num + row_change
      next_x_step = col_num + col_change
      if self.is_out_of_bounds(lines, next_y_step, next_x_step):
        return 0
      
      next_step = lines[next_y_step][next_x_step]
      if next_step == '#' or (next_y_step == row_obs and next_x_step == col_obs):
        direction = self.turn_right(direction)
      else:
        row_num = next_y_step
        col_num = next_x_step

        
  def traverse(self):
    lines = read_file(self.get_input_file_path())
    start_row, start_col = self.get_start_position(lines)
    marked_path = self.walk_and_mark(lines, start_row, start_col, 'u')
    return len(marked_path)

  def count_looping_possibilities(self):
    lines = read_file(self.get_input_file_path())
    start_row, start_col = self.get_start_position(lines)
    marked_path = self.walk_and_mark(lines, start_row, start_col, 'u')
    loops = 0
    for string in marked_path:
      row, col = [int(x) for x in string.split(',')]
      if row == start_row and col == start_col:
        continue

      obstruction = (row, col)
      loops += self.walk_and_detect_loop(lines, start_row, start_col, 'u', obstruction)
    return loops

  

  def part1(self):
    return self.traverse()

  def part2(self):
    print('expecting 6, 1586')
    return self.count_looping_possibilities()
