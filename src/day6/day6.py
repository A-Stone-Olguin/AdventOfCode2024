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
    return col < 0 or row < 0 or row >= len(lines) or col >= len(lines[row])
        
  def walk_and_mark(self, lines, row_num, col_num, direction):
    marked_path = {}
    while(True):
      # mark the values
      marked_path[f"{row_num},{col_num}"] = 1

      row_change, col_change = self.direction_to_path(direction)
      next_y_step = row_num + row_change
      next_x_step = col_num + col_change
      if self.is_out_of_bounds(lines, next_y_step, next_x_step):
        return len(marked_path.keys())
      
      next_step = lines[next_y_step][next_x_step]
      if next_step == '#':
        direction = self.turn_right(direction)
      else:
        row_num = next_y_step
        col_num = next_x_step

    

        
  def traverse(self):
    lines = read_file(self.get_input_file_path())
    start_row, start_col = self.get_start_position(lines)
    length = self.walk_and_mark(lines, start_row, start_col, 'u')
    return length
    

  def determine_loop(self, lines, row_num, col_num, direction, proposed_row, proposed_col):
    line_copy = copy.deepcopy(lines)

    line_arr = list(line_copy[proposed_row])
    line_arr[proposed_col] = '#'
    line_str = ''.join(line_arr)
    line_copy[proposed_row] = line_str

    marked_path = {}

    while(True):
      print('row, col', row_num, col_num, proposed_row, proposed_col, direction)
      if direction in marked_path.get(f"{row_num},{col_num}", []):
        return True

      marked_path[f"{row_num},{col_num}"] = marked_path.get(f"{row_num},{col_num}", []) + [direction]

      row_change, col_change = self.direction_to_path(direction)
      next_y_step = row_num + row_change
      next_x_step = col_num + col_change
      if self.is_out_of_bounds(line_copy, next_y_step, next_x_step):
        return False
      
      next_step = line_copy[next_y_step][next_x_step]
      if next_step == '#':
        direction = self.turn_right(direction)
      else:
        row_num = next_y_step
        col_num = next_x_step

  # def determine_loop(self, lines, row_num, col_num, direction):
  #   marked_path = {}
  #   not_finished = True
  #   while(not_finished):
  #     # mark the values
  #     marked_path.get(f"{row_num},{col_num}", []) + [direction]

  #     row_change, col_change = self.direction_to_path(direction)
  #     next_y_step = row_num + row_change
  #     next_x_step = col_num + col_change
  #     if self.is_out_of_bounds(lines, next_y_step, next_x_step):
  #       not_finished = False
      
  #     next_step = lines[next_y_step][next_x_step]
  #     if next_step == '#':
  #       direction = self.turn_right(direction)
  #     else:
  #       row_num = next_y_step
  #       col_num = next_x_step
  #   for row, line in enumerate(lines):
  #     for col, char in enumerate(line):
  #       if char == '^' or char == '#':
  #         continue

  #       if marked_path.get(f"{row},{col}", False):
  #         if marked_path[row][col] 
    


  def count_loop_objects(self):
    lines = read_file(self.get_input_file_path())
    start_row, start_col = self.get_start_position(lines)
    sum = 0
    for row_num, line in enumerate(lines):
      for col_num, char in enumerate(line):
        if char != '^' and char != '#':
          sum += int(self.determine_loop(lines, start_row, start_col, 'u', row_num, col_num))
    return sum

  

  def part1(self):
    return self.traverse()

  def part2(self):
    return self.count_loop_objects()
