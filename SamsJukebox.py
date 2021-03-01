import random
import argparse

from library import QRReader, MusicPlayer, Controller
from library.system_setting import Setting
from library.data import MusicLibrary

class SamsJukebox:

    @staticmethod
    def setup(library_path):
        Setting.set_library_path(library_path)
        music_library = MusicLibrary(Setting.library_path())
        music_library.setup()
        music_library.update()
        music_player = MusicPlayer()
        music_player.beep()

    @staticmethod
    def run():
        music_library = MusicLibrary(Setting.library_path())

        qr_reader = QRReader()

        music_player = MusicPlayer()
        kill_card = False

        while True:
            # QR CODE
            detected_qr_code = qr_reader.read()
            music_player.clear_history()

            if detected_qr_code == Controller.UPDATE_LIBRARY:
                music_player.pause()
                music_player.beep()
                music_library.update()
                music_player.beep()
                music_player.unpause()

            elif detected_qr_code == Controller.KILL_CARD:
                kill_card = True
                music_player.beep()

            elif detected_qr_code == Controller.KILL_COLLECTION:
                music_player.beep()
                music_library.kill_collection()

            elif detected_qr_code == Controller.UNPAUSE:
                music_player.unpause()

            elif detected_qr_code == Controller.PAUSE:
                music_player.pause()

            elif detected_qr_code == Controller.STOP:
                music_player.stop()

            elif detected_qr_code == Controller.PREVIOUS:
                music_player.play_previous()

            elif detected_qr_code == Controller.NEXT:
                music_player.play_next()

            elif detected_qr_code == Controller.PLAYLIST_SWITCH:
                music_player.switch_party_mode()

            elif detected_qr_code == Controller.FEELING_LUCK:
                music_player.play_song(music_library.get_random_owned_card())

            elif detected_qr_code != Controller.DEFAULT:
                import time

                start = time.time()
                print("hello")

                song_to_play, owned = music_library.find_music_path_from_library(detected_qr_code)
                end = time.time()
                print(end - start)
                print (song_to_play)
                if kill_card:
                    music_library.remove_card_from_library(detected_qr_code)
                    kill_card = False
                if song_to_play:
                    start = time.time()
                    print("hello")
                    music_player.play_song(song_to_play)
                    end = time.time()
                    print(end - start)
                    print ('song_to_play')
                    if owned == 0:
                        music_library.add_card_to_owned_collection(detected_qr_code)

            music_player.idle()

        qr_reader.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Welcome to Sam\'s Jukebox")
    parser.add_argument('-P', '--library_path', type=str, default=None,
                        help='Please provide the absolute path of the music library')

    args = parser.parse_args()
    if args.library_path:
        SamsJukebox.setup(args.library_path)
    SamsJukebox.run()
