import random
import argparse
import time

from library import QRReader, MusicPlayer, Controller
from library.system_setting import Setting
from library.data import MusicLibrary

class SamsJukebox:

    @staticmethod
    def setup(library_path):
        setting = Setting.set_library_path(library_path)
        music_player = MusicPlayer()
        music_player.beep()

    @staticmethod
    def run():
        setting = Setting()
        music_library = MusicLibrary(setting)

        qr_reader = QRReader()

        music_player = MusicPlayer()
        is_update_library = False
        is_party_mode = False
        music_player.beep()

        while True:
            # QR CODE
            detected_qr_code = qr_reader.read()
            music_player.clear_history()

            if detected_qr_code != Controller.DEFAULT:
                music_player.beep()

            if detected_qr_code == Controller.UPDATE_LIBRARY:
                if is_update_library == True:
                    is_update_library = False
                else:
                    is_update_library = True

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
                if is_party_mode == True:
                    is_party_mode = False
                else:
                    is_party_mode = True

            elif detected_qr_code == Controller.FEELING_LUCK:
                detected_qr_code = music_library.get_random_song_from_library()
                if is_party_mode:
                    print("Playing Next Lucky: " + detected_qr_code)
                    music_player.add_to_play_next(detected_qr_code)
                else:
                    print("Playing Lucky: " + detected_qr_code)
                    music_player.play_song(detected_qr_code)

            elif detected_qr_code != Controller.DEFAULT:

                if is_update_library:
                    Setting.set_library_path(detected_qr_code)
                    music_library = MusicLibrary(Setting.set_library_path(detected_qr_code))
                    is_update_library = False
                    print('New Library Location: ' + detected_qr_code)
                else:
                    songs_to_play = music_library.get_songs_filepath(detected_qr_code)
                    for song in songs_to_play:
                        print("Playing Next: " + '\n'.join(songs_to_play))
                        music_player.add_to_play_next(song)
                    if not is_party_mode:
                        music_player.play_next()
                        print("Playing: " + songs_to_play[0])

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
