from tkinter import *
from tkinter import filedialog
import os
from pygame import mixer
from mutagen.mp3 import MP3
import threading
import time

mixer.init()
root = Tk()
root.title("Advanced Music Player")
root.geometry("500x500")
root.configure(bg="black")

playlist = Listbox(root, bg="gray20", fg="white", width=60, selectbackground="lightblue")
playlist.pack(pady=20)

songs_list = []
current_index = 0
is_paused = False

current_label = Label(root, text="No song playing", bg="black", fg="white")
current_label.pack()

duration_label = Label(root, text="00:00 / 00:00", bg="black", fg="white")
duration_label.pack()

seek_bar = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=400, bg="black", fg="white")
seek_bar.pack()

volume_scale = Scale(root, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, label="Volume", fg="white", bg="black")
volume_scale.set(0.5)
volume_scale.pack()
mixer.music.set_volume(0.5)

def set_volume(val):
    mixer.music.set_volume(float(val))

volume_scale.config(command=set_volume)

def load_songs():
    global songs_list
    folder = filedialog.askdirectory()
    if folder:
        playlist.delete(0, END)
        songs_list = []
        for file in os.listdir(folder):
            if file.endswith(".mp3"):
                full_path = os.path.join(folder, file)
                songs_list.append(full_path)
                playlist.insert(END, os.path.basename(full_path))

def play_song():
    global current_index, is_paused
    if playlist.curselection():
        current_index = playlist.curselection()[0]
    song_path = songs_list[current_index]
    mixer.music.load(song_path)
    mixer.music.play()
    current_label.config(text="Now Playing: " + os.path.basename(song_path))
    is_paused = False
    update_duration()
    auto_next_song()

def pause_song():
    global is_paused
    mixer.music.pause()
    is_paused = True

def resume_song():
    global is_paused
    mixer.music.unpause()
    is_paused = False

def stop_song():
    mixer.music.stop()
    current_label.config(text="Stopped")
    duration_label.config(text="00:00 / 00:00")

def next_song():
    global current_index
    current_index = (current_index + 1) % len(songs_list)
    playlist.selection_clear(0, END)
    playlist.selection_set(current_index)
    play_song()

def update_duration():
    def run():
        while mixer.music.get_busy():
            if not is_paused:
                song = MP3(songs_list[current_index])
                total = int(song.info.length)
                current = mixer.music.get_pos() // 1000
                current_time = time.strftime('%M:%S', time.gmtime(current))
                total_time = time.strftime('%M:%S', time.gmtime(total))
                duration_label.config(text=f"{current_time} / {total_time}")
                seek_bar.config(to=total, value=current)
                time.sleep(1)
    threading.Thread(target=run, daemon=True).start()

def seek(val):
    pos = int(val)
    mixer.music.play(start=pos)

seek_bar.config(command=seek)

def auto_next_song():
    def check():
        while True:
            if not mixer.music.get_busy() and not is_paused:
                time.sleep(1)
                next_song()
                break
            time.sleep(1)
    threading.Thread(target=check, daemon=True).start()

Button(root, text="Load Songs", command=load_songs, bg="blue", fg="white").pack(pady=5)
Button(root, text="Play", command=play_song, bg="green", fg="white").pack(pady=5)
Button(root, text="Pause", command=pause_song, bg="orange", fg="black").pack(pady=5)
Button(root, text="Resume", command=resume_song, bg="purple", fg="white").pack(pady=5)
Button(root, text="Stop", command=stop_song, bg="red", fg="white").pack(pady=5)
Button(root, text="Next", command=next_song, bg="darkgreen", fg="white").pack(pady=5)

root.mainloop()