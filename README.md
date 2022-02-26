# Hash Code 2022

Program made in the 2022 Hash Code Google competition qualification round (our first coding challenge).

Read the problem and try your solution (this link might become unreachable when the practice mode ends): https://codingcompetitions.withgoogle.com/hashcode/round/00000000008caae7/000000000098afc8 

Run 'solver.py' to solve the inputs of the challege. We have only managed to solve 3/6 files:
- a_an_example.in.txt
- b_better_start_small.in.txt
- d_dense_schedule.in.txt

When trying to solve the other 3 files, our algorithm remains indefinitely solving (there must be some error), therefore, by default only the inputs (a, b and d) are solved when executing the program and the solutions will be created in a directory called 'solutions' (comment out line 30 of 'solver.py' to try to solve all of them). Notice that our algorithm doesn't take into account some important aspects to fully develop a complete solution (e.g. we didn't have time to add the mentoring feature).

For the program to execute custom input files that you have created, set the 'DEBUG' variable to True and create the 'own_inputs' directory and put the files you want to be solved there (the solutions will be saved in a directory called 'own_solutions')

In case you want to clone the repository and modify the code to try to improve the algorithm (now that the practice mode of the classification problem is open [today - february 26 of 2022]), execute the 'mkzip.py' file to create a submission file to perform an attempt on the page (if you create more files that you want to put in the zip, you must add them in the 'files_to_submit' variable).

## Results of our algorithm
We compare our results against those achieved by the rank 1 team in the classification.
| Fichero | Puntos Obtenidos | Mejor Equipo |
|     :---:      |  :---:      | :---: |  
| a_an_example.in.txt  |  20  | 33 |
| b_better_start_small.in.txt  | 310.676 | 969.087 |
| c_collaboration.in.txt  | 0 | 229.517 |
| d_dense_schedule.in.txt  | 54.835 | 674.945 |
| e_exceptional_skills.in.txt  | 0 | 1.640.454 |
| f_find_great_mentors.in.txt  | 0 | 706.200 |
| Total  | 365.531 | 4.220.236 |

## Execute Solver
- Windows
```
py solver.py
```
- Linux y Mac
```
python3 solver.py
```
