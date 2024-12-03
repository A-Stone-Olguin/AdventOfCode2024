# This will be where we call into with different arguments

import argparse
from utils.importFiles import run_day_classes

def main():
  # Create the argument parser
  parser = argparse.ArgumentParser(description="Advent of Code Solver")
  
  # Add arguments
  parser.add_argument("--day", type=str, required=False, help="Day number (e.g., 1 for Day 1) or 'all' for all parts")
  parser.add_argument("--part", type=str, choices=["1", "2", "both"], required=False, help="Part number (1, 2, or both)")
  parser.add_argument("--type", type=str, choices=["example", "input"], required=False, help="What type of input to use")
  
  # Parse the arguments
  args = parser.parse_args()
  
  day = args.day if args.day is not None else "all" 
  part = args.part if args.part is not None else "both"
  type = args.type if args.type is not None else "example"

  run_day_classes(day, part, type)

if __name__ == "__main__":
  main()