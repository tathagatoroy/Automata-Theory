## TATHAGATO ROY 
## ROLL : 2019111020

# To Run any of the file :
``` sh
python3 q1.py path/to/input/file path/to/output/file

```

# Q1

Convert to transform regex to NFA

Approach :
First convert the infix regex to postfix using shunting yard  

Then Convert the postfix to an NFA using Thompson construction wih the help of stacks  

Assumption : Empty set is cannot be input  


# Q2

Convert an NFA to DFA

Approach :

Create a directed graph of states with only epsilon edges.  
Use floyd Warshal to compute distance matrix and then for each state generate the list of reachable states using only epsilon transitions

The above generates the e-closures for each set.After that follow the algorithm given in Sipser to Convert the NFA to DFA

# Q3

Convert regex to DFA

Approach :

Create a N-state GNFA from the dfa .Then Create a 2 state GNFA iteratively by removing  non - final and non - start state at every iteration

The final edge weight is the regex

# Q4

DFA minimization 

Approach : 

Remove all unreachable states

The partition the remaining states using the  equivalence class idea from Myhill-Node Theorem

#  LINK TO THE VIDEO

https://iiitaphyd-my.sharepoint.com/:v:/g/personal/tathagato_roy_research_iiit_ac_in/ERZ6GV6rzipNlDrJT6mD5RsByLhRSRmW2k7bhtQ9GYHCuQ?e=wpRjDq
