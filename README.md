# SpotifyMatcher <!-- omit in toc -->

![Logo image](https://user-images.githubusercontent.com/46006784/166269127-56d4709d-6464-4f83-aace-e6fb53bbbd9d.png)

Free, cross-platform tool to match your local files to Spotify's database. Easily transfer all your local songs over to a playlist on Spotify in just a few minutes. Migrating your local library has never been easier!

*Because we all deserve to listen to our music wherever we want to.*

## Table of Contents <!-- omit in toc -->

1. [Before you start (5 minutes)](#before-you-start-5-minutes)
   1. [Install Python >=3.10 and dependencies](#install-python-310-and-dependencies)
      1. [Using `venv` or `virtualenv` (OPTIONAL, RECOMMENDED)](#using-venv-or-virtualenv-optional-recommended)
      2. [Installing the libraries](#installing-the-libraries)
   2. [Creating a Spotify Developer Application](#creating-a-spotify-developer-application)
   3. [Configuring your Spotify credentials](#configuring-your-spotify-credentials)
2. [Using SpotifyMatcher](#using-spotifymatcher)
   1. [**_CAREFUL_**](#careful)
3. [Getting your username and playlist ids](#getting-your-username-and-playlist-ids)
   1. [Username](#username)
   2. [Playlist id](#playlist-id)

## Before you start (5 minutes)

> [!NOTE]
> _This tool isn't infalible, and it would be quite surprising if it matched 100% of songs. Be aware you'll probably have to do **a bit** of manual searching, but this will significantly reduce that amount by automating the majority of the process._
>
> Also, **this guide assumes no prior experience with code, Python or command line**. This means if you do have experience, feel free to skip around.

### Install Python >=3.10 and dependencies

Make sure you have Python 3.10+ installed, preferably the latest version. Google it or ask AI, as it will vary depending on your system.

#### Using `venv` or `virtualenv` (OPTIONAL, RECOMMENDED)

I suggest you create a virtual environment so you don't install dependencies globally, with the built-in `venv` or via `virtualenv`.

For this, simply navigate to or open a terminal in the folder that the code is in (tip: type `wt` in the Windows Explorer address bar for Windows Terminal, or `cmd` if that doesn't work, or use `cd /path/to/folder`) and write the following:

```shell
python -m pip install -U pip # get the latest pip just in case

# Set up the virtual environment
python -m venv .venv
# pip install virtualenv && python -m virtualenv .venv # if you prefer `virtualenv`, but `venv` works just fine

# Then activate it according to your system:
chmod +x .venv/bin/activate # if you run into permission issues on Linux/MacOS
source .venv/bin/activate # Linux/MacOS
.venv\Scripts\Activate.ps1 # PowerShell
.venv\Scripts\activate.bat # cmd
```

This should make the terminal look something like this:

![Terminal with venv active](https://i.imgur.com/1jWhGhU.png)

To exit the virtual environment, simply type `deactivate` and press Enter. It is not necessary, though, as you'll be working within the environment and you can just close the console once it is done.

#### Installing the libraries

You can now run:

```shell
python -m pip install -e .
```

And you're all set!

### Creating a Spotify Developer Application

Head over to [the Spotify Developer website](https://developer.spotify.com/dashboard/), log in with your Spotify account and create a new application (name doesn't matter).

Copy the `client id` and the `client secret` (don't worry, the ones shown below no longer valid), open the settings and add `https://open.spotify.com/` to the "Redirect URIs".

![](https://i.imgur.com/lwFiRh9.png)
![](https://i.imgur.com/OerZP5c.jpg)
![](https://i.imgur.com/Z3DIPZf.jpg)

### Configuring your Spotify credentials

Copy `.env.example` to `.env`:

```shell
cp .env.example .env
```

Then open `.env` and paste the `client id` and `client secret` from your Spotify Developer application:

```dotenv
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret
```

With this, setup is done and you can now use the tool!

## Using SpotifyMatcher

Usage is very, very simple. You only have to call the program from a terminal of your choice with

```sh
python main.py username playlist_id
```

(may have to use `python3` if you have several versions of Python installed or if you're on Linux distros).

With this, the application should open a new tab on your default browser. Accept the permissions it asks for, and copy the URL of the page it takes you to (if it's localhost, it will probably not load anything, that's perfectly ok; we only need the URL).

Paste it in the terminal.

With that, authentication should be done and you can move on to the _good stuff_. Simply paste the path to your music directory (Tip: right click the address bar on Windows Explorer, 'Copy address as text').

> [!TIP]
> **You can also bypass this step** if you manually enter a path in the source code. Simply find the `MUSIC_DIR` constant and paste it there before you execute the program

If the path is valid, the program should start identifying your files and subsequently searching Spotify for a match. This may take several minutes, depending on your processor, internet speed, number of files... Just be patient!

Once done, if you specified a `playlist_id` it will try to add the matches to said playlist.

#### **_CAREFUL_**

If you don't own said playlist, can't add tracks or it has been deleted, **the program will fail, and you'll have to start again**, so make sure you have said permissions.

I recommend either leaving it blank, so the program creates a new one for you or creating a new playlist and getting its id (simply open it in the browser and copy the final string of numbers and letters).

Only thing left is to check the .txt file with the failed matches and search those manually (sucks but it is the best we can do with Spotify's search!)

## Getting your username and playlist ids

### Username

Open Spotify on PC, go to your user profile and click the 3 dots. Click share and "Copy Spotify URI". Paste and remove the `spotify:user:`

![Find your Spotify URI](https://i.imgur.com/TS6ZZlV.png)

You can also copy your profile link and just take the stuff after `/user` but before the `?`

### Playlist id

I recommend you don't actually use a playlist id and rather leave it blank so the program creates one for you automatically, but if you insist, simply open the playlist, click the 3 dots > Share > Copy Spotify URI. As with the username, remove the `spotify:playlist:`.

Alternatively, you can simply copy the playlist link and just take the final string of numbers and letters. Same thing.
