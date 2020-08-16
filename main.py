import os
import sys
from pprint import pprint

import eyed3
import spotipy
import spotipy.util as util


def get_username():
    """Retrieve username from arguments"""
    if len(sys.argv) > 1:
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
    print(f"Can't get token for {username}")
    sys.exit()


def get_title_and_artist(rootdir):
    """Recursively reads local files in indicated rootdir and yields a string 'song - artist'"""
    if len(rootdir) == 0 or not os.path.isdir(rootdir):
        while True:
            rootdir = input("Please paste the path to your music directory:")
            if os.path.isdir(rootdir):
                break
            else:
                print(
                    "The provided path is not valid. Please try again or type "
                    "in the path directly into the source code if there's "
                    "issues\n(use Ctrl + C to exit the program)")
    else:
        print(f"Found valid path. Commencing search in {rootdir}")

    successes = 0
    errors = 0
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            if file.split(".")[-1] in formats:
                # if True:
                try:
                    audiofile = eyed3.load(os.path.join(subdir, file))
                except:
                    errors += 1
                else:
                    yield f"track:{audiofile.tag.title} artist:{audiofile.tag.artist}"
                    # Query being in double quotes makes it stick to the given
                    # word order instead of matching a bunch of possibilities
                    successes += 1

    print(f"Successfully read {successes} files and found {errors} errors")


if __name__ == "__main__":
    """
    # TO-DO: Allow users to pick between 2 modes: direct like, or create playlist
    direct_like_scope = 'user-library-modify'
    create_playlist_scope = 'playlist-modify-public'
    """
    rootdir = ""
    # Write the dirpath directly here to avoid having to do it through terminal
    # Make sure to escape backslashes. Examples:
    # '/Users/John/Music/My Music'
    # "C:\\Users\\John\\Music\\My Music"
    formats = ("mp3", "wav", "flac")
    scope = 'playlist-modify-public user-library-modify user-library-read'

    username = get_username()
    sp = connect_to_spotify(username)

    track_IDs = []
    failed_songs = []
    searched_songs = 1
    for query in get_title_and_artist(rootdir):
        print(f"{searched_songs} - {query}")
        searched_songs += 1
        try:
            # result = sp.search(query, limit=1)
            result = sp.search(query, limit=1)["tracks"]['items'][0]['id']
        except:
            print("\t*NO MATCH*")
            failed_songs.append(query.replace(
                "track:", "").replace("artist:", " - ").title())
            # TO-DO: Write to .txt
        else:
            track_IDs.append(result)
    print(
        f"TOTAL SONGS SEARCHED: {searched_songs-1}\tTOTAL MATCHES: {len(track_IDs)}")
    pprint(track_IDs)
    print("Failed songs:")
    pprint(failed_songs)
