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
                music_player.stop()

            elif detected_qr_code == 'A 4':# previous
                music_player.play_previous()

            elif detected_qr_code == 'A 5':# next
                music_player.play_next()

            elif detected_qr_code == 'A 6':
                music_player.switch_party_mode()#playlist mode ON

            elif detected_qr_code == 'A 7': # feeling lucky
                detected_qr_code, _ = random.choice(list(music_library.owned_cards.items()))

            elif detected_qr_code == 'A 10':
                music_player.pause()
                music_library.setup()
                music_player.unpause()

            elif detected_qr_code != 'A 0': # PLAY MUSIC
                song_to_play = music_library.find_music_path_from_library(detected_qr_code)
                if song_to_play:
                    music_player.play_song(song_to_play)

                    if not music_library.is_card_owned(detected_qr_code):
                        music_library.add_card_to_owned_collection(detected_qr_code)

            music_player.idle()

        qr_reader.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Welcome to Sam\'s Jukebox")
    parser.add_argument('-P', '--library_path', type=str, default = None,
                        help='Please provide the absolute path of the music library')

    args = parser.parse_args()
    if args.library_path:
        SamsJukebox.setup(args.library_path)
    SamsJukebox.run()




