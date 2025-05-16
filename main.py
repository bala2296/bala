import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer

mixer.init()

root = Tk()
root.title("Music Player")
root.geometry("400x350")
root.configure(bg="black")

playlist = Listbox(root, bg="gray20", fg="white", width=50, selectbackground="lightblue")
playlist.pack(pady=20)

def load_songs():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        playlist.delete(0, END)
        for file in os.listdir(folder_selected):
            if file.endswith(".mp3"):
                playlist.insert(END, os.path.join(folder_selected, file))

def play_song():
    song = playlist.get(ACTIVE)
    if song:
        mixer.music.load(song)
        mixer.music.play()

def pause_song():
    mixer.music.pause()

def resume_song():
    mixer.music.unpause()

def stop_song():
    mixer.music.stop()

Button(root, text="Load Songs", command=load_songs, bg="blue", fg="white").pack(pady=5)
Button(root, text="Play", command=play_song, bg="green", fg="white").pack(pady=5)
Button(root, text="Pause", command=pause_song, bg="orange", fg="black").pack(pady=5)
Button(root, text="Resume", command=resume_song, bg="purple", fg="white").pack(pady=5)
Button(root, text="Stop", command=stop_song, bg="red", fg="white").pack(pady=5)

root.mainloop()
