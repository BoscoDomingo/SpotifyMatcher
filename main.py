import os
import sys

import eyed3
import spotipy
import spotipy.util as util

"""
# TO-DO: Allow users to pick between 2 modes: direct like, or create playlist
direct_like_scope = 'user-library-modify'
create_playlist_scope = 'playlist-modify-public'
"""


def get_username():
    """Retrieve username from arguments"""
    if len(sys.argv) > 1:  # TO-DO Ask for username in terminal
        return sys.argv[1]
    else:
        print("Usage: `python %s username`" % (sys.argv[0],))
        sys.exit()


def connect_to_spotify(username):
    """Used to obtain the access token for the given user"""
    token = util.prompt_for_user_token(username,
                                       scope,
                                       client_id='1b906312d4eb44189b1762bba74fa4f6',
                                       client_secret='adb0a2eaadd64949b3ea2074a2e69b6f',
                                       redirect_uri='https://localhost:8080/')

    if token:
        return spotipy.Spotify(auth=token)
    raise()


def get_title_and_artist():
    """Recursively reads local files in indicated rootdir and yields a string 'song - artist'"""
    if(len(rootdir == 0)):
        while True:
            rootdir = input("Please paste the path to your music directory:")
            if os.path.isdir(rootdir):
                break
            else:
                print(
                    "The provided path is not valid. Please try again or type in the path directly\
                    into the source code if there's issues (use Ctrl + C to exit the program)")

    successes = 0
    errors = 0
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            if file.split(".")[1] in formats:
                # if True:
                try:
                    audiofile = eyed3.load(os.path.join(subdir, file))
                    successes += 1
                    yield str(audiofile.tag.artist, "-", audiofile.tag.title)
                except:
                    errors += 1

    print(f"Successfully read {successes} and found {errors} errors")


def match_songs_to_spotify(song_list):
    """Checks the previously found list against the Spotify servers"""


def add_matches_to_playlist(matches_list):
    """Puts all matches into one playlist"""


def like_matches(song_list):
    """Likes all the songs that produced a match on Spotify servers """


if __name__ == "__main__":
    username = get_username()
    # username = "Luis De Marcos"
    try:
        sp = connect_to_spotify(username)
    except:
        print(f"Can't get token for {username}")
        sys.exit()
    # Continue with the Spotify object, sp
    rootdir = ""  # Write the dirpath directly here to avoid having to do it through terminal e.g. '/Users/Luis/Music/iTunes/iTunes Media/Music'
    formats = ("mp3", "wav", "flac")
    scope = 'playlist-modify-public user-library-modify user-library-read'
    tracks = []
    for query in get_title_and_artist():
        tracks.append(sp.search(query)["tracks"]['items'][-1]['uri'])

    """ results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name']) """
