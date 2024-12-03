# AdventOfCode2024
Repository for solutions to the 2024 Advent of Code

## Running the code
We can run any part by simply calling the main python script with command line arguments.

```sh
python3 src/main.py --day <day> --part <part number> --type <type of input file>
```

None of the arguments are required, there are defaults for each value.

### CLI Arguments
* day
  * This can be any given day (1, ..., 25) that is completed
  * Optionally, can be given the value `all` and all days will be run
  * The default value is `all`
* part
  * This can be given values of `1`, `2`, or `both`
  * These regard which part of each day will be ran
  * The default value is `both`
* type
  * This regards what type of input file is to be used for tests
  * The allowed values are `example` or `input`
  * The default value is `example`