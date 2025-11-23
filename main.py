import os
import sys
import time
import threading
import eel

# --------------------------------------------------
# FIX: Correct /www path
# --------------------------------------------------
UI_FOLDER = os.path.join(os.path.dirname(__file__), "www")
eel.init(UI_FOLDER)

print("[INFO] UI folder loaded from:", UI_FOLDER)

# --------------------------------------------------
# BROWSER FIX (forces Chrome)
# --------------------------------------------------
try:
    eel.browsers.set_path("chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
except:
    pass

# --------------------------------------------------
# START EEL SERVER (Thread-friendly)
# --------------------------------------------------
def start_eel_server():
    print(">>> Starting EEL Web Server...")

    try:
        eel.start(
            "index.html",
            mode="chrome",
            host="localhost",
            port=8000,
            block=False    # IMPORTANT FIX
        )
        print(">>> UI running at http://localhost:8000/")
    except Exception as e:
        print("[ERROR] EEL failed:", e)

# --------------------------------------------------
# IMPORT ENGINE
# --------------------------------------------------
from engine.features import PlayYoutube, openCommand, playAssistantSound
from engine.command import takeCommand, speak

# --------------------------------------------------
# VOICE LOOP
# --------------------------------------------------
def voice_loop():
    speak("Assistant is now online.")

    while True:
        try:
            query = takeCommand()
            if not query:
                continue

            query = query.lower().strip()
            print("[USER]:", query)

            if query in ["stop", "exit", "quit"]:
                speak("Shutting down.")
                sys.exit()

            elif query in ["hi", "hello"]:
                speak("Hello!")

          
            elif "open google" in query:
                speak("Opening Google...")
                openCommand("open google")

            elif "youtube" in query or query.startswith("play"):
                PlayYoutube(query)

            elif query.startswith("open "):
                openCommand(query)

            else:
                openCommand(query)

        except Exception as e:
            print("[ERROR]", e)
            time.sleep(0.2)

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":

    try:
        playAssistantSound()
    except:
        pass

    # Start UI server thread
    ui_thread = threading.Thread(target=start_eel_server)
    ui_thread.daemon = True
    ui_thread.start()

    # Give time for UI server to fully start
    time.sleep(2)

    # Start voice assistant
    voice_loop()
