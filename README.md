# RandomCountGenerator
```
Create a function that prints a random number between 1 and 5 to stdout (or console). The probability distribution of the numbers should be as follows:

1 - 50%
2 - 25%
3 - 15%
4 - 5%
5 - 5%

Or roughly that (no need to worry about rounding errors, etc)

Change the function to a method, add a class member that stores a history of the last 100 numbers, and a function to return the frequency percentages of each number.

Create a method that reads the most recently generated random number and the current time and writes them both to disk on one line.

Modify the writer function so it is launched in a different thread. The random number generator should put the numbers and timestamps into a queue that the writer function uses to write its output to disk.

Modify the program so it has 5 copies of the random number function running concurrently in different threads. They should all feed the single writer thread counts and timestamps, and the writer should ensure they are written in chronological order.
```
