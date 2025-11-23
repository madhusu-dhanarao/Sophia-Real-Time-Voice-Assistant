import os
import re
import sqlite3
import webbrowser
from playsound import playsound
import eel
import pywhatkit as kit

from engine.command import speak
from engine.config import ASSISTANT_NAME

conn = sqlite3.connect("sophia.db")
cursor = conn.cursor()


def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)


@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\click_sound.mp3"
    playsound(music_dir)


# ------------------------------
# OPEN COMMAND (APPS / WEBSITES)
# ------------------------------
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "").strip().lower()

    if query == "":
        speak("Please tell me what to open.")
        return

    try:
        # Search system command table
        cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
        result = cursor.fetchone()

        if result:
            speak("Opening " + query)
            os.startfile(result[0])
            return

        # Search website command table
        cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
        result = cursor.fetchone()

        if result:
            speak("Opening " + query)
            webbrowser.open(result[0])
            return

        # Try normally
        speak("Opening " + query)
        os.system(f'start {query}')

    except Exception as e:
        speak("Sorry, I couldn't open " + query)


# ------------------------------
# YOUTUBE PLAY FUNCTION
# ------------------------------
def PlayYoutube(query=""):
    """Safe YouTube function that works for:
       - 'open youtube'
       - 'play song on youtube'
       - 'play naruto music'
    """

    # 1. If user said "open youtube"
    if "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return

    # 2. Extract term: "play *something* on youtube"
    search_term = extract_yt_term(query)

    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
        return

    # 3. If they said "play song" etc
    if query.startswith("play"):
        term = query.replace("play", "").strip()
        if term:
            speak("Playing " + term + " on YouTube")
            kit.playonyt(term)
            return

    speak("Sorry, I didn't understand what to play on YouTube.")


# Extract play term
def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None
