import os
import random
from tkinter import *
from tkinter import filedialog
from pygame import mixer

# Initialize mixer
mixer.init()

# Root window
root = Tk()
root.title("🎵 Music Player")
root.geometry("500x500")
root.configure(bg="black")

# Variables
current_song_index = 0
songs_list = []
loop_song = False

# Functions
def load_songs():
    global songs_list
    folder = filedialog.askdirectory()
    if folder:
        songs_list = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")]
        playlist.delete(0, END)
        for song in songs_list:
            playlist.insert(END, os.path.basename(song))

def play_song():
    global current_song_index
    song = playlist.get(ACTIVE)
    if song:
        current_song_index = playlist.curselection()[0]
        song_path = songs_list[current_song_index]
        mixer.music.load(song_path)
        mixer.music.play()
        song_label.config(text=os.path.basename(song_path))

def pause_song():
    mixer.music.pause()

def resume_song():
    mixer.music.unpause()

def stop_song():
    mixer.music.stop()
    song_label.config(text="No Song Playing")

def next_song():
    global current_song_index
    if current_song_index + 1 < len(songs_list):
        current_song_index += 1
        playlist.select_clear(0, END)
        playlist.selection_set(current_song_index)
        playlist.activate(current_song_index)
        play_song()

def prev_song():
    global current_song_index
    if current_song_index > 0:
        current_song_index -= 1
        playlist.select_clear(0, END)
        playlist.selection_set(current_song_index)
        playlist.activate(current_song_index)
        play_song()

def set_volume(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)

def toggle_loop():
    global loop_song
    loop_song = not loop_song
    loop_button.config(bg="green" if loop_song else "gray")

def shuffle_song():
    global current_song_index
    current_song_index = random.randint(0, len(songs_list) - 1)
    playlist.select_clear(0, END)
    playlist.selection_set(current_song_index)
    playlist.activate(current_song_index)
    play_song()

# Volume Label
volume_label = Label(root, text="Volume", bg="black", fg="white")
volume_label.pack()

# Volume Slider
volume_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_volume, bg="gray20", fg="white")
volume_slider.set(70)
volume_slider.pack()

# Song name display
song_label = Label(root, text="No Song Playing", bg="black", fg="white", font=("Arial", 14))
song_label.pack(pady=10)

# Playlist Listbox
playlist = Listbox(root, bg="gray20", fg="white", width=60, selectbackground="lightblue")
playlist.pack(pady=10)

# Buttons
btn_frame = Frame(root, bg="black")
btn_frame.pack(pady=10)

Button(btn_frame, text="⏯ Load", command=load_songs, width=8, bg="blue", fg="white").grid(row=0, column=0, padx=5)
Button(btn_frame, text="▶ Play", command=play_song, width=8, bg="green", fg="white").grid(row=0, column=1, padx=5)
Button(btn_frame, text="⏸ Pause", command=pause_song, width=8, bg="orange", fg="black").grid(row=0, column=2, padx=5)
Button(btn_frame, text="⏹ Stop", command=stop_song, width=8, bg="red", fg="white").grid(row=0, column=3, padx=5)
Button(btn_frame, text="⏵ Next", command=next_song, width=8, bg="purple", fg="white").grid(row=1, column=0, padx=5, pady=5)
Button(btn_frame, text="⏴ Prev", command=prev_song, width=8, bg="purple", fg="white").grid(row=1, column=1, padx=5)
Button(btn_frame, text="🔀 Shuffle", command=shuffle_song, width=8, bg="brown", fg="white").grid(row=1, column=2, padx=5)
loop_button = Button(btn_frame, text="🔁 Loop", command=toggle_loop, width=8, bg="gray", fg="white")
loop_button.grid(row=1, column=3, padx=5)

root.mainloop()
