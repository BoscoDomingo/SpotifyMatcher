import os
import sys
from pprint import pprint

import eyed3
import spotipy
import spotipy.util as util


def get_essential_data():
    """Retrieve username and playlist id from arguments"""
    if len(sys.argv) == 2:
        return sys.argv[1], ""
    elif len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print(
            f"Usage:\n\tpython {sys.argv[0]} username [OPTIONAL]playlist_id\n\nTo know how to find them, check the README.md")
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


def get_title_and_artist(music_dir):
    """Recursively reads local files in indicated music_dir and yields a string 'song - artist'"""
    if len(music_dir) == 0 or not os.path.isdir(music_dir):
        while True:
            music_dir = input("Please paste the path to your music directory:")
            if os.path.isdir(music_dir):
                break
            else:
                print(
                    "The provided path is not valid. Please try again or type "
                    "in the path directly into the source code if there's "
                    "issues\n(use Ctrl + C to exit the program)")
    else:
        print(f"Found valid path. Commencing search in {music_dir}")

    successes = 0
    errors = 0
    for subdir, _, files in os.walk(music_dir):
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

    print(f"\nSuccessfully read {successes} files and found {errors} errors")


if __name__ == "__main__":
    """
    # TO-DO: Allow users to pick between 2 modes: direct like, or create playlist
    direct_like_scope = 'user-library-modify'
    create_playlist_scope = 'playlist-modify-public'
    """
    music_dir = "D:/Users/bosco/Downloads/SpotifyMatcher Test"
    # Write the dirpath directly here to avoid having to do it through terminal
    # Make sure to escape backslashes. Examples:
    # '/Users/John/Music/My Music'
    # "C:\\Users\\John\\Music\\My Music"
    formats = ("mp3", "wav", "flac")
    scope = 'playlist-modify-public user-library-modify user-library-read'

    username, playlist_id = get_essential_data()
    sp = connect_to_spotify(username)

    track_ids = []
    failed_song_names = []
    searched_songs = 1
    for query in get_title_and_artist(music_dir):
        print(f"{searched_songs} - {query}")
        searched_songs += 1
        try:
            result = sp.search(query, limit=1)["tracks"]['items'][0]['id']
        except:
            print("\t*NO MATCH*")
            failed_song_names.append(query.replace(
                "track:", "").replace("artist:", "- ").title())
            # TO-DO: Write to .txt
        else:
            track_ids.append(result)
    print(
        f"\nTOTAL SONGS SEARCHED: {searched_songs-1}\tTOTAL MATCHES: {len(track_ids)}")

    try:
        sp.user_playlist(username, playlist_id)["id"]
    except:
        if len(playlist_id) == 0:
            print(f"\nNo playlist_id provided. Creating a new playlist...")
        else:
            print(
                f"\nThe playlist_id provided did not match any of your existing playlists. Creating a new one...")

        playlist_id = sp.user_playlist_create(
            username, "SpotifyMatcher",
            description="Playlist automatically created by SpotifyMatcher from my local files."
                        "Try it at https://github.com/BoscoDomingo/SpotifyMatcher!")["id"]
        print(f"Find it at: https://open.spotify.com/playlist/{playlist_id}")
    finally:
        sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print(f"\nUNMATCHED SONGS({searched_songs-1-len(track_ids)}) (search "
              "for these manually, as they either have wrong info or aren't "
              "available in Spotify):")
        pprint(failed_song_names)
