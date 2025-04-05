import re
import os
from OperaPowerRelay import opr
import sys
import time
 

def initialize(filepath: str = "") -> None:
    global FILEPATH

    if not filepath:
        filepath = os.path.abspath(__file__)
    FILEPATH = filepath

    _load()

def deinitialize() -> None:
    os.system("cls")
    opr.print_from("Filesorter - Deinitialize", "Deinitializing Filesorter...")
    _save()

def _save() -> None:

    global CONFIG_NAME
    opr.save_json("Filesorter - Save", os.path.dirname(FILEPATH), CONFIG, filename=CONFIG_NAME)

def _load() -> None:
        
    global FILEPATH
    global CONFIG


    opr.print_from("Filesorter - Load", "Initializing Filesorter...")
    opr.print_from("Filesorter - Load", f"Saving config file: {FILEPATH}")
    CONFIG = {}
    CONFIG = opr.load_json("Filesorter - Load", os.path.dirname(FILEPATH), filename=CONFIG_NAME)


def _select(isFrom: str, message: str) -> str:
    
    os.system("cls")
    while True:
        opr.print_from(isFrom, message, after_return_count=1)
        for idx, path in enumerate(CONFIG.keys(), 1):
            opr.print_from(isFrom, f"[{idx}] 📂 {path}")

        path = opr.input_from(isFrom, "Enter your choice")

        try:

            path = list(CONFIG.keys())[int(path) - 1]
            break
        
        except (ValueError, IndexError):
            os.system("cls")
            opr.print_from(isFrom, f"{{bg_red}}Invalid input{{def}}")            
            continue

    return path

def _add() -> None:
    os.system("cls")
    while True:
        path = opr.input_from("Filesorter - Wizard | Add", "Include the directory or path to be sorted")
        path = opr.clean_path(path)
        if not os.path.exists(path):
            opr.print_from("Filesorter - Wizard | Add", f"{{bg_red}}Path {path} does not exist{{def}}")
            continue
        if os.path.isfile(path):
            path = os.path.dirname(path)
        _ = opr.input_from("Filesorter - Wizard | Add", f"{{bg_whi}}'{path}'{{def}} Is this correct? [y]")
        if _.lower().strip() == "y":
            break

    #path = repr(path)
    
    CONFIG[path] = []
    _save()

    _edit(path)


def _edit(path: str = "") -> None:
    if not path:
        path = _select("Filesorter - Wizard | Edit", "Select a path to edit")
    
    os.system("cls")
    
    while True:        
        opr.print_from("Filesorter - Wizard | Edit", f"✏️  Editing {path}", after_return_count=1)
        _display_rules(path)
        
        opr.print_from("Filesorter - Wizard | Edit", "Select editing option", 1)
        decision = opr.input_from("Filesorter - Wizard | Edit", "✏️  Edit Rule [1] | 📂 Edit Path [2] | 🚪 Exit [3]", 1)


        if decision == "1":
            _edit_rule(path)

        elif decision == "2":
            path = _edit_path(path)

        elif decision == "3":
            break

        else:
            opr.print_from("Filesorter - Wizard | Edit", "{bg_red}Invalid input{def}")

    _display()

def _edit_rule(path: str) -> None:
    os.system("cls")
    opr.print_from("Filesorter - Wizard | Edit Rule", f"Select which destination's rules you'd like to edit", after_return_count=1)
    _index_rules(path, "destination")

    current = CONFIG[path]
    while True:
        
        decision = opr.input_from("Filesorter - Wizard | Edit Rule", "Enter your choice", 1)
        try:
            index_of = int(decision) - 1
            destination = current[index_of][1]
            break

        except IndexError:
            opr.print_from("Filesorter - Wizard | Edit Rule", f"{{bg_red}}Invalid input{{def}}")
            continue

    while True:
        opr.print_from("Filesorter - Wizard | Edit Rule", f"Editing the rules for {destination}...")
        os.system("cls")
        _index_rules(path, "rule", destination)

        decision = opr.input_from("Filesorter - Wizard | Edit Rule", "✏️  Rewrite [1] | 🔀  Reorder [2] | ❌  Remove [3] | ⏪  Back [4]", 1)

        if decision == "1":
            _rewrite(path, destination)

        elif decision == "2":
            _reorder(path, destination)

        elif decision == "3":
            _impeach_rule(path, destination)

        elif decision == "4":
            break
        

