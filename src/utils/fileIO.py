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


# Writes to a file
def write_file(relativePath, content):
  # Get the absolute path to the current script's directory
  baseDir = os.path.dirname(os.path.abspath(__file__))
  # Resolve the full path
  fullPath = os.path.join(baseDir, relativePath)

  # Create the parent directories if they don't exist
  os.makedirs(os.path.dirname(fullPath), exist_ok=True)
  
  with open(fullPath, "w") as f:
    f.write(content)
