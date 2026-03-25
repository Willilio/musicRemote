# This file handles functions of managing and playing music.
# It can also find and download songs from YouTube music.
#
# The list of songs is stored in the library which contains an index file
MUSIC_DIRECTORY_NAME = "music"
INDEX_FILE_NAME = "index.txt"
# This index lists songs in the following manner:
# The first line contains the number of songs present in the file.
# Each song is represented with <artist>//<title> all lowercase.
#
# Functions of the music player:
# readLibrary() - a private method to populate the library list
# checkSong(artist, title) - determines whether a song is in the library
# getLibrary() - retrieves all songs present in the library
# downloadSong(artist, title) - a private method to download an audio file to the music directory
# addToLibrary(artist, title) - if a song is not in the library, add it by searching and downloading
# removeFromLibrary(artist, title) - if a song is in the library, remove it and erase the download
# playSong(artist, title) - begins playing the selected song

import os
import sys
import yt_dlp
import pygame

pygame.mixer.init()

# The music library is stored as a list of entries
# Each entry in the library
_library = []


# Populate the library list
def __readLibrary():
    global _library

    try:

        # Open the index file in read mode
        with open(f"{MUSIC_DIRECTORY_NAME}/{INDEX_FILE_NAME}", "r") as f:
            num_characters = int(f.readline().strip())
            _library = [f.readline().strip().split("//") for _ in range(num_characters)]
            f.close()

    except Exception as e:

        _library = []
        print("Failed to read index file.")
        print(e, file=sys.stderr)


# Check if song is present in the library list
def checkSong(artist, title):

    for song in _library:
        if song[0].lower() == artist.lower() and song[1].lower() == title.lower():
            return True

    return False


# Get library just returns the library list
def getLibrary():

    return _library


# Download a song to the music directory
def __downloadSong(artist, title):

    print(f"Downloading {title} by {artist}... ")

    # Song search and options
    song_query = f"{artist} {title}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'C:\Users\wcirw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin',
        'outtmpl': f"{MUSIC_DIRECTORY_NAME}/{artist.lower()}-{title.lower()}.%(ext)s",
        'noplaylist': True,
        'default_search': 'ytsearch1',
        'quiet': True,
        'no_warnings': False,
    }

    # Download song
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_query])

    print("Done!")


# Add a song to the library and modify the index file.
# This also downloads the requested song.
def addToLibrary(artist, title):

    if checkSong(artist, title):
        return

    try:

        # Update the index file
        file_lines = []
        with open(f"{MUSIC_DIRECTORY_NAME}/{INDEX_FILE_NAME}", "a+") as f:
            f.write(f"{artist}//{title}\n")
            f.seek(0, 0)
            file_lines = f.readlines()
            f.close()

        file_lines[0] = f"{int(file_lines[0].strip()) + 1}\n"
        with open(f"{MUSIC_DIRECTORY_NAME}/{INDEX_FILE_NAME}", "w") as f:
            f.writelines(file_lines)
            f.close()

        __downloadSong(artist, title)

    except Exception as e:

        print("Failed to add song to library.")
        print(e)

    finally:

        __readLibrary()


# Remove a song from the library and index file.
# This also deletes the downloaded music file.
def removeFromLibrary(artist, title):

    if checkSong(artist, title):

        print(f"Removing {title} by {artist} from library... ", end='')

        try:

            # Update the index file
            file_lines = []
            with open(f"{MUSIC_DIRECTORY_NAME}/{INDEX_FILE_NAME}", "r") as f:
                file_lines = f.readlines()
                f.close()

            file_lines[0] = f"{int(file_lines[0].strip()) - 1}\n"
            with open(f"{MUSIC_DIRECTORY_NAME}/{INDEX_FILE_NAME}", "w") as f:
                f.writelines(file_lines[:-1])
                f.close()

            # Delete the music file
            os.remove(f"{MUSIC_DIRECTORY_NAME}/{artist.lower()}-{title.lower()}.mp3")

            print("Done!")

        except Exception as e:

            print("Failed to remove song from library.")
            print(e)

        finally:

            __readLibrary()


# Begins playing a song from the beginning.
# It only works for songs present in the library.
def playSong(artist, title):

    if checkSong(artist, title):
        try:

            pygame.mixer.music.load(f"{MUSIC_DIRECTORY_NAME}/{artist.lower()}-{title.lower()}.mp3")
            pygame.mixer.music.play()

            # Keep the script alive while music plays
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:

            print("Failed to play song.")
            print(e)


# Setup code should be executed when this module is imported
if __name__ != "__main__":

    # If the music directory does not exist, then it should be created
    if not os.path.isdir(MUSIC_DIRECTORY_NAME):
        print("Music directory does not exist. Creating... ", end='')
        os.mkdir(MUSIC_DIRECTORY_NAME)
        print("Done!")

    # If the music directory does not contain an index file, then it should be created
    if not os.path.isfile(f"{MUSIC_DIRECTORY_NAME}/{INDEX_FILE_NAME}"):
        print("Music directory does not contain an index file. Creating... ", end='')
        with open(f"{MUSIC_DIRECTORY_NAME}/{INDEX_FILE_NAME}", "w") as idxFile:
            idxFile.write("0\n")
            idxFile.close()
        print("Done!")

    # Read the library index file
    __readLibrary()
