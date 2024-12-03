import importlib
import re
from pathlib import Path
import os


def get_day_classes(base_path):
  """Get all day classes dynamically."""
  day_classes = []
  for folder in Path(base_path).iterdir():
    if folder.is_dir() and folder.name.startswith("day"):
      try:
        # Dynamically import the module
        module = importlib.import_module(f"{folder.name}.{folder.name}")
        
        day_number = re.findall(r'\d+', folder.name)[0]

        class_name = f"Day{day_number}"
        day_class = getattr(module, class_name)

        # Make a tuple of the folder name and the class
        day_classes.append((day_number, day_class))
      except Exception as e:
        print(f"Error loading {folder.name}: {e}")
  return day_classes

def get_day_class(number):
  try:
    # Dynamically import the module
    module = importlib.import_module(f"day{number}.day{number}")

    class_name = f"Day{number}"
    day_class = getattr(module, class_name)
  except Exception as e:
    print(f"Error loading day{number}: {e}")
    return []
  return [(number, day_class)]


def run_day_classes(day="all", part="both", type="example"):
  """Instantiate and run part1 and part2 for each day's class."""

  srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  if day == "all":
    day_classes = get_day_classes(srcDir)
  else:
    day_classes = get_day_class(int(day))
  
  for day_number, DayClass in sorted(day_classes):
    day_instance = DayClass(day_number, type)
    if part == "both":
      print(f"=== day{day_number} ===")
      print(f"Part 1: {day_instance.part1()}")
      print(f"Part 2: {day_instance.part2()}")
    elif part == "1":
      print(f"=== day{day_number} part {part}===")
      print(f"Part 1: {day_instance.part1()}")
    elif part == "2":
      print(f"=== day{day_number} part {part}===")
      print(f"Part 2: {day_instance.part2()}")
    else:
      print("Invalid part given")


