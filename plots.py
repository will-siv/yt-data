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
        ax.step(x, y, linewidth=2.5, color='black', alpha=0.1)

    ax.set_ylabel('Game in Tournament')
    ax.set_xlabel('Time Passed (seconds)')
    plt.show()

    return