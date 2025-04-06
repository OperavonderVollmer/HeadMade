from HeadMade import ruler
from HeadMade import sorter
from OperaPowerRelay import opr


DEBUG = False

def quickly() -> bool:
    
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
    ruler.DEBUG = False


    result = sorter.organize_by_rules(ruler.CONFIG)
    if result:
        opr.print_from("Filesorter - Quickly", "Successfully sorted files!")

    else:
        opr.print_from("Filesorter - Quickly", "Failed to sort files!")
    

    ruler.deinitialize()

    return result

if __name__ == "__main__":
    opr.wipe(False)
    ruler.initialize()
    ruler.DEBUG = DEBUG
    
    while True:
        try:
            decision = opr.input_from("Filesorter - Main", "📂 Edit Rules [1] | 🚀 Start Sorting [2] | 🚪 Exit [3]", 1)

            if decision == "1":
                opr.wipe(False)
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
