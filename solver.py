
# Built-in
import os
from pathlib import Path

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

def main():
    for i, inp in enumerate(inputs):
        if i != 0 and i != 1 and i != 3: continue
        print("+ Solving:", inp)
        read_input(input_dir_path/inp)
        filter_buffers()
        solve()
        write_output(out_dir_path/(inp.replace("in", "out")))
        reset()
        print("Done!!")
        
def _print_obj_list(array):
    for obj in array:
        print(obj)
        
def solve():
    global projects, contributors
    day = 0; current_projects = {}
    while True:
        # Comprobamos si hay projectos acabados
        delete_ps = []
        for p, pinfo in current_projects.items():
            dl = pinfo["deathline"]
            if dl == day:
                delete_ps.append(p)
                contrib = pinfo["contributors"]
                for c in contrib:
                    contributors.append(c)
        for p in delete_ps:
            current_projects.pop(p)
        
        # Comprobamos si hay projectos que se puedan empezar
        posible_projects = []
        for pp in projects:
            if pp.can_start(team=contributors):
                posible_projects.append(pp)
                
        if len(posible_projects) != 0:
            # Hayamos el ratio de los proyectos
            scores_r = []
            for p in posible_projects:
                minus = day - (p.bb + p.duration)
                if minus < 0: minus = 0
                actual_score = (p.score - minus)/p.duration
                if actual_score < 0: actual_score = 0
                scores_r.append(actual_score)
            
            # Añadidos contribuidores a trabajar en el proyecto
            max_sc = max(scores_r)
            if max_sc == 0: 
                # No merece la pena seguir haciendo proyectos
                break
            index = scores_r.index(max_sc)
            p_chosen = posible_projects[index]; solutions[p_chosen] = []
            # Asignamos los contribuidores al proyecto
            for r in p_chosen.roles:
                for c in contributors:
                    if c.fits_role(r) and c not in solutions[p_chosen]:
                        solutions[p_chosen].append(c)
                        break
            for c in solutions[p_chosen]:
                contributors.remove(c)
            # Añadimos el proyecto a los proyectos actuales
            current_projects[p_chosen] = {
                'contributors': solutions[p_chosen],
                'deathline': day + p_chosen.duration
            }
            projects.remove(p_chosen)
        elif len(current_projects) == 0:
            break
        day += 1
        if len(projects) == 0:
            # Ya hemos asignado todos los proyectos 
            break
        
def filter_buffers():
    global projects, contributors
    # Descartamos los projectos que tengan una habilidad que ningun contribuidor tenga
    valid_projects = []
    for p in projects:
        roles = p.roles; not_roles = {}; remove_p = False
        for r in roles:
            not_roles[r] = 0
            for c in contributors:
                if not c.fits_role(r):
                    not_roles[r] += 1
        for r, num in not_roles.items():
            if num == len(contributors):
                remove_p = True
        if not remove_p:
            valid_projects.append(p)
    # Eliminamos los contribuidores que no tengan skills
    valid_c = []
    for c in contributors:
        if c.has_skills():
            valid_c.append(c)
    # Reemplazamos los buffers globales
    contributors = valid_c
    projects = valid_projects
    
def write_output(output_path:Path) -> None:
    output = f"{len(solutions)}\n"
    for p, cs in solutions.items():
        output += p.name + "\n"
        contrib_line = ""
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






