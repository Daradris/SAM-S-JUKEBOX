from pygame import mixer

import datetime
from data import MusicLibrary
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import random
import time


import argparse

from system_setting import Setting
from library import QRReader, MusicPlayer

class SamsJukebox:

    @staticmethod
    def setup(library_path):
        Setting.set_library_path(library_path)
        music_library = MusicLibrary(Setting.library_path())
        music_library.setup()

    @staticmethod
    def run():
        music_library = MusicLibrary(Setting.library_path())
        music_library.load()
        qr_reader = QRReader()

        # MUSIC
        mixer.init()
        music_sound = mixer.Channel(0)
        system_sound = mixer.Channel(1)
        system_sound.play(mixer.Sound("system_setting/beep.mp3"))

        pause_state = False
        previous_songs = []
        current_song = ''
        next_songs = []
        playlist_mode = False
        music_player = MusicPlayer()
        while True:
            # QR CODE
            detected_qr_code = qr_reader.read()

            music_player.clear_history()

            if detected_qr_code == 'A 1':# play/ unpause
                music_player.unpause()

            elif detected_qr_code == 'A 2':# PAUSE
                music_player.pause()


            elif detected_qr_code == 'A 3': # STOP
                if current_song != '':
                    if pause_state == False:
                        music_sound.pause()
                        time.sleep(2.0)
                        system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                pause_state = False
                previous_songs = []
                current_song = ''
                next_songs = []
                playlist_mode = False

            elif detected_qr_code == 'A 4':# previous
                if previous_songs:
                    if current_song:
                        next_songs.insert(0, current_song)
                        previous_songs[0] = current_song
                        previous_songs.pop(0)
                        system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                        time.sleep(2.0)
                        music_sound.play(mixer.Sound(current_song))
                    else:
                        current_song = previous_songs[0]
                        previous_songs.pop(0)
                        system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                        time.sleep(2.0)
                        music_sound.play(mixer.Sound(current_song))
                else:
                    system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                    time.sleep(2.0)
                    music_sound.play(mixer.Sound(current_song))
                pass

            elif detected_qr_code == 'A 5':# next
                if playlist_mode == True:
                    if current_song:
                        if next_songs:
                            previous_songs.insert(0, current_song)
                            current_song = next_songs[0]
                            next_songs.pop(0)
                            system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                            time.sleep(2.0)
                            music_sound.play(mixer.Sound(current_song))
                pass

            elif detected_qr_code == 'A 6': #playlist mode ON
                if playlist_mode == False:
                    playlist_mode = True
                    system_sound.play(mixer.Sound("system_setting/beep.mp3"))

            elif detected_qr_code == 'A 7': # feeling lucky
                detected_qr_code, _ = random.choice(list(music_library.owned_cards.items()))

            elif detected_qr_code == 'A 10':
                system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                music_library.setup()
                system_sound.play(mixer.Sound("system_setting/beep.mp3"))

            elif detected_qr_code != 'A 0': # PLAY MUSIC
                song_to_play = music_library.find_music_path_from_library(detected_qr_code)
                if song_to_play:
                    if playlist_mode == False:
                        if current_song:
                            previous_songs.insert(0, current_song)
                        current_song = song_to_play

                        system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                        time.sleep(2.0)
                        music_sound.play(mixer.Sound(song_to_play))

                    if playlist_mode == True:

                        next_songs.append(song_to_play)
                        system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                    if not music_library.is_card_owned(detected_qr_code):
                        music_library.add_card_to_owned_collection(detected_qr_code)

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
        qr_reader.stop()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Welcome to Sam\'s Jukebox")
    parser.add_argument('-P', '--library_path', type=str, default = None,
                        help='Please provide the absolute path of the music library')

    args = parser.parse_args()
    if args.library_path:
        SamsJukebox.setup(args.library_path)
    SamsJukebox.run()




