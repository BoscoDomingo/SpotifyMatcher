import os
import sys
from datetime import datetime
from time import sleep

import spotipy
from spotipy import oauth2
from tinytag import TinyTag

SCOPE = "playlist-modify-public playlist-modify-private user-library-modify"
MUSIC_DIR = ""
FAILED_MATCHES_FILENAME = "Failed matches - SpotifyMatcher.txt"
# Write the dirpath directly here to avoid having to do it through terminal.
# Make sure to escape backslashes. Examples:
# 'C:/Users/John/Music/My Music'
# "C:\\Users\\John\\Music\\My Music"


def get_user_data(argv=None):
    """Retrieve username and optional playlist id from arguments."""
    args = argv if argv is not None else sys.argv
    if len(args) == 2:
        return args[1], ""

    if len(args) == 3:
        return args[1], args[2]

    print(
        f"Usage:\n\tpython {args[0]} username [OPTIONAL]playlist_id"
        "\n\nTo know how to find each, check the README.md or the GitHub page"
    )
    sys.exit()


def connect_to_spotify(username):
    """Create and return the Spotify client and auth manager for a user."""
    auth_manager = oauth2.SpotifyOAuth(
        client_id="1b906312d4eb44189b1762bba74fa4f6",
        client_secret="adb0a2eaadd64949b3ea2074a2e69b6f",
        redirect_uri="https://open.spotify.com/",
        scope=SCOPE,
        username=username,
    )

    if not auth_manager:
        print(f"Can't get token for {username}")
        sys.exit()

    return spotipy.Spotify(auth_manager=auth_manager), auth_manager


def get_auth_token(auth_manager):
    auth_token = auth_manager.get_cached_token()

    if not auth_token:
        return auth_manager.get_access_token(as_dict=True)

    return auth_token


def get_title_and_artist(music_dir):
    """Read files in music_dir and yield (spotify_query, display_name)."""
    if len(music_dir) == 0 or not os.path.isdir(music_dir):
        while True:
            music_dir = input("Please paste the path to your music directory:")

            if not os.path.isdir(music_dir):
                print(
                    "The provided path is not valid. Please try again or type "
                    "in the path directly into the source code if there's "
                    "issues\n(use Ctrl + C to exit the program)"
                )
            else:
                break
    else:
        print(f"Found valid path. Commencing search in {music_dir}")

    files_read = 0
    for subdir, _, files in os.walk(music_dir):
        for file in files:
            try:
                audiofile = TinyTag.get(os.path.join(subdir, file))
            except Exception:
                continue

            if not audiofile.title or not audiofile.artist:
                continue

            files_read += 1
            yield f"track:{audiofile.title} artist:{audiofile.artist}", f"{audiofile.artist} - {audiofile.title}"

    if files_read == 0:
        print("\nNo files found at the specified location.Please check the path to the directory is correct.")
        sys.exit()

    print(
        f"\nRead {files_read} files. Make sure to check for any possible "
        'unread files due to "Lame tag CRC check failed" or similar.\n'
        "Those come from an external library and this software cannot "
        "account for them"
    )


def ensure_playlist_exists(sp, username, playlist_id):
    try:
        if not playlist_id:
            raise ValueError("No playlist ID provided")

        sp.user_playlist(username, playlist_id)["id"]
        return playlist_id
    except Exception:
        print(
            "\nNo playlist_id provided. Creating a new playlist..."
            if len(playlist_id) == 0
            else "\nThe playlist_id provided did not match any of your existing playlists. Creating a new one..."
        )
        return create_new_playlist(sp, username)


def create_new_playlist(sp, username):
    try:
        date = datetime.now().strftime("%d %b %Y at %H:%M")
        playlist_id = sp.user_playlist_create(
            username,
            "SpotifyMatcher",
            description="Playlist automatically created by SpotifyMatcher "
            f"from my local files on {date}. "
            "Try it at https://github.com/BoscoDomingo/SpotifyMatcher!",
        )["id"]
        print(f"Find it at: https://open.spotify.com/playlist/{playlist_id}")
        return playlist_id
    except Exception:
        print(
            "\nWARNING: \n"
            "There was an error creating the playlist. Please, create one "
            "manually and paste its id in the terminal, after your username\n"
        )
        sys.exit(1)


def add_tracks_to_playlist(sp, username, playlist_id, track_ids):
    """Add tracks in batches of 100, since that's Spotify's limit."""
    spotify_limit = 100
    while len(track_ids) > 0:
        try:
            sp.user_playlist_add_tracks(username, playlist_id, track_ids[:spotify_limit])
        except Exception:
            sleep(0.2)
        else:
            del track_ids[:spotify_limit]


def calculate_success_rate(matches, searched):
    if searched == 0:
        return "0.00"
    return "{:.2f}".format(matches / searched * 100)


def run(music_dir=MUSIC_DIR):
    username, playlist_id = get_user_data()
    sp, auth_manager = connect_to_spotify(username)

    sp.search("whatever", limit=1)

    token_info = get_auth_token(auth_manager)
    track_ids = []
    search_cache = {}
    searched_songs = 0

    with open(FAILED_MATCHES_FILENAME, "w", encoding="utf-8") as failed_matches_file:
        for query, display_name in get_title_and_artist(music_dir):
            if auth_manager.is_token_expired(token_info):
                token_info = auth_manager.refresh_access_token(token_info["refresh_token"])

            searched_songs += 1
            print(f"{searched_songs}: {display_name}")

            if query not in search_cache:
                try:
                    search_cache[query] = sp.search(query, limit=1)["tracks"]["items"][0]["id"]
                except Exception:
                    search_cache[query] = None

            result = search_cache[query]
            if result is None:
                print("\t*NO MATCH*")
                failed_matches_file.write(f"{display_name}\n")
            else:
                track_ids.append(result)

        success_rate = calculate_success_rate(len(track_ids), searched_songs)
        print(f"\n***TOTAL SONGS SEARCHED: {searched_songs}  TOTAL MATCHES:{len(track_ids)} ({success_rate}%)***\n")

    playlist_id = ensure_playlist_exists(sp, username, playlist_id)
    number_of_matches = len(track_ids)
    add_tracks_to_playlist(sp, username, playlist_id, track_ids)

    print(f"\nSuccessfully added {number_of_matches} songs to the playlist.\nThank you for using SpotifyMatcher!")
    print(
        f"\n{searched_songs - number_of_matches} UNMATCHED SONGS (search "
        "for these manually, as they either have wrong info or aren't "
        f'available in Spotify)\nWritten to "{FAILED_MATCHES_FILENAME}":\n'
    )


if __name__ == "__main__":
    run()