def _edit_path(path: str) -> None:
    os.system("cls")

    global CONFIG

    while True:
        opr.print_from("Filesorter - Wizard | Edit Path", f"Select the new path you would like to monitor", after_return_count=1)
        new_path = opr.input_from("Filesorter - Wizard | Edit Path", "Enter your choice", 1)
        new_path = opr.clean_path(new_path)
        
        if not os.path.exists(new_path):
            opr.print_from("Filesorter - Wizard | Edit Path", f"{{bg_red}}Path {new_path} does not exist{{def}}")
            continue

        if os.path.isfile(new_path):
            new_path = os.path.dirname(new_path)
        confirm = opr.input_from("Filesorter - Wizard | Edit Path", f"{{bg_whi}}'{new_path}'{{def}} Is this correct? [y]")

        if confirm.lower().strip() == "y":
            break

    CONFIG[new_path] = CONFIG.pop(path)
    _save()
    time.sleep(0.5)
    _load()

    return new_path


def _retrieve_rules(path: str, set_destination: str) -> list:
    for r in CONFIG[path]:
        pattern, destination = r
        if destination == set_destination:
            return pattern.copy()
    
def _insert_rules(path: str, set_destination: str, rules: list) -> None:
    for path in CONFIG[path]:
        if path[1] == set_destination:
            path[0] = rules
    _save()

def _rewrite(path: str, destination: str) -> None:
    current = _retrieve_rules(path, destination)

    os.system("cls")

    opr.print_from("Filesorter - Index Rules", f"📌 User-written rules are likely **incompatible with rewriting tool** and must be rewritten manually")
    opr.print_from("Filesorter - Wizard | Rewrite", f"{{bg_red}}Please note that rewriting rules will overwrite existing rules{{def}}", after_return_count=1)

    for rule in current:
        opr.print_from("Filesorter - Wizard | Rewrite", f"🔽 {_readable_regex(rule)}")      

    decision = opr.input_from("Filesorter - Wizard | Rewrite", "Continue? [y]", 1)
    
    if decision.lower().strip() != "y":
        return

    creation_means = opr.input_from("Filesorter - Wizard | Rewrite", "Would you like to manually write a rule? [y]")


    os.system("cls")
    opr.print_from("Filesorter - Wizard | Rewrite", f"✏️  Rewriting rules for {destination}", after_return_count=1)

    if creation_means.lower().strip() == "y":
        rule = _write_manual_rule(destination)
        _insert_rules(path, destination, rule)
        return

    
    selected_rules = _select_rule_types()
    entered_patterns = _write_basic_rule(selected_rules)
    enforced_patterns = _process_patterns(entered_patterns)
    _insert_rules(path, destination, enforced_patterns)

    time.sleep(0.5)
    os.system("cls")


def _reorder(path: str, set_destination: str) -> None:
    
    current = _retrieve_rules(path, set_destination)    

    while True:

        os.system("cls")
        opr.print_from("Filesorter - Wizard | Reorder", f"Select a rule to reorder", after_return_count=1)

        for idx, rule in enumerate(current, 1):
            opr.print_from("Filesorter - Wizard | Reorder", f"🔽 [{idx}] {_readable_regex(rule)}")

        decision = opr.input_from("Filesorter - Wizard | Reorder", "Enter your choice. (Enter 'break' to exit)", 1)
        if decision.lower().strip() == "break":
            break
        try:
            index = int(decision) - 1
            if index > len(current) or index < 0:
                opr.print_from("Filesorter - Wizard | Reorder", f"{{bg_red}}Invalid input{{def}}")
                continue

        except (ValueError, IndexError):
            opr.print_from("Filesorter - Wizard | Reorder", f"{{bg_red}}Invalid input{{def}}")
            continue

        decision = opr.input_from("Filesorter - Wizard | Reorder", "Select the index you'd like to move the rule to", 1)
        try:
            new_index = int(decision) - 1
            if new_index >= len(current) or new_index < 0:
                opr.print_from("Filesorter - Wizard | Reorder", f"{{bg_red}}Invalid input{{def}}")
                continue

        except (ValueError, IndexError):
            opr.print_from("Filesorter - Wizard | Reorder", f"{{bg_red}}Invalid input{{def}}")
            continue

        current[index], current[new_index] = current[new_index], current[index]

    decision = opr.input_from("Filesorter - Wizard | Reorder", "Are you sure you want to reorder these rules? [y]")

    if decision.lower().strip() == "y":
        _insert_rules(path, set_destination, current)
        


