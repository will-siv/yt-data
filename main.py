import yt_data
import json

# function returns True for flag raised
def checkFlags(p):
    # a playlist is not included in the data set if:
    # the length of the playlist is under 10 videos (insufficient) OR
    # "doubles" is in the playlist title
    if len(p['videos']) < 10:
        print(f"Length of playlist {p['title']} is under 10 videos.")
        return True
    if "doubles" in p['title'].lower():
        print(f"'Doubles' found in playlist {p['title']}.")
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
    ret = {
        'title':'',
        'durations':[]
    }

    for playlist in data['playlists']:
        toAdd = []
        ret['title'] = playlist['title']
        for video in playlist['videos']:
            toAdd.append(video['duration'] / divisor)
        ret['durations'].append(toAdd)
    return ret

def main(youtube):
    name = input("name of data file (enter to query youtube): ")
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
            data['playlists'].pop(i)
            continue
        i += 1
    
# manual edit to fix bug in original data
# this is bc the first two playlists are created out of order
# first two playlists are last two in this set
    temp = data['playlists'][-2]
    data['playlists'][-2] = data['playlists'][-1]
    data['playlists'][-1] = temp

# get durations for every game for every tournament
    audioData = audioDuration(data, 120)
    print(audioData)
#printing because i am putting this in audacity i give up

# returning for working in a live environment
    return data


if __name__ == "__main__":
    main(None)