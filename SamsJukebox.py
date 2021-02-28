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
        music_player = MusicPlayer()
        music_player.beep()

    @staticmethod
    def run():
        music_library = MusicLibrary(Setting.library_path())

        qr_reader = QRReader()

        music_player = MusicPlayer()

        while True:
            # QR CODE
            detected_qr_code = qr_reader.read()
            music_player.clear_history()

            if detected_qr_code == Controller.UPDATE_LIBRARY:
                music_player.pause()
                music_player.beep()
                music_library.setup()
                music_player.beep()
                music_player.unpause()

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
                music_player.play_song(random.choice(list(music_library.owned_cards.items())))

            elif detected_qr_code != Controller.DEFAULT:
                song_to_play = music_library.find_music_path_from_library(detected_qr_code)


                #     kill_card = False
                if song_to_play:
                    music_player.play_song(song_to_play)


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
