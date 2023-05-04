import numpy as np
import matplotlib.pyplot as plt

def createPlot(data):
    fig, ax = plt.subplots()
    for playlist in data['playlists']:
        playlistTitle = playlist['title']
        x = [0]
        timePassed = 0
        for video in playlist['videos']:
            videoTitle = video['title']
            dur = video['duration']
            timePassed += dur
            x.append(timePassed)
        y = np.arange(0,len(x))
        ax.step(x, y, linewidth=2.5, color='black', alpha=0.1, where='post')

    ax.set_ylabel('Streamed Game in Tournament')
    ax.set_xlabel('Time Passed (seconds)')

    ax.set_title("Tournament Progression by Stream")
    plt.show()

    return

def createAudioPlot(audioData):
    def makeNoteArray(num):
        notes = "CDEGA"
        octave = 3
        ret = []
        i = 0
        while i < num:
            ret.append(notes[i%5] + str(octave))
            i+=1
            if i%5 == 4:
                octave += 1
        return ret

    fig, ax = plt.subplots()

    for data in audioData:
        durs = data['durations']
        playlistTitle = data['title']
        timePassed = 0
        x = [0]
        for duration in durs:
            timePassed += duration
            x.append(timePassed)
        y = np.arange(0, len(x))
        ax.step(x,y, linewidth=2.5, color='black', alpha=0.1, where='post')
    
    ax.set_yticks(np.arange(24))
    ax.set_yticklabels(makeNoteArray(24))
    ax.set_ylabel("Note Being Played")
    ax.set_xlabel("Time Into Audio")

    ax.set_title("Notes Played as Time Passes")
    plt.show()

    return
