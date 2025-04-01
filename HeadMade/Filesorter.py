from OperaPowerRelay import opr
from abc import ABC, abstractmethod
import re
import os
import traceback


"""

    Rules look like this
    key : value
    regex expression : directory (should be absolute path to a directory)

"""

class iSorter:
    def __init__(self, path: str, depth: int, rules: dict[str, str]):
        self._path = path
        self._depth = depth
        self._dir = opr.enumerate_directory(self._path, self._depth, True)
        self._rules = rules



    def sort(self):




        pass

criteria = [r".*\.(mp4|mp3|png)$"]



def move_files(path: str, rules: dict) -> bool:

    try:
        for rule, directory in rules.items():
            if re.match(rule, path):
                opr.print_from("Filesorter", f"{{bg_gre}}File {os.path.basename(path)} match found{{def}}\nPlacing file in {directory}")           
                os.rename(path, os.path.join(directory, os.path.basename(path)))
                return True

        opr.print_from("Filesorter", f"{{bg_blu}}File {os.path.basename(path)} does not match any rules{{def}}") 
        return True

    except Exception as e:
        opr.error_pretty(e, "Filesorter")
        return False

    
rules = {
    r".*\.(py)$": r"C:\Users\Vaynes\Desktop\Media"
} 

"""

    Dict
    path : [rule, new path]

"""





if __name__ == "__main__":
    test_path = opr.input_from("Filesorter", "{blu}Enter the path to the directory you want to sort{def}")
    cleaned_path = opr.clean_path(test_path)
    move_files(cleaned_path, rules)