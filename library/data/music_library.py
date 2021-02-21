import os
import json
import hashlib
import inspect
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


class MusicLibrary:

    HASH_MAX_LENGTH = 10
    LIBRARY_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)), 'library.json')
    COLLECTED_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)), 'collected_cards.json')

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
        with open(self.LIBRARY_JSON_PATH, 'w', encoding='utf8') as json_file:
            json.dump(self.music_files, json_file, ensure_ascii=False, indent=4)

    def song_hash(self, song_info):
        hash_object = hashlib.md5(song_info.encode())
        return hash_object.hexdigest()[0:self.HASH_MAX_LENGTH]

    def load(self):
        if os.stat(self.LIBRARY_JSON_PATH).st_size == 0:
            self.music_files = {}
        else:
            open_file = open(self.LIBRARY_JSON_PATH)
            self.music_files = json.load(open_file)
            open_file.close()

    def find_music_path_from_library(self, hashcode):
        return self.music_files.get(hashcode, '')

    def read_collected_cards(self):
        if os.stat(self.COLLECTED_JSON_PATH).st_size == 0:
            self.owned_cards = {}
        else:
            open_file = open(self.COLLECTED_JSON_PATH)
            self.owned_cards = json.load(open_file)
            open_file.close()

    def is_card_owned(self, hashcode):
        return self.music_files.get(hashcode, '')

    def add_card_to_owned_collection(self, hashcode):
        self.owned_cards[hashcode] = self.music_files[hashcode]
        self.save_collection()

    def remove_card_from_library(self, hashcode):
        self.owned_cards.pop(hashcode, None)
        self.save_collection()

    def save_collection(self):
        with open(self.COLLECTED_JSON_PATH, 'w', encoding='utf8') as json_file:
            json.dump(self.owned_cards, json_file, ensure_ascii=False, indent=4)

    def kill_collection(self):
        self.owned_cards = {}
        self.save_collection()