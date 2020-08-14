# shows track info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import sys
from pprint import pprint
import os
import eyed3

CLIENT_ID = "1b906312d4eb44189b1762bba74fa4f6"
CLIENT_SECRET = "adb0a2eaadd64949b3ea2074a2e69b6f"
username = "Luis De Marcos"
scope = 'playlist-modify-public'
redirect_uri = 'https://open.spotify.com/'

# token = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
token = util.prompt_for_user_token(
    username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri=redirect_uri)
if token:
   sp = spotipy.Spotify(auth=token)

tracks = []
rootdir = '/Users/Luis/Desktop/Pruebas'
for subdir, dirs, files in os.walk(rootdir):
     for file in files:
            try:
                audiofile = eyed3.load(os.path.join(subdir, file))
                artistName = audiofile.tag.artist
                trackName = audiofile.tag.title
                q = f"artist:{artistName} track:{trackName}"
                tracks.append(sp.search(q)["tracks"]['items'][-1]['uri'])
            except:
                pass

print(tracks)
sp.user_playlist_add_tracks(username, playlist_id="3M0rFsqlKE8NWmoHoRds1b", tracks=tracks)
