from tkinter import *
import pygame
import os
import time
import tkinter.ttk as ttk
import tkinter.messagebox as tkm
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from mutagen.mp3 import MP3


class PlayList:
    def __init__(self, app):
        self.files_path = []
        self.song_names = []
        self.app = app
        self.song_box = Listbox(self.app, bg='#2c2c2c', fg='white', width=63, selectbackground='#ffba00',
                                selectforeground='#2c2c2c', font=('montserrat', 9, 'bold'))
        self.song_box.grid(row=0, column=0)

    def add_song(self, event):
        if event:
            song = filedialog.askopenfilename(initialdir="C:\Music", title='Choose A Song',
                                            filetypes=(('mp3 Files', '*.mp3'), ('wav Files', '*.wav')))
            directory = os.path.dirname(song)
            self.files_path.append(str(directory))
            os.chdir(directory)
            song_dir_split = os.path.split(song)
            song_only = song.split('/')[-1]
            self.song_names.append(song_only)
            self.song_box.insert(END, song_only)
        
    
    # Add Many Songs

    def add_many_songs(self, event):
        if event:
            songs=filedialog.askopenfilenames(initialdir="C:\Music", title='Choose A Song',filetypes=(('mp3 Files','*.mp3'),('wav Files','*.wav')))
            
            for b in songs:
                b=os.path.basename(b)
                self.song_names.append(b)
                self.song_box.insert(ANCHOR,b)

            for i in songs:
                i=os.path.dirname(i)  
                self.files_path.append(i)
    
    
    

    def remove_one_song(self):
        # Delete Selected Song
        self.song_box.delete(ANCHOR)
        # Delete Song Index From Set
        next_one = self.song_box.curselection()
        song_index = next_one[0]
        self.files_path.pop(song_index)
        self.song_names.pop(song_index)


class MusicPlayer:
    def __init__(self, app, playlist):
        self.playlist = playlist
        self.stopped = False
        self.paused = False
        self.app = app

        # Initialize Pygame
        pygame.mixer.init()

        # Controls Frame
        controls_frame = Frame(app)
        controls_frame.grid(row=1, column=0, pady=20)

        # Music Slider Frame
        music_slider_frame = LabelFrame(app)
        music_slider_frame.grid(row=2, column=0, pady=10, padx=10)

        # Volume Frame
        volume_frame = LabelFrame(app, text='Volume', bd=4, relief=GROOVE, font=('gilroy', 10, 'bold'))
        volume_frame.grid(row=3, column=0, padx=10)

        # Player Buttons
        self.back_btn = Button(controls_frame, text='Back', command=self.previous_song)
        self.forward_btn = Button(controls_frame, text='Forward', command=self.next_song)
        self.play_btn = Button(controls_frame, text='Play', command=self.play)
        self.pause_btn = Button(controls_frame, text='Pause', command=self.pause)
        self.stop_btn = Button(controls_frame, text='Stop', command=self.stop)

        self.back_btn.grid(row=0, column=0, padx=10)
        self.forward_btn.grid(row=0, column=1, padx=10)
        self.play_btn.grid(row=0, column=2, padx=10)
        self.pause_btn.grid(row=0, column=3, padx=10)
        self.stop_btn.grid(row=0, column=4, padx=10)

        # Menu Bar
        menu = Menu(app)
        app.config(menu=menu)

        # Song Menu
        songmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Add Songs", menu=songmenu)
        songmenu.add_command(label="Add One Song to Playlist", command=self.playlist.add_song(True), accelerator='[Ctrl+O]')
        songmenu.add_command(label="Add Many Songs to Playlist", command=lambda:self.playlist.add_many_songs(True),accelerator='[Ctrl+A]' ) 
        songmenu.add_separator()
        
        
        

        # Remove Songs Menu
        remove_songs_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Remove Songs", menu=remove_songs_menu)
        remove_songs_menu.add_command(label="Selected Song", command=self.playlist.remove_one_song)

        # Music Slider
        self.music_slider = ttk.Scale(music_slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=self.slide,
                                      length=600)
        self.music_slider.pack(pady=20, padx=20)

        # Volume Slider
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=self.volume,
                                       length=200)
        self.volume_slider.grid(row=0, column=0, padx=15)

    

    def play(self):
        self.stopped = False
        selected_song_path = self.playlist.song_box.curselection()
        song_index = selected_song_path[0]
        song_path = self.playlist.files_path[song_index]
        song_only = self.playlist.song_box.get(ACTIVE)
        song = song_path + chr(92) + song_only
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

    def stop(self):

        # Stop Song
        pygame.mixer.music.stop()
        self.playlist.song_box.selection_clear(ACTIVE)

        # Set Stop value to True
        self.stopped = True

    def pause(self):
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def next_song(self):
        
        next_one = self.playlist.song_box.curselection()
        song_index = (next_one[0])
        next_one = next_one[0] + 1
        song = self.playlist.song_box.get(next_one)
        song_next = self.playlist.files_path[next_one] + chr(92) + song
        pygame.mixer.music.load(song_next)
        pygame.mixer.music.play(loops=0)
        self.playlist.song_box.selection_clear(0, END)
        self.playlist.song_box.activate(next_one)
        self.playlist.song_box.selection_set(next_one, last=None)

    def previous_song(self):
        
        next_one = self.playlist.song_box.curselection()
        song_index = (next_one[0])
        next_one = next_one[0] - 1
        song = self.playlist.song_box.get(next_one)
        song_next = self.playlist.files_path[next_one] + chr(92) + song
        pygame.mixer.music.load(song_next)
        pygame.mixer.music.play(loops=0)
        self.playlist.song_box.selection_clear(0, END)
        self.playlist.song_box.activate(next_one)
        self.playlist.song_box.selection_set(next_one, last=None)

    def volume(self, x):
        pygame.mixer.music.set_volume(self.volume_slider.get())

    def slide(self, x):
        selected_song = self.playlist.song_box.get(ACTIVE)
        selected_song_path = self.playlist.song_box.curselection()
        song_index = (selected_song_path[0])
        song_path = self.playlist.files_path[song_index]
        song_only = (selected_song)
        song = song_path + chr(92) + song_only
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0, start=int(self.music_slider.get()))
        
    

app = Tk()
app.title("Music Player App")
app.geometry('700x650+450+100')
app.resizable(False, False)
app.iconbitmap('Images\Papirus-Team-Papirus-Apps-Multimedia-audio-player.ico')

playlist = PlayList(app)
music_player = MusicPlayer(app, playlist)

app.mainloop()