def _impeach_rule(path: str, destination: str) -> None:
    
    os.system("cls")
    _display_rules(path)

    current = CONFIG[path]

    for rule, des in current:
        if des == destination:
            for r in rule:
                opr.print_from("Filesorter - Wizard | Impeach Rule", f"🔽 {_readable_regex(r)}")

    decision = opr.input_from("Filesorter - Wizard | Impeach Rule", "{bg_red}Are you sure you want to impeach these rules?{def} [y]", 2)

    if decision.lower().strip() != "y":
        return

    CONFIG[path] = [entry for entry in CONFIG[path] if entry[1] != destination]

    os.system("cls")

    _save()
    time.sleep(0.5)
    _load()

def _enforce_rule(path: str) -> tuple[str, str] | None:    

    os.system("cls")

    opr.print_from("Filesorter - Wizard | Enforce Rule", f"Enforce rule for directory '{os.path.basename(path)}'", after_return_count=1)

    des = opr.input_from("Filesorter - Wizard | Enforce Rule", "Enter the destination")

    if not os.path.exists(des):
        os.system("cls")
        opr.print_from("Filesorter - Wizard | Enforce Rule", f"{{bg_red}}'{des}' does not exist{{def}}")
        return
    
    des = opr.clean_path(des)

    destination = des

    creation_means = opr.input_from("Filesorter - Wizard | Enforce Rule", "Would you like to manually write a rule? [y]")
    if creation_means.lower().strip() == "y":
        rule = _write_manual_rule(destination)
        return rule, destination
    
    selected_rules = _select_rule_types()

    entered_patterns = _write_basic_rule(selected_rules)
    
    enforced_patterns = _process_patterns(entered_patterns)

    return enforced_patterns, destination



def _select_rule_types() -> list:
    rule_types = ["ends with", "starts with", "contains"]

    selected_rules = []
    while True:
        for idx, rule in enumerate(rule_types, 1):
            opr.print_from("Filesorter - Wizard | Select Rule Types", f"{{bg_whi}}[{idx}] {rule}{{def}}")

        decision = opr.input_from("Filesorter - Wizard | Select Rule Types", "Enter numbers separated by commas (e.g. 1, 2, 3) or all")

        if decision.lower().strip() == "all":
            selected_rules = rule_types
            break

        try:
            selected_rules = [rule_types[int(x) - 1] for x in decision.split(",")]
            break
        except IndexError:
            opr.print_from("Filesorter - Wizard | Enforce Rule", f"{{bg_red}}Invalid input{{def}}")
            continue
        except ValueError:
            opr.print_from("Filesorter - Wizard | Enforce Rule", f"{{bg_red}}Invalid input{{def}}")
            continue

    return selected_rules


def _write_manual_rule() -> str:
    
    rule = opr.input_from("Filesorter - Wizard | Manual Rule", "Enter the rule")
    pattern = re.compile(rule)
    return pattern


def _write_basic_rule(selected_rules: list) -> dict[str, list]:
    entered_patterns = {
        "starts with": [],
        "contains": [],
        "ends with": []
    }


    for rule in selected_rules:

        pattern = []
        os.system("cls")
        opr.print_from("Filesorter - Wizard | Basic Rule", f"Enforcing rule: {{bg_mag}}{rule}{{def}}")

        while True:
            p = opr.input_from("Filesorter - Wizard | Basic Rule", "Enter the pattern (What string of text to look out for. Please note that this is case sensitive)")

            safep, logmessage = opr.sanitize_text(p)

            if not safep:
                opr.print_from("Filesorter - Wizard | Basic Rule", f"{{bg_red}}You have entered an illegal pattern, please try again. {logmessage}{{def}}")
                continue

            pattern.append(p)

            _ = opr.input_from("Filesorter - Wizard | Basic Rule", "Add another pattern? [y]")
            if not _.lower().strip() == "y":
                break
            os.system("cls")
        entered_patterns[rule] = pattern


    return entered_patterns

def _process_patterns(patterns: dict) -> list:
    end_starts_with, end_contains, end_ends_with = "", "", ""

    if patterns["starts with"]:
        starts_with = "|".join(patterns["starts with"])
        end_starts_with += f"^(?:{starts_with})"

    if patterns["contains"]:
        contains = " | ".join(patterns["contains"])
        end_contains +=  f"(?:{contains})"

    if patterns["ends with"]:
        ends_with = "|".join(patterns["ends with"])
        end_ends_with += f"(?:{ends_with})$"

    enforced_patterns = [end_starts_with, end_contains, end_ends_with]

    finished_pattern = [p for p in enforced_patterns if p]

    return finished_pattern


