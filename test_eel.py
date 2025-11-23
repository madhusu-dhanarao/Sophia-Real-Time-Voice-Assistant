import eel

print("Initializing EEL...")

eel.init("www")

print("Starting EEL server...")
eel.start('index.html', host='localhost', port=8000)
