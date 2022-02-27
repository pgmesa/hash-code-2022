
# Built-in
import os
import copy
from math import floor
from time import time
from pathlib import Path
from functools import cmp_to_key

from tqdm import tqdm

# Custom
from classes import Project, Contributor

DEBUG = False

# Paths
if not DEBUG:
    input_dir_path = Path('./input_data').resolve()
    inputs = os.listdir(input_dir_path)
    out_dir_path = Path('./solutions').resolve()
else:
    input_dir_path = Path('./own_inputs').resolve()
    inputs = os.listdir(input_dir_path)
    out_dir_path = Path('./own_solutions').resolve()
if not os.path.exists(out_dir_path):
    os.mkdir(out_dir_path)
# Vars
num_contributors = 0; num_projects = 0
contributors = []; projects = []
# Solutions vars
solutions = {}

# --------------------------------------------------------------------
# ------ UTILS
def timer(func):
    def f(*a, **ka):
        t0 = time()
        func(*a,**ka)
        tf = time()
        total_secs = round(tf-t0, 2)
        if total_secs < 60:
            print(f"\nElapsed time: {total_secs} s")
        else: 
            mins = floor(total_secs/60)
            secs = int(total_secs - mins*60)
            print(f"\nElapsed time: {mins} min {secs} s")
    return f

def _print_obj_list(array):
    for obj in array:
        print(obj)
        
# ------ Problem solving
def main():
    for i, inp in enumerate(inputs):
        print("+ Solving:", inp)
        read_input(input_dir_path/inp)
        solve()
        write_output(out_dir_path/(inp.replace(".in.", ".out.")))
        reset()
        print("Done!!")
        
@timer       
def solve():
    global projects, contributors
    day = 0; current_projects = {}; deathlines = set(); not_possible_p = []
    print("Calculating projects to assign...(it can take a few minutes)")
    while True:       
        # Comprobamos si hay projectos que se puedan empezar
        possible_projects = []
        for pp in projects:
            if pp.can_start(team=contributors):
                possible_projects.append(pp)
            elif pp not in not_possible_p and day == 0:
                not_possible_p.append(pp)
        if day == 0:
            pbar_p = tqdm(projects, desc="Projects to Assign", unit=" projects", position=0, leave=None)
            projects = copy.copy(possible_projects)
        elif len(projects) == 0:
            now_possible = []
            for pp in not_possible_p:
                if pp.can_start(team=contributors):
                    now_possible.append(pp)
            for pp in now_possible:
                possible_projects.append(pp)
                not_possible_p.remove(pp)
                projects.append(pp)
        # Si hay projectos que se puedan empezar vamos asignando hasta que no se puedan mas        
        if len(possible_projects) != 0:
            # Hayamos el ratio de los proyectos
            def calc_ratio(p:Project) -> int:
                minus = day - (p.bb + p.duration)
                if minus < 0: minus = 0
                actual_score = (p.score - minus)/p.duration
                if actual_score < 0: actual_score = 0
                return actual_score
            
            scores_r = []       
            for p in possible_projects:
                scores_r.append(calc_ratio(p))
                
            while len(possible_projects) != 0:                
                # Añadidos contribuidores a trabajar en el proyecto
                max_sc = max(scores_r)
                s_msg = f"Projects score ration -> {round(max_sc,2)}"
                if day == 0:
                    pbar_s = tqdm(desc=s_msg, position=1, leave=False)
                pbar_s.set_description(s_msg); pbar_s.refresh()
                if max_sc == 0: 
                    # No merece la pena seguir haciendo proyectos
                    pbar_p.close(); pbar_s.close()
                    print("\n[!] Exiting: All project scores now worth <= 0 points")
                    return
                index = scores_r.index(max_sc); scores_r.pop(index)
                p_chosen = possible_projects[index]
                p_chosen.start(day); solutions[p_chosen] = []
                pbar_p.update(1)
                # Asignamos los contribuidores al proyecto
                for r in p_chosen.roles:
                    for c in contributors:
                        if c.fits_role(r) and c not in solutions[p_chosen]:
                            solutions[p_chosen].append(c)
                            break
                for c in solutions[p_chosen]:
                    contributors.remove(c)
                # Añadimos el proyecto a los proyectos actuales
                deathline = day + p_chosen.duration
                current_projects[p_chosen] = {
                    'contributors': solutions[p_chosen],
                    'deathline': deathline
                }
                deathlines.add(deathline)
                projects.remove(p_chosen); possible_projects.remove(p_chosen)
                # Vemos si hay mas disponibles ahora que se han eliminado contribuidores
                possible_projects2 = []; scores_r = []
                for pp in possible_projects:
                    if pp.can_start(team=contributors):
                        possible_projects2.append(pp)
                        scores_r.append(calc_ratio(pp))
                possible_projects = possible_projects2
        elif len(projects) == 0 and len(current_projects) == 0:
            break
        # Avanzamos hasta que se finalice la primera deathline de los proyectos en curso para liberar 
        # contribuidores y volver a chequear si hay proyectos disponibles 
        forward = min(deathlines); deathlines.remove(forward)
        delete_ps = []
        for p, pinfo in current_projects.items():
            roles = p.roles
            dl = pinfo["deathline"]
            if dl <= forward:
                delete_ps.append(p)
                contrib = pinfo["contributors"]
                for i, c in enumerate(contrib):
                    role = roles[i]
                    sk = c.get_skill(role.name)
                    if sk.level == role.level:
                        c.level_up_skill(sk.name)
                    contributors.append(c)
        for p in delete_ps:
            current_projects.pop(p)
        day = forward
    
