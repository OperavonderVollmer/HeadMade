from OperaPowerRelay import opr
from abc import ABC, abstractmethod
import re
import os
import traceback
import shutil
from datetime import date

def organize_by_rules(path_and_rules: dict[str, list[tuple[list, str]]]) -> bool:
    global MOVED_FOLDERS
    MOVED_FOLDERS = set()

    if not any(path_and_rules.keys()):
        opr.wipe()
        opr.print_from("Filesorter - Organize", "{bg_red}No paths found{def}")
        return False

    for path in path_and_rules.keys():
        if not os.path.exists(path):
            opr.print_from("Filesorter - Organize", f"{{bg_red}}Path {path} does not exist{{def}}")
            return False
        
        opr.print_from("Filesorter - Organize", f"{{bg_whi}}Organizing {path}{{def}}")
        _judicial_court(path, path_and_rules[path])

    return True

def _judicial_court(path, rule_destination: list[tuple[list, str]]) -> None:
    

    dir = opr.enumerate_directory(path, 10, True)
    _due_process(dir, rule_destination, path)
    

def _due_process(dir: list[str, dict[str, list]], rule_destination: list[tuple[list, str]], previous_path: str) -> None:
    for _ in dir:
        if isinstance(_, str):
            #judge(crime=rule, defendant=_, scene=previous_path, jail=destination)
            _courtroom(rule_destination, _, previous_path)

        elif isinstance(_, dict):
            for sublist in _.values():
                _due_process(dir=sublist, rule_destination=rule_destination, previous_path=previous_path)
        else:
            opr.print_from("Filesorter - Due Process", f"{{bg_yel}}Skipping unknown type: {type(_)}{{def}}")


def _courtroom(rule_destination: list[tuple[list, str]], defendent: str, previous_path: str) -> None:

    for rules, destination in rule_destination:
        for rule in rules:
            judge(crime=rule, defendant=defendent, scene=previous_path, jail=destination)



def judge(crime: str, defendant: str, scene: str, jail: str) -> bool:
    global MOVED_FOLDERS


    if re.search(crime, os.path.basename(defendant)):
        opr.print_from("Filesorter - Judge", f"{{bg_gre}}{os.path.basename(defendant)} matches rule {crime}{{def}}")
        opr.print_from("Filesorter - Judge", f"{{bg_yel}}Old path: {defendant}{{def}}")
        
        rel_path = os.path.relpath(defendant, scene)

        opr.print_from("Filesorter - Judge", f"{{bg_yel}}Relative path: {rel_path}{{def}}")

    
        if not os.path.exists(jail):
            os.makedirs(jail, exist_ok=True)

        try:
            # checks if the file is inside the directory under watch and moves it exclusively
            if os.path.dirname(defendant) == scene:
                opr.print_from("Filesorter - Judge", f"{{bg_blu}}Moving '{os.path.basename(defendant)}' from '{os.path.dirname(defendant)}' to '{jail}'{{def}}")

                if os.path.exists(os.path.join(jail, os.path.basename(defendant))):

                    today = date.today().strftime("%Y-%m-%d")
                    base, ext = os.path.splitext(os.path.basename(defendant))
                    renamed = f"{base}_{today}{ext}"
                    duplicate = os.path.join(os.path.dirname(defendant), renamed)

                    os.rename(defendant, duplicate)
                    defendant = duplicate

    #NOTE: THIS HASN'T BEEN TESTED YET
                    
                shutil.move(defendant, jail)
                return

            # if it isn't gets the parent directory of the file under the director under watch and moves that
            path_folder = defendant
            while True:
                e = os.path.dirname(path_folder)
                if e == scene:
                    break
                path_folder = e
            
            if path_folder in MOVED_FOLDERS:
                opr.print_from("Filesorter - Judge", f"{{cya}}Directory '{os.path.basename(path_folder)}' has already been moved{{def}}")
                return

            MOVED_FOLDERS.add(path_folder)

            new_path= os.path.join(jail, os.path.basename(path_folder))
            opr.print_from("Filesorter - Judge", f"{{bg_blu}}Moving directory '{os.path.basename(path_folder)}' from '{path_folder}' to '{new_path}'{{def}}")
            shutil.move(path_folder, new_path)

            return True
        
        except FileNotFoundError as e:
            opr.error_pretty(e, "Filesorter - Judge", f"{{bg_red}}{defendant} has already been moved or does not exists{{def}}")

        except PermissionError as e:
            opr.error_pretty(e, "Filesorter - Judge", f"{{bg_red}}Permission error while moving {defendant}: {e}{{def}}")

        except Exception as e:
            opr.error_pretty(e, "Filesorter - Judge", f"{{bg_red}}An unexpected error occurred while moving {defendant}: {e}{{def}}")

    return False

def organize_directory(path):
    for _ in path:
        if isinstance(_, str):
            judge(_)
        elif isinstance(_, dict):
            value = _.values()
            organize_directory(value)
        elif isinstance(_, list):
            organize_directory(_)
        else:
            opr.print_from("Filesorter", f"{{bg_yel}}Skipping unknown type: {type(_)}{{def}}")
            

MOVED_FOLDERS = set()

if __name__ == "__main__":
    pass