from utils.fileIO import read_file
from functools import reduce
import re
from baseDayClass import BaseDay

class Day5(BaseDay):
  def is_order(self, line):
    return '|' in line
  
  def is_update(self, line):
    return ',' in line
  
  def get_updates_and_orders(self):
    lines = read_file(self.get_input_file_path())
    orders = []
    updates = []
    for line in lines:
      if self.is_order(line):
        orders.append(line)
      elif self.is_update(line):
        updates.append(line)
    return updates, orders
  
  def get_vals(self, line):
    regex = r'(\d+)'
    matches = re.findall(regex, line)
    values = [int(x) for x in matches]
    return values
  
  def make_orders_dict(self, orders):
    orders_dict = {}
    for order in orders:
      vals = self.get_vals(order)
      first = vals[0]
      second = vals[1]

      sub_dict = orders_dict.get(first, {})
      sub_dict[second] = True

      orders_dict[first] = sub_dict
    return orders_dict
  
  def rule_exists(self, orders_dict, first, second):
    first_check = orders_dict.get(first, False)
    if not first_check:
      return False
    
    second_check = first_check.get(second, False)
    if not second_check:
      return False
    
    return True
    
  
  def is_right_order(self, orders_dict, update_vals):
    result = True
    for i, num in enumerate(update_vals):
      sublist = [update_vals[j] for j in range(i+1, len(update_vals))]
      correctly_placed = reduce(lambda prev, current: prev and self.rule_exists(orders_dict, num, current), sublist, True)
      result = result and correctly_placed
    return result
  
  def get_middle_values_sum(self, updates, orders):
    orders_dict = self.make_orders_dict(orders)
    sum = 0
    for update in updates:
      update_vals = self.get_vals(update)
      right_order = self.is_right_order(orders_dict, update_vals)
      if right_order:
        middle_index = len(update_vals) // 2
        middle_value = update_vals[middle_index]
        sum += middle_value
    return sum
  
  def get_incorrect_updates(self, updates, orders):
    orders_dict = self.make_orders_dict(orders)
    incorrect_updates = []
    for update in updates:
      update_vals = self.get_vals(update)
      right_order = self.is_right_order(orders_dict, update_vals)
      if not right_order:
        incorrect_updates.append(update_vals)
    return incorrect_updates, orders_dict
  
  def fix_incorrect(self, incorrect_update, orders_dict):
    for i, num in enumerate(incorrect_update):
      sublist = [incorrect_update[j] for j in range(i+1, len(incorrect_update))]
      for j, check_val in enumerate(sublist):
        if not self.rule_exists(orders_dict, num, check_val) and self.rule_exists(orders_dict, check_val, num):
          temp = incorrect_update[i]
          incorrect_update[i] = incorrect_update[i+j+1]
          incorrect_update[i+j+1] = temp
          return self.fix_incorrect(incorrect_update, orders_dict)
    return incorrect_update
    
  def part1(self):
    updates, orders = self.get_updates_and_orders()
    return self.get_middle_values_sum(updates, orders)

  def part2(self):
    updates, orders = self.get_updates_and_orders()
    incorrect_updates, orders_dict = self.get_incorrect_updates(updates, orders)
    sum = 0
    for incorrect_update in incorrect_updates:
      fixed = self.fix_incorrect(incorrect_update, orders_dict)
      middle_index = len(fixed) // 2
      middle_value = fixed[middle_index]
      sum += middle_value
    return sum
