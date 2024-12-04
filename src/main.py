# This will be where we call into with different arguments

import argparse
import time
from utils.importFiles import run_day_classes

def print_time(start, end):
  print("\n")
  print("=== Total time ===")
  print(f"Time elapsed: {end-start:.2f} seconds")

def main():
  # Create the argument parser
  parser = argparse.ArgumentParser(description="Advent of Code Solutions")
  
  # Add arguments
  parser.add_argument("--day", type=str, required=False, help="Day number (e.g., 1 for Day 1) or 'all' for all parts")
  parser.add_argument("--part", type=str, choices=["1", "2", "both"], required=False, help="Part number (1, 2, or both)")
  parser.add_argument("--type", type=str, choices=["example", "input"], required=False, help="What type of input to use")
  
  # Parse the arguments
  args = parser.parse_args()
  
  day = args.day if args.day is not None else "all" 
  part = args.part if args.part is not None else "both"
  type = args.type if args.type is not None else "input"

  start_time = time.time()
  run_day_classes(day, part, type)
  end_time = time.time()
  print_time(start_time, end_time)

if __name__ == "__main__":
  main()