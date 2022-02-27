# Hash Code 2022

Program made in the 2022 Hash Code Google competition qualification round (our first coding challenge) (24 of february)

Read the problem and try your solution (this link might become unreachable when the practice mode ends): https://codingcompetitions.withgoogle.com/hashcode/round/00000000008caae7/000000000098afc8 

Run 'solver.py' to solve the inputs of the challege. We only managed to solve 3/6 files in the competition:
- a_an_example.in.txt -> t=0s
- b_better_start_small.in.txt -> t=0s
- d_dense_schedule.in.txt -> t=0s

When trying to solve the other 3 files, our algorithm remained indefinitely solving (not efficient enough). The original team submission is in the 'round_submission.zip'

In the practice mode I made some changes two days later (26 of february) to optimize, clean and fix issues, being able to solve all input files (also added tqdm pbars for geting feedback while solving):
- a_an_example.in.txt -> t=0s
- b_better_start_small.in.txt -> t=0s
- c_collaboration.in.txt -> t=19.56 s
- d_dense_schedule.in.txt -> t=17.2 s
- e_exceptional_skills.in.txt -> t=5 min 45 s
- f_find_great_mentors.in.txt -> t=7 min 52 s

Notice that the algorithm doesn't take into account a few important aspects to fully develop a complete solution (e.g. we didn't have time to add the mentoring feature).

## Algorithm Scores
We compare our results against those achieved by the rank 1 team in the classification.
| Input File | Our Score | Score after Optimizing | Rank 1 team Score |
|     :---:      |  :---:   | :---: | :---: |  
| a_an_example.in.txt  | 20 | 20 | 33 |
| b_better_start_small.in.txt  | 310.676 | 743.704 | 969.087 |
| c_collaboration.in.txt  | 0 | 140.005 | 229.517 |
| d_dense_schedule.in.txt  | 54.835 | 133.020 | 674.945 |
| e_exceptional_skills.in.txt  | 0 | 207.366 | 1.640.454 |
| f_find_great_mentors.in.txt  | 0 | 211.117 | 706.200 |
| Total  | 365.531 | 1.435.232 | 4.220.236 |

For the program to execute custom input files that you have created, set the 'DEBUG' variable to True and create the 'own_inputs' directory and put the files you want to be solved there (the solutions will be saved in a directory called 'own_solutions')

In case you want to clone the repository and modify the code to try to improve the algorithm (now that the practice mode of the classification problem is open [today - february 26 of 2022]), execute the 'mkzip.py' file to create a submission file to perform an attempt on the page (if you create more files that you want to put in the zip, you must add them in the 'files_to_submit' variable).

## Execute Solver
First install the external dependencies
```
pip install -r requirements.txt
```
- Windows
```
py solver.py
```
- Linux y Mac
```
python3 solver.py
```
