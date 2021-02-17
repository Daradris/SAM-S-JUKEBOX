from pygame import mixer
import cv2
import datetime
from library_manager import Library_manager
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import random
import time


import argparse

from system_setting import Setting


class SamsJukebox:

    @staticmethod
    def setup(library_path):
        Setting.set_music_library_path(library_path)

    @staticmethod
    def run():
        #BLOCK 1
        #setting the library

        filepath = Setting.music_library_path()
        music_lib = Library_manager(filepath)
        music_lib.read_library()


        # QR CODE
        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)


        previous_order = 'A 0'
        time_of_first_blanck = datetime.datetime.now()
        time_of_last_oder = datetime.datetime.now()


        # MUSIC
        mixer.init()
        music_sound = mixer.Channel(0)
        system_sound = mixer.Channel(1)
        system_sound.play(mixer.Sound("beep.mp3"))

        pause_state = False
        previous_songs = []
        current_song = ''
        next_songs = []
        playlist_mode = False

        while True:
            # QR CODE
            frame = vs.read()
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
            if barcodes:
                data = barcodes[0].data.decode("utf-8")
            else:
                data = ''
            new_order = 'A 0'
            if data:
                if data != previous_order:

                    new_order = data
                    previous_order = new_order
                time_of_last_oder = datetime.datetime.now()
            if data == "":
                time_of_first_blanck = datetime.datetime.now()
                if (time_of_first_blanck - time_of_last_oder ) > datetime.timedelta(seconds=5):
                    previous_order = 'A 0'

            previous_songs = previous_songs[0:5]
            isplaying = music_sound.get_busy()


            if new_order == 'A 1':# play/ unpause
                if current_song != '':
                    if pause_state == True:
                        system_sound.play(mixer.Sound("beep.mp3"))
                        music_sound.unpause()
                        pause_state = False
                pass

            elif new_order == 'A 2':# PAUSE
                if current_song != '':
                    if pause_state == False:
                        music_sound.pause()
                        system_sound.play(mixer.Sound("beep.mp3"))
                        pause_state = True
                    pass

            elif new_order == 'A 3': # STOP
                if current_song != '':
                    if pause_state == False:
                        music_sound.pause()
                        system_sound.play(mixer.Sound("beep.mp3"))
                pause_state = False
                previous_songs = []
                current_song = ''
                next_songs = []
                playlist_mode = False

            elif new_order == 'A 4':# previous
                if previous_songs:
                    if current_song:
                        next_songs.insert(0, current_song)
                        previous_songs[0] = current_song
                        previous_songs.pop(0)
                        system_sound.play(mixer.Sound("beep.mp3"))
                        music_sound.play(mixer.Sound(current_song))
                    else:
                        current_song = previous_songs[0]
                        previous_songs.pop(0)
                        system_sound.play(mixer.Sound("beep.mp3"))
                        music_sound.play(mixer.Sound(current_song))
                else:
                    system_sound.play(mixer.Sound("beep.mp3"))
                    music_sound.play(mixer.Sound(current_song))
                pass

            elif new_order == 'A 5':# next
                if playlist_mode == True:
                    if current_song:
                        if next_songs:
                            previous_songs.insert(0, current_song)
                            current_song = next_songs[0]
                            next_songs.pop(0)
                            system_sound.play(mixer.Sound("beep.mp3"))
                            music_sound.play(mixer.Sound(current_song))
                pass

            elif new_order == 'A 6': #playlist mode ON
                if playlist_mode == False:
                    playlist_mode = True
                    system_sound.play(mixer.Sound("beep.mp3"))

            elif new_order == 'A 7': # feeling lucky
                new_order, _ = random.choice(list(music_lib.owned_cards.items()))

            elif new_order == 'A 10':
                music_lib.library()

            elif new_order != 'A 0': # PLAY MUSIC
                song_to_play = music_lib.find_music_path_from_library(new_order)
                if song_to_play:
                    if playlist_mode == False:
                        if current_song:
                            previous_songs.insert(0, current_song)
                        current_song = song_to_play

                        system_sound.play(mixer.Sound("beep.mp3"))
                        music_sound.play(mixer.Sound(song_to_play))

                    if playlist_mode == True:

                        next_songs.append(song_to_play)
                        system_sound.play(mixer.Sound("beep.mp3"))

                    if not music_lib.is_card_owned(new_order):
                        music_lib.add_card_to_owned_collection(new_order)

            isplaying = music_sound.get_busy()

            if isplaying == 0 : # NOT PLAYING
                if next_songs:
                    current_song = next_songs[0]
                    next_songs.pop(0)
                    music_sound.play(mixer.Sound(current_song))
                else:
                    current_song = ''

        # free camera object and exit
        print("[INFO] cleaning up...")
        csv.close()
        cv2.destroyAllWindows()
        vs.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Welcome to Sam\'s Jukebox")
    parser.add_argument('-P', '--library_path', type=str, default = None,
                        help='Please provide the absolute path of the music library')

    args = parser.parse_args()
    if args.library_path:
        SamsJukebox.setup(args.library_path)
    SamsJukebox.run()




