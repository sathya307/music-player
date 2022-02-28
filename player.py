import os
from tkinter.filedialog import askdirectory
import threading
import time

import pygame
import tkinter
from tkinter import *
from tkinter import ttk
from mutagen.id3 import ID3
from ttkthemes import themed_tk as tk


root = tk.ThemedTk()
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("radiance")         # Sets an available theme

root.minsize(300,300)
statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)


listofsongs = []
realnames = []

v = StringVar()
songlabel = Label(root, textvariable=v, width=35)

index = 0


def directorychooser():
    directory = askdirectory()
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio['TIT2'].text[0])

            listofsongs.append(files)

    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    # pygame.mixer.music.play()


directorychooser()

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)


rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()



def updatelabel():
    global index
    global songname
    v.set(realnames[index])
    a = pygame.mixer.Sound(realnames)
    total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and pygame.mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1
    # return songname

def playsong(event):
    global paused
    pygame.mixer.music.play()
    statusbar['text'] = "Music Resumed"
    updatelabel()



def nextsong(event):
    global index
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    statusbar['text'] = "NEXT SONG "
    updatelabel()


def prevsong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    statusbar['text'] = "PREV SONG"
    updatelabel()


def stopsong(event):
    pygame.mixer.music.stop()
    statusbar['text'] = "Music Stopped"
    v.set("")
    # return songname
def pause_music():
    global paused
    paused = TRUE
    pygame.mixer.music.pause()
    statusbar['text'] = "Music Paused"

def set_vol(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        pygame.mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        pygame.mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)



label = Label(leftframe, text='Music Player')
label.pack()

listbox = Listbox(leftframe)
listbox.pack()

# listofsongs.reverse()
realnames.reverse()

for items in realnames:
    listbox.insert(0, items)

realnames.reverse()
# listofsongs.reverse()

bottomframe = Frame(rightframe)
bottomframe.pack()


playPhoto = PhotoImage(file='/Users/sathya/PycharmProjects/musicplayer/images/play.png')
playbutton = Button(middleframe, image=playPhoto)
playbutton.pack()

pausePhoto = PhotoImage(file='/Users/sathya/PycharmProjects/musicplayer/images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto)



nextbutton = Button(root, text='Next Song')
nextbutton.pack()

rewindPhoto = PhotoImage(file='/Users/sathya/PycharmProjects/musicplayer/images/rewind.png')
previousbutton = Button(bottomframe, image=rewindPhoto)
previousbutton.pack()

stopPhoto = PhotoImage(file='/Users/sathya/PycharmProjects/musicplayer/images/stop.png')
stopbutton = Button(middleframe, image=stopPhoto)
stopbutton.pack()



mutePhoto = PhotoImage(file='/Users/sathya/PycharmProjects/musicplayer/images/mute.png')
volumePhoto = PhotoImage(file='/Users/sathya/PycharmProjects/musicplayer/images//volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL)
scale.set(70)  # implement the default value of scale when music player starts
pygame.mixer.music.set_volume(0.7)



playbutton.bind("<Button-1>",playsong)
nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", prevsong)
stopbutton.bind("<Button-1>", stopsong)
pauseBtn.bind("<Button-1>",pause_music)
volumeBtn.bind("<Button-1>",mute_music)
scale.bind("<Button-1>",set_vol)



songlabel.pack()

root.mainloop()