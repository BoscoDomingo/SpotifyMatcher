from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
import eyed3

# shows artist info for a URN or URL

# export SPOTIPY_CLIENT_ID = "1b906312d4eb44189b1762bba74fa4f6"
# export SPOTIPY_CLIENT_SECRET = "adb0a2eaadd64949b3ea2074a2e69b6f"

rootdir = '/Users/Luis/Music/iTunes/iTunes Media/Music'
formats = ("mp3","wav","flac")

def main():
    errorFiles = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.split(".")[1] in formats:
                try:
                    a = 1
                    audiofile = eyed3.load(os.path.join(subdir, file))
                    print(audiofile.tag.artist, "-",audiofile.tag.title)
                except:
                    pass

if __name__ == "__main__":
    # Get whatever IDs are needed to establish connection
    main()
    pass

