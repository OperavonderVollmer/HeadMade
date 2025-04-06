from OperaPowerRelay import opr
from HeadMade import Filesorter
import os
import datetime
import threading
import time
from HeadMade import trayicon
import sys


FILEPATH = ""
CONFIG = {}
TIME_MODE = ""
TIME_FRAME = ""
CONFIG_NAME = "config_headmade.json"

HEADLESS = sys.argv[1] if len(sys.argv) > 1 else "No"

FILESORTER_THREAD = None
WIZARD_THREAD = None    

STOP_SIGNAL = threading.Event()

def setup(mode: str = "", frame : str = "") -> None:
    """
    Sets up the time mode and frame for the Filesorter.

    Parameters
    ----------
    mode : str, optional
        The time mode for the Filesorter. If not provided, the user will be prompted to select one.
    frame : str, optional
        The time frame for the Filesorter. If not provided, the user will be prompted to enter one.

    Returns
    -------
    None

    """
    
    global TIME_MODE
    global TIME_FRAME
    global CONFIG
    global CONFIG_NAME

    if not mode:
        _ = _get_time_mode()
        if _:
            mode = _
            TIME_MODE = mode
        else:
            opr.print_from("Headmade - Time Mode", "{bg_red}Something went wrong{def}")
            return 

    if not frame:
        _ = _get_time_frame() 
        if _:
            frame = _
            TIME_FRAME = frame

        else:
            opr.print_from("Headmade - Time Frame", "{bg_red}Something went wrong{def}")
            return 
        

    CONFIG["time_mode"] = TIME_MODE
    CONFIG["time_frame"] = TIME_FRAME
    opr.print_from("Headmade - Time Mode", f"Time mode set to: {TIME_MODE}")
    opr.print_from("Headmade - Time Frame", f"Time frame set to: {TIME_FRAME}")

    opr.save_json("Headmade - Save", os.path.dirname(FILEPATH), CONFIG, filename=CONFIG_NAME)
    

def _get_time_mode(mode: str = "") -> str:
    
    while True:

        opr.wipe()
        mode = opr.input_from("Headmade - Time Mode", "Select time mode (Interval [1] | Schedule [2]) ", 1)

        if mode == "1":
            return "Interval"
        elif mode == "2":
            return "Schedule"
        else:
            opr.print_from("Headmade - Time Mode", "{bg_red}Invalid input{def}")
        

def _get_time_frame() -> str | None:
    global TIME_MODE   
    

    if not TIME_MODE:
        opr.wipe()
        opr.print_from("Headmade - Time Frame", "{bg_red}Please set time mode first{def}")
        return None 

    while True:

        opr.wipe()

        while True:
            opr.print_from("Headmade - Time Frame", f"Select time frame for {TIME_MODE} mode")
            input_time = opr.input_from("Headmade - Time Frame", "Enter time in HH:MM:SS format (Military)", 1)

            if not input_time:
                opr.print_from("Headmade - Time Frame", "{bg_red}Invalid input{def}")
                continue

            break

        if TIME_MODE == "Interval":
            frame = _get_time_frame_interval(input_time)

        elif TIME_MODE == "Schedule":
            frame = input_time

        if frame:
            return frame
        else:
            opr.print_from("Headmade - Time Frame", "{bg_red}Invalid input{def}")


def _get_time_frame_interval(input_time: str) -> str | None:

    if "." in input_time:
        input_time = input_time.split(".")[0]

    arrayd = input_time.split(":")

    total_seconds = 0
    level = 1

    for i in arrayd[::-1]:
        total_seconds = int(total_seconds) + int(i) * level
        level *= 60
    
    return str(total_seconds)


def _get_time_frame_schedule() -> str | None:
    global TIME_FRAME

    current_time = datetime.datetime.now().time()
    target_time = datetime.datetime.strptime(TIME_FRAME, "%H:%M:%S").time()


    ct = int(_get_time_frame_interval(str(current_time)))
    tt = int(_get_time_frame_interval(str(target_time)))

    delta = tt - ct

    if delta == 0:
        delta = _get_time_frame_interval("23:59:59")

    return str(delta)

