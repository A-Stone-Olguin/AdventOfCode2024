import os
class BaseDay:
    """Base class for all day modules."""

    def __init__(self, number, type = "example"):
      self.number = number
      self.type = type

    def get_input_file_path(self):
      # Get the absolute path to the current script's directory
      baseDir = os.path.dirname(os.path.abspath(__file__))
      # Resolve the full path
      fullPath = os.path.join(baseDir, "./input_files")

      if self.type == "example":
        file = f'{fullPath}/day{self.number}/example.txt'
      else:
        file = f'{fullPath}/day{self.number}/input.txt'
      return file

    def part1(self):
        """Part 1 logic. Override this in subclasses."""
        raise NotImplementedError("Part 1 is not implemented")
    
    def part2(self):
        """Part 2 logic. Override this in subclasses."""
        raise NotImplementedError("Part 2 is not implemented")