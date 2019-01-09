import spotipy
import os
import sys
import json
import webbrowser
import random
import spotipy.util as util
from json.decoder import JSONDecodeError

## 
#  Connect to device
#
#  Ask for user's mood
#
#  Find artists within the genre specified by mood
#
#  Gather random songs from top 5 artists (user decides how many songs)
#
#  Create playlist for user given parameters
##


# Get username from terminal
username = sys.argv[1]
playlist_ids = 'YOUR PLAYLIST ID'
scope = 'playlist-modify-public user-read-private user-read-playback-state user-modify-playback-state'

# Erase cache and prompt for user permission
try: 
    token = util.prompt_for_user_token(username,scope,client_id='CLIENT_ID',client_secret='CIENT_SECRET',redirect_uri='http://google.com/')
except(AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# Create our spotifObject
spotipy = spotipy.Spotify(auth=token)

# Get current device
devices = spotipy.devices()
deviceID = devices['devices'][0]['id']
user = spotipy.current_user()
displayName = user['display_name']
followers = user['followers']['total']

# Get track info
track = spotipy.current_user_playing_track()
print()
artist = track['item']['artists'][0]['name']
track = track['item']['name']

mood = input("How are you feeling today? (sad, lit, happy, calm, curious, hardcore)")
number = int(input("How many songs do you want for your playlist?"))
playlistName = input("Name your playlist: ")
playlistDesc = input("Describe your playlist: ")

def create_mood(mood):
    """ creates a playlist of songs based on user's preference

        Param: mood --> describes how user is feeling
    """
    

    if mood == "sad":
        artistList = ['Grace Carter', 'George Glew', 'SYML', 'Folly Rae', 'Maria Lynn', 'Sara Phillips', 'Khalid', 'blackbear', 'Ed Sheeran']
    if mood == "lit":
        artistList = ['Drake', 'Sheck Wes', '21 Savage', 'A Boogie Wit da Hoodie', 'Kodak Black', 'Young Thug', 'Juice WRLD', 'Travis Scott', 'Lil Baby', 'Gunna', 'Future']
    if mood == "happy":
        artistList = ['David Guetta', 'Louis The Child', 'ODESZA', 'Diplo', 'Ookay', 'Hippie Sabotage', 'Flume', 'Tove Lo', 'What So Not', 'Big Wild', 'Alison Wonderland', 'RL Grime']
    if mood == "calm":
        artistList = ['jhfly', 'jrd.', 'Arbour', 'Lost Son', 'Idealism', 'Caleb Belkin', 'eevee', 'DLJ', 'Dweeb', 'SPEECHLESS', 'StackOne', 'Leavv', 'moow', 'towser']
    if mood == "curious":
        artistList = ['ZAYN', 'Maroon 5', 'Lil Wayne', 'Demi Lovato', 'Miguel', 'Shawn Mendes', 'Skrillex', 'Ludwig van Beethoven', 'Daddy Long Neck']
    if mood == "hardcore":
        artistList = ['Yellow Claw' ,'Bro Safari', 'Flosstradamus', 'Carnage', 'Zomboy', '$uicideBoy$', 'Borgore', 'MUST DIE!', 'ARIUS', 'Afrojack', 'SLANDER', 'GTA', 'Datsik']
    
    return artistList
    
def create_songs(number):
    """ Take in our list of artists based on mood user selected,
        and create a list of songs given the number they provided

        Param: number --> number of songs to use
    """ 
    artistList = create_mood(mood)
    userPick = [random.choice(artistList) for i in range(number)]
    print(userPick)
    searchResults = spotipy.search(userPick, 1, 0, "artist")
    artist = searchResults['artists']['items'][0]
    add_songs(artist)


def create_playlist(playlistName, playlistDesc):
    """ Creates the user playlist

        Param: playlistName --> the playlist title
               playlistDesc --> the playlist description
    """ 
    playlist = spotipy.user_playlist_create(username, playlistName, public=True, playlistDesc)     

def add_songs(artist):
    """ adds the songs to the created playlist

        Param: artist --> selects random songs given the artist
    """

    i = 0
    artistID = artist['id'] # Album and track details
    trackURIs = []
    songList = []

    albumResults = spotipy.artist_albums(artistID) # Extract album data
    albumResults = albumResults['items']
    albumList = random.choice(albumResults)

    for item in albumResults:
        albumID = item['id']
        trackResults = spotipy.album_tracks(albumID)
        trackResults = trackResults['items']

    trackList = random.choice(trackResults)
    songList.append(trackList['uri'])
    
    while i < number:
        newPlaylist = spotipy.user_playlist_add_tracks(username, playlist_ids, random.choice(songList))
        i+= 1


while True:

    print()
    print('>>> Welcome to Spotimood ' + displayName + '!')
    print('>>> You have ' + str(followers) + ' followers')
    print()
    print('0 - Create a mood playlist')
    print('1 - Exit the Application')
    print()
    choice = input("Your choice: ")

    if choice == "0":
        print("0")
        print()
        i = 0

        while i < 1:
            create_songs(number)
            i += 1
        
    

    if choice == "1":
        break