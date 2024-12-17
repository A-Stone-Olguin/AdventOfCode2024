from utils.fileIO import read_file
from functools import reduce
from baseDayClass import BaseDay

class Day15(BaseDay):
  def get_instructions_and_locs(self, double):
    lines = read_file(self.get_input_file_path())
    locs = {}
    commands = []
    in_commands = False
    for row, line in enumerate(lines):
      if len(line.strip()) == 0:
        in_commands = True

      for col, char in enumerate(line.strip()):

        if char == '@':
          start_row, start_col = row, col
          if double:
            locs[(row, 2*col)] = char
            locs[(row, 2*col+1)] = '.'
            # print('Start!', locs)
          else:
            locs[(row, col)] = char
          continue

        if in_commands:
          commands.append(char)
        elif char == 'O' and double:
          locs[(row, 2*col)] = '['
          locs[(row, 2*col+1)] = ']'
        elif char == 'O':
          locs[(row, col)] = '['
        elif double:
          locs[(row, 2*col)] = char
          locs[(row, 2*col+1)] = char
        else:
          locs[(row, col)] = char

    return locs, commands, (start_row, start_col)
  

  def move(self, locs, direction, row, col, double):
    moving = {'^': (-1, 0), '>': (0, 1), '<': (0, -1), 'v': (1, 0)}
    (row_change, col_change) = moving[direction]
    (r, c) = (row+row_change, col+col_change)
    # don't move if hitting edge
    if locs[(r, c)] == '#':
      return row, col
    
    
    # Recursively move objects
    if locs[(r, c)] == '[' or locs[(r, c)] == ']':
      if double:
        if locs[(r, c)] == '[' and direction == '>':
          if locs[(r, c+2)] == '[':
            self.move(locs, direction, r, c+2, double)
            # TODO here
      else:
        self.move(locs, direction, r, c, double)
  
    # update the moved location
    if locs[(r, c)] == '.':
      if double:
        previous = {'^': (1, 0), '>': (0, -1), '<': (0, 1), 'v': (-1, 0)}
        (r1, c1) = previous[direction]
        prev_char = locs[(r+r1, c+c1)]
        # Check if can move
        if prev_char == '[' or prev_char == ']':
          if direction == '^' or direction == 'v':
            other_check = {'[': (0, 1), ']': (0, -1)}
            (r2, c2) = other_check[prev_char]
            # If we have both dots available, move both
            if locs[(r+r2, c+c2)] == '.':
              locs[(r, c)], locs[(r+r1, r+c1)] = locs[(r+r1, c+c1)], locs[(r, c)]
              locs[(r+r1, c+c2)], locs[(r+r2, c+c2)] = locs[(r+r2, c+c2)], locs[(r+r1, c+c2)]
          # else:

        
        else:
          locs[(r, c)], locs[(row, col)] = locs[(row, col)], locs[(r, c)]
      else:
        locs[(r, c)], locs[(row, col)] = locs[(row, col)], locs[(r, c)]
      return r, c
    
    return row, col
  
  def calculate_objects(self, locs):
    sum = 0
    for (row, col), char in locs.items():
      if char == '[':
        sum += row*100 + col
    return sum
  
  def sum_coords(self, double):
    locs, commands, (row, col) = self.get_instructions_and_locs(double)
    for direction in commands:
      row, col = self.move(locs, direction, row, col, double)
    return self.calculate_objects(locs)


  def part1(self):
    return self.sum_coords(double=False)

  def part2(self):
    # return self.sum_coords(double=True)
    return 'not done'
  
