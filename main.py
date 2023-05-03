import yt_data
import json

import tones
import tones.mixer

# function returns True for flag raised
def checkFlags(p):
    # a playlist is not included in the data set if:
    # the length of the playlist is under 10 videos (insufficient) OR
    # "doubles" is in the playlist title OR
    # a video in the playlist has a duration of 0
    if len(p['videos']) < 10:
        print(f"Length of playlist {p['title']} is under 10 videos.")
        return True
    if "doubles" in p['title'].lower():
        print(f"'Doubles' found in playlist {p['title']}.")
        return True
    if p['videos'][0]['duration'] == 0:
        print(f"Playlist {p['title']} has video with zero duration.")
        return True
    return False

def getMaxVid(data):
    dur_max = 0
    newVid = None
    for playlist in data['playlists']:
        for video in playlist['videos']:
            if video['duration'] > dur_max:
                dur_max = video['duration']
                newVid = video
    return newVid

def getMaxTournament(data):
    dur_max = 0
    newTournament = None
    for playlist in data['playlists']:
        length = 0
        for video in playlist['videos']:
            length += video['duration']
        if length > dur_max:
            newTournament = playlist
            dur_max = length
    return newTournament

def audioDuration(data, divisor):
    ret = []
    for playlist in data['playlists']:
        toAdd = {
            'title': playlist['title'],
            'durations': []
        }
        for video in playlist['videos']:
            dur = video['duration'] / divisor
            toAdd['durations'].append(round(dur, 3))
        ret.append(toAdd)
    return ret

def createWav(data):
    # audio data is an array
    notes = "cdega" #chromatic scale
    octave = 3

    mixer = tones.mixer.Mixer()
    mixer.create_track("track")
    title = data['title']
    i=0
    for dur in data['durations']:
        mixer.add_note(
            'track',
            duration=dur,
            amplitude=0.25,
            note=notes[i],
            octave=octave,
            attack=0.25,
            decay=0.25
        )
        i += 1
        if i == 5:
            i = 0
            octave += 1
    mixer.write_wav(f'wav/{title}.wav')

def main(youtube):
    name = input("name of data file (enter to query youtube): ")
    wav = input("create new wav files? (y/n): ")
    if name == "":
        name = "data.json"
        if youtube == None:
            youtube = yt_data.getYoutube()
        data = yt_data.getAllPlaylists(youtube)
        with open(name, 'w') as w:
            json.dump(data, w)

    data = {}
    with open(name, 'r') as r:
        data = json.loads(r.read())

# remove entries based on requirements
    i = 0
    for playlist in data['playlists']:
        if checkFlags(playlist):
            print(data['playlists'].pop(i)['title'] + " dropped.")
        i += 1
    
# manual edit to fix bug in original data
# this is bc the first two playlists are created out of order
# first two playlists are last two in this set
    if data['channel'] == "Highlander Smash":
        temp = data['playlists'][-2]
        data['playlists'][-2] = data['playlists'][-1]
        data['playlists'][-1] = temp

# get durations for every game for every tournament
    audioData = audioDuration(data, 120)
    for aData in audioData:
        print(aData)
        if wav.lower() == 'y':
            createWav(aData)

# returning for working in a live environment
    return data


if __name__ == "__main__":
    main(None)