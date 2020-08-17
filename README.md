# SpotifyMatcher

Cross-platform tool to match your local files to Spotify's database! Easily move all your .mp3 files over to a playlist on Spotify

## Before you start (5 minutes)

This isn't infalible, and it would be quite surprising if it matched 100% of songs. Be aware you'll probably have to do *a bit* of manual searching, but this will significantly reduce that amount by automating the majority of the process. On to the requirements and instructions:

### Install Python >3.4

Make sure you have Python 3.4 or later installed, preferably the latest version. We tested it with Python 3.8.4 on a x64 PC with Windows 10
You'll need to install the libraries `spotipy` and `eyed3`

I suggest you create a virtual environment so you don't mess other libraries, with the built in `venv`

### Using venv (OPTIONAL, RECOMMENDED)

For this, simply open a Terminal in the folder that the code is in (type 'wt' in the Windows Explorer address bar for Windows Terminal, or 'cmd' if that doesn't work)
and write the following commands (make sure to change <MyEnv> for your desired folder name):

```python
python -m pip install --upgrade pip
python -m venv <MyEnv>
<MyEnv>\Scripts\activate.bat # <- on cmd
<MyEnv>\Scripts\Activate.ps1 # <- on PowerShell
```

This should make the terminal look something like this:

![Terminal with venv active](https://imgur.com/1jWhGhU.png)

To exit the virtual environment, simply type `deactivate` and press Enter. It is not necessary, though, as we'll be working within the environment and you can just close the console once it is done.

### Installing the libraries

You can now install `spotipy` and `eyed3` with:

```python
pip install --upgrade spotipy
pip install --upgrade eyed3
```

### Creating a Spotify Developer Application

Head over to [the Spotify Developer website](https://developer.spotify.com/dashboard/), log in with your Spotify account and create a new application (name doesn't matter).

Copy the `client id` and the `client secret`, open the settings and make sure to add a URL to the "Redirect URIs". It doesn't really matter what, try https://localhost/ if not sure, but take note of it because you'll need to write it in the source code later.

![](https://i.imgur.com/lwFiRh9.png)
![](https://i.imgur.com/OerZP5c.jpg)
![](https://i.imgur.com/Z3DIPZf.jpg)

With these 3, open the file `main.py` with whatever IDE or Text Editor you like (preferably Wordpad if you use a text editor), and change this bit of code:

![connect_to_spotify code](https://i.imgur.com/m4rNPEW.png)

(Use the Find function to find it if you don't see it. It is inside the `connect_to_spotify` function)

Paste the aforementioned ids and the URL you chose in the corresponding lines. With this, setup is done and you can now use the tool!

## Using SpotifyMatcher

Usage is very, very simple. You only have to call the program with 
```python
python ./main.py username playlist_id
```
(may have to use `python3` if you have several versions of Python installed or if you're not on Windows).

With this, the application should open a new tab on your default browser. Accept the permissions its asking, and copy the URL of the page it takes you to (if it's localhost, it will probably not load anything, that's perfectly ok). Paste it in the terminal.

After that, authentication should be done and you can move on to the good stuff. Simply paste the path to your music directory (Tip: right click the address bar on Windows Explorer, 'Copy address as text'). **You can also bypass this step** if you manually enter a path in the source code. Simply find the `music_dir` variable and paste it there before you execute the program:

![Imgur](https://i.imgur.com/zXi9UkD.png)

If the path is valid, the program should start identifying your files and subsequently searching Spotify for a match. This may take several minutes, depending on your processor, internet speed, number of files... Just be patient!

Once done, if you specified a `playlist_id` it will try to add the matches to said playlist.
#### ***CAREFUL***
If you don't own said playlist, can't add tracks or it has been deleted, **the program will fail, and you'll have to start again**, so make sure you have said permissions.


We recommend either creating a new playlist and getting its id (simply open it in the browser and copy the final string of numbers and letters) or leaving it blank, so the program creates a new one for you.

Only thing left is to check the .txt file with the failed matches and search those manually (blame Spotify's unconsistent artist - title debacle!)

## Getting your username and playlist ids
### Username
Open Spotify on PC, go to your user profile and click the 3 dots. Click share and "Copy Spotify URI". You can use that directly, or remove the `spotify:user:`. Doesn't matter

![](https://imgur.com/TS6ZZlV.png)

You can also copy your user link and just take the stuff after `/user` but before the `?`

### Playlist id
We recommend you don't actually use a playlist id and rather leave it blank so the program creates one for you automatically, but if you insist, simply open the playlist, click the 3 dots > Share > Copy Spotify URI. As with the username, you can (and frankly we suggest you do) remove the `spotify:playlist:`.

As with the username, you can simply copy the palylist link and just take the final string of numbers and letters. Same thing.
