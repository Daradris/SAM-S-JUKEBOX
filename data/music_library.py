import os
import json
# hash : song _ data : track number title album Artist

import hashlib

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


class MusicLibrary:

    HASH_MAX_LENGTH = 10

    def __init__(self, filepath):
        self.library_filepath = filepath
        self.owned_cards = {}
        self.music_files = ()

    def setup(self):
        self.music_files = {}
        for root, _, files in os.walk(self.library_filepath):
            for file in files:
                if file.endswith(".mp3"):
                    music_filepath = os.path.join(root, file)
                    song_info = MP3(music_filepath, ID3=EasyID3)
                    stringf = "{0} - {1} - {2} - {3}".format(
                        song_info['tracknumber'][0],
                        song_info['title'][0],
                        song_info['album'][0],
                        song_info['artist'][0]
                    )
                    hasheds = str(self.song_hash(stringf))
                    self.music_files[hasheds] = music_filepath
        with open("data/library.json", 'w', encoding ='utf8') as json_file:
            json.dump(self.music_files, json_file, ensure_ascii = False, indent=4)

    def song_hash(self, song_info):
        hash_object = hashlib.md5(song_info.encode())
        return hash_object.hexdigest()[0:self.HASH_MAX_LENGTH]

    def load(self):
        filepath = "data/library.json"
        if os.stat(filepath).st_size == 0:
            self.music_files = {}
        else:
            open_file = open(filepath)
            self.music_files = json.load(open_file)
            open_file.close()

    def find_music_path_from_library(self, hashcode):
        return self.music_files.get(hashcode, '')

    def read_collected_cards(self):
        filepath = "data/collected_cards.json"
        if os.stat(filepath).st_size == 0:
            self.owned_cards = {}
        else:
            open_file = open(filepath)
            self.owned_cards = json.load(open_file)
            open_file.close()

    def is_card_owned(self, hashcode):
        return self.music_files.get(hashcode, '')

    def add_card_to_owned_collection(self, hashcode):
        self.owned_cards[hashcode] = self.music_files[hashcode]