def _filesorter_thread() -> None:
    global TIME_MODE
    global TIME_FRAME

    if not TIME_MODE or not TIME_FRAME:
        opr.print_from("Headmade - Filesorter", "{bg_red}Please set time mode and time frame first{def}")
        return
    
    first_run = True
    
    while not STOP_SIGNAL.is_set():    
        wait = 0
        if TIME_MODE == "Interval":
            wait = int(TIME_FRAME)

        elif TIME_MODE == "Schedule":
            wait = int(_get_time_frame_schedule())

        if first_run:        
            user_input = opr.input_timed("Headmade - Filesorter", f"Wait {opr.seconds_to_time(wait)} before starting file sorter. Would you like to start now?", 1, 10)
            if user_input and user_input == "y":
                wait = 0.1

        first_run = False

        opr.print_from("Headmade - Filesorter", f"Sleeping for {wait} seconds")
        time.sleep(wait)
        opr.print_from("Headmade - Filesorter", "Awake~! Starting file sorter...")
        
        if not Filesorter.quickly():
            opr.write_log("Headmade - Filesorter", os.path.dirname(FILEPATH), "Headmade.log", "Something went wrong", "ERROR")
            return

def start() -> None:
    """
    Starts the file sorter thread.

    This function starts the file sorter thread which will automatically sort your files according to the time mode and time frame set.

    Returns
    -------
    None
    """
    global FILESORTER_THREAD
    global STOP_SIGNAL

    STOP_SIGNAL.clear()
    FILESORTER_THREAD = threading.Thread(target=_filesorter_thread, daemon=True)
    FILESORTER_THREAD.start()

def stop() -> None:
    """
    Stops the file sorter thread.

    This function stops the file sorter thread and does not affect the Filesorter module directly.

    Returns
    -------
    None
    """
    global STOP_SIGNAL
    global FILESORTER_THREAD

    STOP_SIGNAL.set()

def initialize(filepath: str = "") -> None:
    global FILEPATH
    global CONFIG
    global TIME_MODE
    global TIME_FRAME

    if not filepath:
        filepath = os.path.abspath(__file__)
    FILEPATH = filepath

    CONFIG = opr.load_json("Headmade - Load", os.path.dirname(FILEPATH), filename=CONFIG_NAME)

    TIME_MODE = CONFIG.get("time_mode", None)
    TIME_FRAME = CONFIG.get("time_frame", None)

def deinitialize() -> None:
    global CONFIG_NAME
    global CONFIG

    opr.save_json("Headmade - Save", os.path.dirname(FILEPATH), CONFIG, filename=CONFIG_NAME)

def headmade_wizard() -> None:
    global STOP_SIGNAL

    while not STOP_SIGNAL.is_set():
        try:
            opr.list_choices([
                "📂 Start Filesorter",
                "⏰ Set Time Mode",
                "⚙️ Configure Filesorter",
                "🚪 Exit"            
            ], "Welcome to Headmade", 1)

            if not TIME_MODE or not TIME_FRAME:
                opr.print_from("Headmade - Main", "{bg_red}Please set time mode and time frame first{def}", 1)
            else:
                opr.print_from("Headmade - Main", f"Current Time Mode: {TIME_MODE}", 1)
                opr.print_from("Headmade - Main", f"Current Time Frame: {TIME_FRAME}")

            decision = opr.input_from("Headmade - Main", "Enter your choice", 1)

            if decision == "1":
                sort_now = opr.input_from("Headmade - Main", "Would you like to sort now? [y]", 1)
                if sort_now == "y":
                    Filesorter.quickly()
                start()

            elif decision == "2":
                setup()

            elif decision == "3":
                opr.wipe()
                Filesorter.ruler.filesorter_wizard()

            elif decision == "4":
                stop()
                break

            else:
                opr.print_from("Headmade - Main", "{bg_red}Invalid input{def}")

            opr.wipe()

        except (KeyboardInterrupt, EOFError):
            break

        except Exception as e:
            opr.error_pretty(e, "Headmade - Main")
            break

    stop()


def direct_run() -> None:
    """
    Runs the Headmade application directly.

    This function initializes the Headmade configuration and starts the file sorter thread.
    It then enters a loop where it waits for user input to sort files now, set the time mode, configure the file sorter, or exit the application.
    If the user chooses to exit, the file sorter thread is stopped and the configuration is saved.

    Returns
    -------
    None
    """
    
    opr.wipe()
    initialize()
    global TIME_MODE
    global TIME_FRAME
    global STOP_SIGNAL

    Filesorter.ruler.FILEPATH = FILEPATH

    if HEADLESS == "HEADLESS":
        start()

    else:

        WIZARD_THREAD = threading.Thread(target=headmade_wizard, daemon=True)
        WIZARD_THREAD.start()

    try:
        STOP_SIGNAL.wait()
    except (KeyboardInterrupt, EOFError):
        pass

    stop()
    deinitialize()
    opr.wipe()
    opr.print_from("Headmade - Main", "Goodbye!")

if __name__ == "__main__":


    if HEADLESS:
        print(HEADLESS)

    trayicon.start_icon(stop)
    direct_run()

    trayicon.stop_icon()