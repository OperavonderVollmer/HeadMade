from PIL import Image
from OperaPowerRelay import opr
import pystray
import os
import threading
import time
import sys

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "HeadMade.ico")
ICON = Image.open(PATH)
STOP_SIGNAL = threading.Event()
ICON_THREAD = None
STOP: callable = None

def stop_icon() -> None:
    global STOP_SIGNAL
    global STOP

    STOP_SIGNAL.set()
    time.sleep(0.5)
    STOP()


def icon_thread() -> None:
    global ICON

    
    i = pystray.Icon("HeadMade", ICON, "HeadMade", menu=pystray.Menu(
        pystray.MenuItem("Exit", stop_icon)
    ))

    opr.write_log("Headmade - Trayicon", os.path.abspath(__file__), "headmade_icon.log", "Starting trayicon thread...", "INFO")


    i.run_detached()


    while not STOP_SIGNAL.is_set():
        time.sleep(1)


    opr.write_log("Headmade - Trayicon", os.path.abspath(__file__), "headmade_icon.log", "Stopping trayicon thread...", "INFO")
    i.stop()

def start_icon(callback: callable) -> None:
    global ICON_THREAD
    global STOP

    
    ICON_THREAD = threading.Thread(target=icon_thread, daemon=True)
    ICON_THREAD.start()

    STOP = callback