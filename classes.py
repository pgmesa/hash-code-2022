
class Skill:
    def __init__(self, name:str, level:int) -> None:
        self.name = name
        self.level = level
        
    def __str__(self) -> str:
        return f"Name: {self.name} | level: {self.level}"
        
class Contributor:
    def __init__(self, name:str) -> None:
        self.name = name
        self.skills = []
        
    def __str__(self) -> str:
        return f"{self.name} | Num-Skills = {len(self.skills)}"
        
    def add_skill(self, skill_name:str, level:int) -> None:
        skill = Skill(skill_name, level)
        self.skills.append(skill)
    
    def get_num_skills(self) -> int:
        return len(self.skills)
    
    def fits_role(self, skill:Skill) -> bool:
        for sk in self.skills:
            if sk.name == skill.name and sk.level >= skill.level:
                return True
        return False
    
    def has_skills(self) -> bool:
        for skill in self.skills:
            if skill.level != 0:
                return True
        return False
    
    def get_skill(self, skill_name:str) -> Skill:
        for sk in self.skills:
            if sk.name == skill_name:
                return sk
    
    def level_up_skill(self, skill_name:str):
        for sk in self.skills:
            if sk.name == skill_name:
                sk.level += 1
                break

class Project:
    def __init__(self, name:str, duration:int, score:int, best_before:int, numc:int) -> None:
        self.name = name
        self.duration = duration 
        self.score = score
        self.bb = best_before
        self.numc = numc
        self.start_date = None
        self.roles = []
        
    def __str__(self) -> str:
        return f"{self.name} {self.duration} {self.score} {self.bb} {self.numc}"
    
    def add_role(self, role_name:str, level:int) -> None:
        role = Skill(role_name, level)
        self.roles.append(role)
    
    def get_role(self, role_name:str, level:int) -> Skill:
        for role in self.roles:
            if role.name == role_name and level == role.level:
                return role
        else: return None
        
    def get_num_roles(self) -> int:
        return len(self.roles)
    
    def can_start(self, team:list[Contributor]) -> bool:
        roles_taken = []; already_working = []
        for r in self.roles:
            for c in team:
                if c.fits_role(r) and c not in already_working:
                    roles_taken.append(r)
                    already_working.append(c)
                    break
        if len(roles_taken) == self.get_num_roles():
            return True
        return False
    
    def start(self, date_num:int) -> None:
        if self.start_date is not None:
            print("2 inits")
        self.start_date = date_num

