import os
import random
class MusicLibrary:

    def __init__(self, filepath):
        self.library_filepath = filepath
        self.all_songs = None

    def get_song_filepath(self, detected_qr_code):
        return os.path.join(self.library_filepath, detected_qr_code)

    def get_random_song_from_library(self):
        if self.all_songs is None:
            self.all_songs = []
            for root, _, files in os.walk(self.library_filepath):
                for file in files:
                    if file.endswith(".mp3"):
                        self.all_songs.append(os.path.join(root, file))
        return random.choice(self.all_songs)
