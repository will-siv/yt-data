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

def getMax(data):
    dur_max = 0
    newVid = ''
    for playlist in data['playlists']:
        for video in playlist['videos']:
            if video['duration'] > dur_max:
                dur_max = video['duration']
                newVid = video
    return newVid

def main():
    name = input("name of data file (enter to query youtube):")
    if name == "":
        name = "data.json"
        youtube = yt_data.getYoutube()
        data = yt_data.getAllPlaylists(youtube)
        with open(name, 'w') as w:
            w.write(str(data))

    with open(name, 'r') as r:
        data = json.loads(r.read())

    i = 0
    for playlist in data['playlists']:
        if checkFlags(playlist):
            data['playlists'].pop(i)
            continue
        i += 1


if __name__ == "__main__":
    main()