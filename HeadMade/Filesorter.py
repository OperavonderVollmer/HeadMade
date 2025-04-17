from HeadMade import ruler
from HeadMade import sorter
from OperaPowerRelay import opr
import os


DEBUG = False

def quickly(path:str=None) -> bool:
    
    """
    Executes the file sorting process using predefined rules.

    This function initializes the file sorter, sets the debug mode to false,
    and invokes the sorting mechanism based on the configuration rules.
    It then deinitializes the file sorter and returns the success status of the operation.

    
    Note
    ----
    This is the proper way to use the file sorter using the module. Running this module directly would use the interface and prompt the user for input, which is probably not what you want. 

    If you want to set rules, use the ruler's filesorter_wizard() function. 


    Returns
    -------
    bool
        True if the files were successfully sorted, False otherwise.
    """

    ruler.initialize()
    ruler.DEBUG = DEBUG


    result = sorter.organize_by_rules(ruler.CONFIG)

    filepath = path or os.path.dirname(os.path.abspath(__file__))

    if filepath is not None:
        if result:
            opr.write_log("Filesorter - Quickly", filepath, "Headmade.log", "Successfully sorted files.", "SUCCESS")
        else:
            opr.write_log("Filesorter - Quickly", filepath, "Headmade.log", "Something went wrong while sorting files.", "FAILURE")
    ruler.deinitialize()

    return result

if __name__ == "__main__":
    opr.wipe(DEBUG)
    ruler.initialize()
    ruler.DEBUG = DEBUG
    
    while True:
        try:
            decision = opr.input_from("Filesorter - Main", "📂 Edit Rules [1] | 🚀 Start Sorting [2] | 🚪 Exit [3]", 1)

            if decision == "1":
                opr.wipe(DEBUG)
                ruler.filesorter_wizard()

            elif decision == "2":
                sorter.organize_by_rules(ruler.CONFIG)

            elif decision == "3":
                break

            else:
                opr.print_from("Filesorter - Main", "{bg_red}Invalid input{def}")

        except KeyboardInterrupt:
            break

        except Exception as e:
            opr.error_pretty(e, "Filesorter - Main")
            break

    ruler.deinitialize()
    opr.print_from("Filesorter - Main", "Exiting Filesorter...")
