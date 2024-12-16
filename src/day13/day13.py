from utils.fileIO import read_file
from functools import reduce
import re
from baseDayClass import BaseDay
from sympy import Matrix, Integer


class ArcadeMachine:
  def __init__(self, Ax, Ay, Bx, By, prize_x,  prize_y):
    self.Ax = Ax
    self.Ay = Ay
    self.Bx = Bx
    self.By = By
    self.prize_x = prize_x
    self.prize_y = prize_y
    self.mat = Matrix([
      [Ax, Bx, prize_x],
      [Ay, By, prize_y]
      ])

  # If rref doesn't return integers, we don't work
  def is_possible(self):
    rref = self.mat.rref()[0]
    last_col = rref.col(2)
    all_integers = all(isinstance(value, Integer) for value in last_col)
    return all_integers, last_col

  def cost(self, a_presses, b_presses):
    return 3*a_presses + b_presses
  
  def get_minimum_cost(self):
    is_possible, last_col = self.is_possible()
    if not is_possible:
      return 0
    
    # We are assuming that rref returns the minimum cost
    return self.cost(last_col[0], last_col[1])

class Day13(BaseDay):
  def create_machines(self, increase_position):
    machines_strs = ''.join(read_file(self.get_input_file_path())).split('\n\n')
    regex = r'.*X\+(\d+), Y\+(\d+)\n.*X\+(\d+), Y\+(\d+)\n.*X=(\d+), Y=(\d+)'
    arcade_machines = []
    for machine_str in machines_strs:
      val_strs = re.findall(regex, machine_str)[0]
      int_vals = [int(x) for x in val_strs]
      if increase_position:
        int_vals[-1] += 10000000000000
        int_vals[-2] += 10000000000000
      arcade_machine = ArcadeMachine(*int_vals)
      arcade_machines.append(arcade_machine)
    return arcade_machines
  
  def total_cost(self, increase_position):
    arcade_machines = self.create_machines(increase_position)
    total_cost = 0
    for arcade_machine in arcade_machines:
      total_cost += arcade_machine.get_minimum_cost()
    return total_cost


  def part1(self):
    return self.total_cost(increase_position=False)

  def part2(self):
    return self.total_cost(increase_position=True)