def _remove(path: str = "") -> None:
    if not path:
        path = _select("Filesorter - Wizard | Remove", "Select a path to remove")

    os.system("cls")
    decision = opr.input_from("Filesorter - Wizard | Remove", f"{{bg_red}}'{path}' Are you sure you want to remove this path? [y]{{def}}")
    if decision.lower().strip() != "y":
        return
    
    del CONFIG[path]
    _save()

    _display()


import re

def _readable_regex(pattern: str) -> str:
    try:
        pattern = re.sub(r"\(\?:", "(", pattern)  

        if pattern.startswith("^"):
            match = re.match(r"^\^(\(.*\)|\w+)", pattern) 
            newPattern = f"Begins with {match.group(1).strip('()')}" if match else f"Begins with {pattern[1:]}"

        elif pattern.endswith("$"):
            match = re.match(r"(\(.*\)|\w+)\$$", pattern) 
            newPattern = f"Ends with {match.group(1).strip('()')}" if match else f"Ends with {pattern[:-1]}"

        elif "(?=" in pattern:
            matches = re.findall(r"\(\?=\.(\*?\w+)\)", pattern)  
            if matches:
                newPattern = f"Contains {' and '.join(matches)}"
            else:
                newPattern = f"Contains {pattern}"  

        else:
            match = re.match(r"\(?(.+?)\)?$", pattern)  
            newPattern = f"Contains {match.group(1)}" if match else f"Contains {pattern}"

        newPattern = newPattern.replace("|", " or ")
        newPattern = newPattern.replace("\.", ".")
        newPattern = newPattern.replace(".*", "")
        newPattern = newPattern.replace("?", "one ")
        newPattern = newPattern.replace("(", "")
        newPattern = newPattern.replace(")", "")
        
        return newPattern

    except TypeError as e:
        opr.error_pretty(e, "Filesorter - Readable Regex", "An error occurred while trying to convert the regex to a readable format. Please try again" + pattern)



def _display_rules(path: str, enum: str = "destination") -> None:
    if not any(CONFIG[path]):
        opr.print_from("Filesorter - Display Rules", f" ├ ❌ No sorting rules found for this folder.")
        return
        
    for r in CONFIG[path]:
        rule, destination = r

        opr.print_from("Filesorter - Display Rules", f" ├ {len(rule)} rule(s) -> {destination}")
        
def _index_rules(path: str, enum: str, set_destination: str = "") -> None:
    if not any(CONFIG[path]):
        opr.print_from("Filesorter - Index Rules", f" ├ ❌ No sorting rules found for this folder.")
        return
    
    if enum == "destination":
        for index, r in enumerate(CONFIG[path]):
            pattern, destination = r
            opr.print_from("Filesorter - Index Rules", f" ├ [{index + 1}] {destination}")
    
    elif enum == "rule":
        for r in CONFIG[path]:
            pattern, destination = r
            if destination == set_destination:
                opr.print_from("Filesorter - Index Rules", f"📌 Rules are processed **top-to-bottom** (higher = higher priority)")

                opr.print_from("Filesorter - Index Rules", f" ├ {len(pattern)} rule(s) -> {destination}")
                for index, p in enumerate(pattern):
                    opr.print_from("Filesorter - Index Rules", f" ├ 🔽  [{index + 1}] {_readable_regex(p)} ")

def _display() -> None:
    global CONFIG

    opr.print_from("Filesorter - Display Rules", "Monitored Folders and their rules")

    if any(CONFIG.keys()):
        for path in CONFIG.keys():
            opr.print_from("Filesorter - Display Rules", f"📂 **{os.path.basename(path)}**", 1)
            _display_rules(path)

    else:        
        opr.print_from("Filesorter - Display Rules", "{bg_red}No paths found{def}")

def filesorter_wizard() -> None:
    try:
        while True:
            _display()
            decision = opr.input_from("Filesorter - Wizard", "➕ Add Path [1] | ✏️  Edit Path [2] | 🗑️  Remove Path [3] | 🚪 Exit [4]", 1)

            if decision == "1":
                _add()
            elif decision == "2":
                _edit()
            elif decision == "3":
                _remove()
            elif decision == "4":
                break
            else:
                os.system("cls")
                opr.print_from("Filesorter - Wizard", "{bg_red}Invalid input{def}")
    
    except KeyboardInterrupt:
        pass

FILEPATH = ""
CONFIG: dict[str, list[tuple[list, str]]] = {}
CONFIG_NAME = "config_headmade_filesorter.json"


if __name__ == "__main__":


    os.system("cls")
    opr.print_from("Filesorter - Main", "Starting Filesorter (Ctrl+C to exit)...")
    
    initialize()
    filesorter_wizard()
    deinitialize()
    sys.exit(0)
