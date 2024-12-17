from utils.fileIO import read_file
from functools import reduce
import re
from baseDayClass import BaseDay

class Day9(BaseDay):
  def get_file_ids(self):
    line = read_file(self.get_input_file_path())[0].strip()
    regex = r'(\d)(\d)'
    values = re.findall(regex, line)
    id = 0
    file_values = {}
    sizes = {}
    for (file_blocks, free_space) in values:
      file_values[id] = {'used': int(file_blocks), 'free': int(free_space)}
      # Creating a stack of ids with a suitable size
      sizes[int(file_blocks)] = [id] + sizes.get(int(file_blocks), [])
      id += 1
    # Get last value and give it zero free blocks
    if len(line) % 2 == 1:
      file_values[id] = {'used': int(line[-1]), 'free': 0}
      sizes[int(line[-1])] = [id] + sizes.get(int(line[-1]), [])

    return file_values, sizes, id
  
  def file_ids_to_list(self, file_ids):
    list = []
    indices = {}
    for id, file_info in file_ids.items():
      blocks, free = file_info['used'], file_info['free']
      for _ in range(blocks):
        list.append(id)
        indices[id] = indices.get(id, []) + [len(list)-1]
      for _ in range(free):
        list.append('.')
    return list, indices
  
  def move_values(self, file_list):
    reverse_iter = len(file_list) - 1
    for i, file_value in enumerate(file_list):
      if file_value != '.':
        continue

      if reverse_iter <= i:
        return i
      
      file_list[i], file_list[reverse_iter] = file_list[reverse_iter], file_list[i]
      reverse_iter -= 1
      # Keep going back if there is free space
      while(file_list[reverse_iter] == '.'):
        reverse_iter -= 1

  def loop_and_check(self, file_info, file_list, indices, swap_id):
    most_recent = 0
    for i in range(len(file_list)):
      file_value = file_list[i]
      if file_value != '.':
        # Increased by one index, it is the current one
        if file_value == most_recent + 1:
          most_recent = file_value
        continue

      # Try seeing if we can swap here
      if file_info[swap_id]['used'] <= file_info[most_recent]['free']:
        file_info[most_recent]['free'] -= file_info[swap_id]['used']
        for j, index in enumerate(indices[swap_id]):
          file_list[i+j], file_list[index] = file_list[index], file_list[i+j]
        return



  def move_new_values(self, file_info, file_list, sizes, indices, last_id):
    for swap_id in range(last_id, -1, -1):
      self.loop_and_check(file_info, file_list, indices, swap_id)

  def determine_checksum(self):
    file_values, _, _ = self.get_file_ids()
    file_list, _ = self.file_ids_to_list(file_values)
    split_index = self.move_values(file_list)
    sum = 0
    for i, value in enumerate(file_list[:split_index]):
      sum += i * value
    return sum

  def determine_new_checksum(self):
    file_values, sizes, last_id = self.get_file_ids()
    file_list, indices = self.file_ids_to_list(file_values)
    # print('original',file_list)
    # print('sizes', sizes)
    self.move_new_values(file_values, file_list, sizes, indices, last_id)
    sum = 0
    # print('final',file_list)
    for i, value in enumerate(file_list):
      if value != '.':
        sum += i * value
    return sum



  def part1(self):
    return self.determine_checksum()

  def part2(self):
    return 'not done'
