import threading
import time
import eel

eel.init("www")

def start_ui():
    print("UI THREAD STARTED")
    try:
        eel.start("index.html", block=False)
    except Exception as e:
        print("EEL ERROR:", e)

print("Launching UI thread...")
ui_thread = threading.Thread(target=start_ui)
ui_thread.daemon = True
ui_thread.start()

time.sleep(5)
print("Main thread finished waiting.")
