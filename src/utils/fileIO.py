import os

# Reads a file
def read_file(relativePath):
  # Get the absolute path to the current script's directory
  baseDir = os.path.dirname(os.path.abspath(__file__))
  # Resolve the full path
  fullPath = os.path.join(baseDir, relativePath)

  with open(fullPath, "r") as f:
    lines = f.readlines()
  return lines

