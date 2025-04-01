import re
import os
from OperaPowerRelay import opr
import shutil

# Goal, capture the correct files. Then, capture the directory containing the files. Then, print the directory, as well as the would be directory. No moving anything yet

rule = r".*\.(py)$"
destination = r"C:\Users\Vaynes\Desktop\Test\Scripts"
watched_path = r"C:\Users\Vaynes\Downloads"
moved_folders = set()
paths_and_rules = {
    r"C:\Users\Vaynes\Downloads": [
            (r".*\.(mp4)$", r"C:\Users\Vaynes\Desktop\Test\Videos"), 
            (r".*\.(mp3)$", r"C:\Users\Vaynes\Desktop\Test\Music"), 
            (r".*\.(exe)$", r"C:\Users\Vaynes\Desktop\Test\Executables")
        ],
    r"B:\Games\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg - Copy": [
            (r".*\.(cfg)$", r"C:\Users\Vaynes\Desktop\Test\Configs"),
            (r".*\.(vcfg)$", r"C:\Users\Vaynes\Desktop\Test\VCfgs"),
        ]
    }

def organize_by_rules(path_and_rules: dict[str, list[tuple[str, str]]]) -> None:
    paths = list(path_and_rules.keys())
    for path in paths:
        if not os.path.exists(path):
            opr.print_from("Filesorter", f"{{bg_red}}Path {path} does not exist{{def}}")
            return
        
        opr.print_from("Filesorter", f"{{bg_whi}}Organizing {path}{{def}}")
        for rule, destination in path_and_rules[path]:
            _judicial_court(rule, destination, path)

def _judicial_court(rule: str, destination, path: str) -> None:
    
    dir = opr.enumerate_directory(path, 10, True)
    _due_process(dir, rule, destination, path)
    

def _due_process(dir: list[str, dict[str, list]], rule: str, destination: str, previous_path: str) -> None:
    for _ in dir:
        if isinstance(_, str):
            _judge(crime=rule, defendant=_, scene=previous_path, jail=destination)
        elif isinstance(_, dict):
            for sublist in _.values():
                _due_process(sublist, rule, destination, previous_path)
        else:
            opr.print_from("Filesorter", f"{{bg_yel}}Skipping unknown type: {type(_)}{{def}}")
    pass

def _judge(crime: str, defendant: str, scene: str, jail: str) -> None:
    global moved_folders

    if re.match(crime, defendant):
        opr.print_from("Filesorter", f"{{bg_gre}}{os.path.basename(defendant)} matches rule {crime}{{def}}")
        opr.print_from("Filesorter", f"{{bg_yel}}Old path: {defendant}{{def}}")
        
        rel_path = os.path.relpath(defendant, scene)


        opr.print_from("Filesorter", f"{{bg_yel}}Relative path: {rel_path}{{def}}")

    
        if not os.path.exists(jail):
            os.makedirs(jail, exist_ok=True)

        # checks if the file is inside the directory under watch and moves it exclusively
        if os.path.dirname(defendant) == scene:
            opr.print_from("Filesorter", f"{{bg_blu}}Moving '{os.path.basename(defendant)}' from '{os.path.dirname(defendant)}' to '{jail}'{{def}}")
            shutil.move(defendant, jail)
            return

        # if it isn't gets the parent directory of the file under the director under watch and moves that
        path_folder = defendant
        while True:
            e = os.path.dirname(path_folder)
            if e == scene:
                break
            path_folder = e
        
        if path_folder in moved_folders:
            opr.print_from("Filesorter", f"{{cya}}Directory '{os.path.basename(path_folder)}' has already been moved{{def}}")
            return


        moved_folders.add(path_folder)

        new_path= os.path.join(jail, os.path.basename(path_folder))
        opr.print_from("Filesorter", f"{{bg_blu}}Moving directory '{os.path.basename(path_folder)}' from '{path_folder}' to '{new_path}'{{def}}")
        shutil.move(path_folder, new_path)

        

def organize_directory(path):
    for _ in path:
        if isinstance(_, str):
            _judge(_)
        elif isinstance(_, dict):
            value = _.values()
            organize_directory(value)
        elif isinstance(_, list):
            organize_directory(_)
        else:
            opr.print_from("Filesorter", f"{{bg_yel}}Skipping unknown type: {type(_)}{{def}}")
            

if __name__ == "__main__":
    #f = opr.input_from("Filesorter", "{blu}Enter the path to the directory you want to sort{def}")
    #f = r"C:\Users\Vaynes\Downloads\testfile.py"
    #f = r"C:\Users\Vaynes\Downloads"
    #dir = opr.enumerate_directory(f, 2, True)
    #organize_directory(dir)

    organize_by_rules(paths_and_rules)





"""

    

"""