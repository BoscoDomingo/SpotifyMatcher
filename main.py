import os
import sys
from datetime import date
from pprint import pprint
from time import sleep

import eyed3
import spotipy
import spotipy.util as util


def get_user_data():
    """Retrieve username and playlist id from arguments"""
    if len(sys.argv) == 2:
        return sys.argv[1], ""
    elif len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print(
            f"Usage:\n\tpython {sys.argv[0]} username [OPTIONAL]playlist_id"
            "\n\nTo know how to find them, check the README.md")
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

    files_read = 0
    for subdir, _, files in os.walk(music_dir):
        for file in files:
            if file.split(".")[-1] == "mp3":
                try:
                    audiofile = eyed3.load(os.path.join(subdir, file))
                except:
                    pass
                else:
                    files_read += 1
                    yield (f"track:{audiofile.tag.title} artist:{audiofile.tag.artist}",
                           f"{audiofile.tag.artist} - {audiofile.tag.title}")
                    # NOTE: Query being in double quotes makes it stick to the
                    # given word order instead of matching a bunch of possibilities
                    # Use it (by writing \" at the beginning and end of the string)
                    # if you are not happy with the matches found

    print(f"\nRead {files_read} files. Make sure to check for any possible "
          "unread files due to \"Lame tag CRC check failed\" or similar.\n"
          "Those come from an external library and this software cannot "
          "account for them")


def create_new_playlist():
    try:
        today = date.today().strftime("%d %b %Y")  # 1 Jan 2020
        playlist_id = sp.user_playlist_create(
            username, "SpotifyMatcher",
            description="Playlist automatically created by SpotifyMatcher "
            f"from my local files on {today}. "
            "Try it at https://github.com/BoscoDomingo/SpotifyMatcher!")["id"]
        print(
            f"Find it at: https://open.spotify.com/playlist/{playlist_id}")
        return playlist_id
    except:
        print("\nWARNING: \n"
              "There was an error creating the playlist. Please, create one "
              "manually and paste its id in the terminal, next to your username\n")
        sys.exit()


def add_tracks_to_playlist(track_ids):
    """Add tracks in batches of 100, since that's the limit Spotify has in place"""
    spotify_limit = 100
    while len(track_ids) > 0:
        try:
            sp.user_playlist_add_tracks(
                username, playlist_id, track_ids[:spotify_limit])
        except:  # API rate limit reached
            sleep(0.2)
        else:
            del track_ids[:spotify_limit]


if __name__ == "__main__":
    """
    # TO-DO: Allow users to pick between 2 modes: direct like or create playlist
    direct_like_scope = 'user-library-modify'
    create_playlist_scope = 'playlist-modify-public'
    """
    scope = 'playlist-modify-public user-library-modify'
    music_dir = ""
    # Write the dirpath directly here to avoid having to do it through terminal.
    # Make sure to escape backslashes. Examples:
    # '/Users/John/Music/My Music'
    # "C:\\Users\\John\\Music\\My Music"

    username, playlist_id = get_user_data()
    sp = connect_to_spotify(username)
    track_ids = []
    failed_song_names = []
    searched_songs = 0
    failed_matches_filename = "Failed matches - SpotifyMatcher.txt"
    with open(failed_matches_filename, "w") as failed_matches_file:
        for query_song_pair in get_title_and_artist(music_dir):
            searched_songs += 1
            print(f"{searched_songs}: {query_song_pair[1]}")
            try:
                result = sp.search(query_song_pair[0], limit=1)[
                    "tracks"]['items'][0]['id']
            except:
                print("\t*NO MATCH*")
                failed_matches_file.write(f"{query_song_pair[1]}\n")
                failed_song_names.append(query_song_pair[1])
            else:
                track_ids.append(result)
        success_rate = "{:.2f}".format(len(track_ids)/(searched_songs-1)*100)
        print(
            f"\n**TOTAL SONGS SEARCHED: {searched_songs}"
            f"   TOTAL MATCHES:{len(track_ids)} ({success_rate}%)**\n")

    try:  # Check if playlist exists
        sp.user_playlist(username, playlist_id)["id"]
    except:
        if len(playlist_id) == 0:
            print(f"\nNo playlist_id provided. Creating a new playlist...")
        else:
            print(
                f"\nThe playlist_id provided did not match any of your "
                "existing playlists. Creating a new one...")
        playlist_id = create_new_playlist()
    finally:
        number_of_matches = len(track_ids)
        add_tracks_to_playlist(track_ids)
        print(f"Successfully added {number_of_matches} songs to the playlist.\n"
              "Thank you for using SpotifyMatcher!")
        print(f"\n{searched_songs-number_of_matches} UNMATCHED SONGS (search "
              "for these manually, as they either have wrong info or aren't "
              f"available in Spotify)\nWritten to \"{failed_matches_filename}\":\n")
