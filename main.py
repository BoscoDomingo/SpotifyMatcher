import os
import sys
import time
import spotipy
from spotipy import oauth2
from datetime import datetime
from time import sleep
from tinytag import TinyTag


def get_user_data():
    """Retrieve username and playlist id from arguments"""
    if len(sys.argv) == 2:
        return sys.argv[1], ""
    elif len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print(
            f"Usage:\n\tpython {sys.argv[0]} username [OPTIONAL]playlist_id"
            "\n\nTo know how to find each, check the README.md or the GitHub page")
        sys.exit()


def connect_to_spotify():
    """Used to obtain the auth_manager and establish a connection to Spotify
    for the given user.
    Returns (Spotify object, auth_manager)"""
    auth_manager = oauth2.SpotifyOAuth(
        client_id='YOUR_CLIENT_ID_HERE',
        client_secret='YOUR_CLIENT_SECRET_HERE',
        redirect_uri='http://localhost/',
        scope=scope,
        username=username)
    if auth_manager:
        return (spotipy.Spotify(auth_manager=auth_manager), auth_manager)
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
            try:
                audiofile = TinyTag.get(os.path.join(subdir, file))
            except:
                pass
            else:
                files_read += 1
                yield (f"track:{audiofile.title} artist:{audiofile.artist}", f"{audiofile.artist} - {audiofile.title}")
                # NOTE: Query being in double quotes makes it stick to the
                # given word order instead of matching a bunch of possibilities
                # Use it (by writing \" at the beginning and end of the string)
                # if you are not happy with the matches found
    if files_read == 0:
        print("\nNo files found at the specified location."
              "Please check the path to the directory is correct.")
        sys.exit()
    print(f"\nRead {files_read} files. Make sure to check for any possible "
          "unread files due to \"Lame tag CRC check failed\" or similar.\n"
          "Those come from an external library and this software cannot "
          "account for them")


def ensure_playlist_exists(playlist_id):
    try:
        if not playlist_id:
            raise Exception
        sp.user_playlist(username, playlist_id)["id"]
        return playlist_id
    except:
        print(f"\nNo playlist_id provided. Creating a new playlist..." if len(playlist_id) == 0 else f"\nThe playlist_id provided did not match any of your "
              "existing playlists. Creating a new one...")
        return create_new_playlist()


def create_new_playlist():
    try:
        date = datetime.now().strftime("%d %b %Y at %H:%M")  # 1 Jan 2020 at 13:30
        playlist_id = sp.user_playlist_create(
            username, "SpotifyMatcher",
            description="Playlist automatically created by SpotifyMatcher "
            f"from my local files on {date}. "
            "Try it at https://github.com/BoscoDomingo/SpotifyMatcher!")["id"]
        print(
            f"Find it at: https://open.spotify.com/playlist/{playlist_id}")
        return playlist_id
    except:
        print("\nWARNING: \n"
              "There was an error creating the playlist. Please, create one "
              "manually and paste its id in the terminal, after your username\n")
        sys.exit()


def add_tracks_to_playlist(track_ids, playlist_id):
    """Add tracks in batches of 100, since that's the limit Spotify has in place"""
    spotify_limit = 100
    while len(track_ids) > 0:
        try:
            print("\tAdding to Playlist " + playlist_id)
            sp.user_playlist_add_tracks(
                username, playlist_id, track_ids[:spotify_limit])
        except:  # API rate limit reached
            sleep(0.2)
        else:
            del track_ids[:spotify_limit]


def updateWithTrackChunk(chunk_track_ids, playlist_id):
    playlist_id = ensure_playlist_exists(playlist_id)
    number_of_matches = len(chunk_track_ids)
    add_tracks_to_playlist(chunk_track_ids, playlist_id)
    return playlist_id

if __name__ == "__main__":
    """
    TO-DO: Allow users to pick between 2 modes: direct like or create playlist
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
    sp, auth_manager = connect_to_spotify()

    # Needed to get the cached authentication if missing
    dummy_search = sp.search("whatever", limit=1)

    token_info = auth_manager.get_cached_token() if auth_manager.get_cached_token() else auth_manager.get_access_token(as_dict=True)
    track_ids = []
    chunk_track_ids = []
    failed_song_names = []
    searched_songs = 0
    failed_matches_filename = "Failed matches - SpotifyMatcher.txt"
    successful_matches_filename = "Successful matches - SpotifyMatcher.txt"
    cached_playlist_id_filename = "playlist_id.txt"

    if os.path.exists(cached_playlist_id_filename):
        playlist_file = open(cached_playlist_id_filename)
        playlist_id = playlist_file.read()
    else:
        playlist_id = ensure_playlist_exists(playlist_id)
        playlist_file = open(cached_playlist_id_filename, "w+")
        playlist_file.write(playlist_id)
        playlist_file.close()

    if os.path.exists(successful_matches_filename):
        append_write = 'rb+' # append if already exists
    else:
        append_write = 'wb+'

    playlist_id = ensure_playlist_exists(playlist_id)

    with open(failed_matches_filename, append_write) as failed_matches_file:
        with open(successful_matches_filename, append_write) as successful_matches_file:
            found_songs = successful_matches_file.readlines()
            failed_songs = failed_matches_file.readlines()
            print(f"Stored found songs: {len(found_songs)}. Stored failed songs: {len(failed_songs)}");
            for query_song_pair in get_title_and_artist(music_dir):
                try:
                    if auth_manager.is_token_expired(token_info):
                        token_info = auth_manager.refresh_access_token(token_info["refresh_token"])
                    searched_songs += 1
                    song_name = f"{query_song_pair[1]}\n".encode('utf8');
                    print(f"{searched_songs}: {query_song_pair[1]}")
                    if(song_name in found_songs or song_name in failed_songs):
                        print(f"\t ^ already found or failed, skipping")
                    else:
                        try:
                            result = sp.search(query_song_pair[0], limit=1)[
                                "tracks"]['items'][0]['id']
                        except:
                            if (len(query_song_pair) > 1):
                                print("\t*NO MATCH*")
                                failed_matches_file.write(song_name)
                                failed_song_names.append(query_song_pair[1])
                            else:
                                print("SONG CORRUPTED")
                        else:
                            track_ids.append(result)
                            chunk_track_ids.append(result)
                            successful_matches_file.write(song_name)
                            if(searched_songs % 100 == 0 and len(chunk_track_ids) > 0):
                                print("\tSending Chunk")
                                playlist_id = updateWithTrackChunk(chunk_track_ids, playlist_id)
                                chunk_track_ids = []
                except Exception as e: print(e)
                    
                    
        success_rate = "{:.2f}".format(len(track_ids)/(searched_songs-1)*100)
        print(
            f"\n***TOTAL SONGS SEARCHED: {searched_songs}"
            f"  TOTAL MATCHES:{len(track_ids)} ({success_rate}%)***\n")

    playlist_id = updateWithTrackChunk(chunk_track_ids, playlist_id)
    print(f"\nSuccessfully added {number_of_matches} songs to the playlist.\n"
          "Thank you for using SpotifyMatcher!")
    print(f"\n{searched_songs-number_of_matches} UNMATCHED SONGS (search "
          "for these manually, as they either have wrong info or aren't "
          f"available in Spotify)\nWritten to \"{failed_matches_filename}\":\n")
