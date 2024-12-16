from utils.fileIO import read_file, write_file
from functools import reduce
import re
from baseDayClass import BaseDay
import math
from os import path

class Robot:
  def __init__(self, px, py, vx, vy):
    self.px = px
    self.py = py
    self.vx = vx
    self.vy = vy

  def coords_after_n_steps(self, n, x_bound, y_bound):
    final_loc_x = self.px + n*self.vx
    final_loc_y = self.py + n*self.vy

    fixed_x = final_loc_x % x_bound
    fixed_y = final_loc_y % y_bound

    return (fixed_x, fixed_y)


class Day14(BaseDay):
  def get_robots(self):
    lines = read_file(self.get_input_file_path())
    robots = []
    regex = r'-?\d+'
    for line in lines:
      vals = re.findall(regex, line)
      robot = Robot(*[int(x) for x in vals])
      robots.append(robot)
    return robots
  
  def quadrant_from_coords(self, x, y, x_bound, y_bound):
    half_y = y_bound / 2 - 1
    in_top_half = y <= math.floor(half_y)
    in_bottom_half = y >= math.ceil(half_y) + 1

    half_x = x_bound / 2 - 1
    in_left_half = x <= math.floor(half_x)
    in_right_half = x >= math.ceil(half_x) + 1

    # Coords is counter-clockwise starting in top right
    if in_top_half and in_right_half:
      return 1
    elif in_top_half and in_left_half:
      return 2
    elif in_bottom_half and in_left_half:
      return 3
    elif in_bottom_half and in_right_half:
      return 4
    
    # Otherwise, return False
    return False
  
  def get_quadrant_robots(self, n):
    robots = self.get_robots()
    if 'example' in self.get_input_file_path():
      x_bound = 11
      y_bound = 7
    else:
      x_bound = 101
      y_bound = 103

    quadrants = {1: 0, 2: 0, 3: 0, 4: 0}

    for robot in robots:
      qx, qy = robot.coords_after_n_steps(n, x_bound, y_bound)
      quadrant = self.quadrant_from_coords(qx, qy, x_bound, y_bound)
      if quadrant:
        quadrants[quadrant] += 1
    return quadrants

  def calculate_safety_factor(self, seconds):
    quadrants = self.get_quadrant_robots(seconds)
    return reduce(lambda prev, current: prev*current, quadrants.values(), 1)
  
  def has_row(self, locs, number_row):
    for row, col in locs:
      if number_row[row] < 10:
        continue

      for i in range(1, 11):
        if not( (row, col+i) in locs):
          break

        if i == 10:
          return True
      
    return False

  def print_positions(self, max_seconds):
    robots = self.get_robots()
    x_bound = 101
    y_bound = 103

    for seconds in range(1, max_seconds+1):
      locs = set()
      number_in_row = {}
      for robot in robots:
        col, row = robot.coords_after_n_steps(seconds, x_bound, y_bound)
        locs.add((row, col))
        number_in_row[row] = number_in_row.get(row, 0) + 1

      if self.has_row(locs, number_in_row):
        lines = [['.' for _ in range(x_bound)] for _ in range(y_bound)]
        for row, col in locs:
          lines[row][col] = '*'
        
        directory = f"{path.dirname(__file__)}/../output_files/day14"
        file = f"{directory}/seconds_{seconds}.txt"
        content = "\n".join("".join(row) for row in lines)
        write_file(file, content)

        return seconds
    
    return f"Took the maximum number of seconds: {max_seconds}"

  def part1(self):
    return self.calculate_safety_factor(100)

  def part2(self):
    return self.print_positions(10000)
