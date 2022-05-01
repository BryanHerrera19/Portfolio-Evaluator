# COMP_141-Project-Phase-1.1
COMP_141 Project Evaluator By:

Bryan Herrera & Bryant Tran

Instructions:

Run in command line using: python3 main.py testDriver.txt output.txt

Overview:
Takes a block of code from a small imperative language that was assigned, and outputs
each tokens type, creates an AST tree, and outputs the value of each variable.

Example Input:
if 2 * 5 - 8 then
  x := 0;
while x * 4 - 2 do
  skip
endwhile
else
  x := 7
endif;
  y := 1
  
Example Output:

![Token List](https://github.com/BryanHerrera19/COMP_141-Project-Evaluator/blob/main/Images/Token%20List.png?raw=true)
![AST and Output](https://github.com/BryanHerrera19/COMP_141-Project-Evaluator/blob/main/Images/AST%20and%20output.png?raw=true)
