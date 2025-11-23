# test_eel_diag.py
import eel
import traceback
import os

UI = os.path.join(os.path.dirname(__file__), "www")
print("UI folder:", UI)

try:
    eel.init(UI)
    print("Eel initialized OK.")
except Exception as e:
    print("Eel.init() FAILED:", e)
    traceback.print_exc()

try:
    print("Calling eel.start() (blocking) — this should launch server or raise an error.")
    # use block=True so any exceptions surface in this process
    eel.start('index.html', host='localhost', port=8000, mode=None, block=True)
    print("eel.start() returned (server stopped).")
except Exception as e:
    print("eel.start() RAISED EXCEPTION:")
    traceback.print_exc()