def write_output(output_path:Path) -> None:
    global solutions
    output = f"{len(solutions)}\n"
    
    def _compare(c1:Project, c2:Project):
        num1 = c1.start_date
        num2 = c2.start_date
        if num1 < num2: return -1
        elif num1 > num2: return 1
        else: return 0
    
    sorted_ps = sorted(solutions, key=cmp_to_key(_compare))
    for p in sorted_ps:
        output += p.name + "\n"
        contrib_line = ""
        cs = solutions[p]
        for c in cs:
            contrib_line += c.name + " "
        output += contrib_line + "\n"
        
    with open(output_path, 'w') as file:
        file.write(output)
    
def read_input(input_path:Path) -> None:
    global num_contributors, num_projects, contributors, projects  
    # Input read
    lines_to_read = 0; queu_obj = None
    with open(input_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            splitted = line.split(" ")
            if i == 0:
                num_contributors = int(splitted[0])
                num_projects = int(splitted[1])
                continue
            if len(contributors) == num_contributors:
                if lines_to_read == 0:
                    # reading projects
                    name, duration, score, bb, roles = splitted
                    queu_obj = Project(name, int(duration), int(score), int(bb), int(roles))
                    lines_to_read = int(roles)
                else:
                    # add skill to buffered contributor
                    skill_name = splitted[0]
                    level = int(splitted[1])
                    queu_obj.add_role(skill_name, level)
                    lines_to_read -= 1
                    if lines_to_read == 0:
                        projects.append(queu_obj)
            else:
                # reading contributors
                if lines_to_read == 0:
                    # new contributor to add
                    cname = splitted[0]
                    queu_obj = Contributor(cname)
                    lines_to_read = int(splitted[1])
                else:
                    # add skill to buffered contributor
                    skill_name = splitted[0]
                    level = int(splitted[1])
                    queu_obj.add_skill(skill_name, level)
                    lines_to_read -= 1
                    if lines_to_read == 0:
                        contributors.append(queu_obj)
    assert len(contributors) == num_contributors
    assert len(projects) == num_projects

def reset():
    global num_contributors, num_projects, contributors, projects, solutions
    num_contributors = 0; num_projects = 0
    contributors = []; projects = []
    solutions = {}
    
if __name__ == "__main__":
    main()






