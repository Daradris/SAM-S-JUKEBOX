import os
import json
import hashlib
import inspect
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import sqlite3
from sqlescapy import sqlescape

class MusicLibrary:

    HASH_MAX_LENGTH = 10
    LIBRARY_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)), 'library.db')

    def __init__(self, filepath):
        self.library_filepath = filepath

    def setup(self):

        self.kill_collection()
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        conn.execute('''CREATE TABLE library
                (hash_code  CHAR(32)   PRIMARY KEY  NOT NULL,
                 filepath   CHAR(250)               NOT NULL);''')

        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
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
                            print (hasheds, music_filepath)
                            query = """
                                   INSERT INTO library (hash_code, filepath) VALUES ('%s','%s')
                                """ % (hasheds, sqlescape(music_filepath))
                            conn.execute(query)
        conn.commit()
        conn.close()

    def song_hash(self, song_info):
        hash_object = hashlib.md5(song_info.encode())
        return hash_object.hexdigest()[0:self.HASH_MAX_LENGTH]

    def find_music_path_from_library(self, hashcode):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)

        query = """
                SELECT filepath FROM library WHERE hash_code = '%s'
                """ % sqlescape(hashcode)
        cursor = conn.execute(query)
        filepath = ''
        myresult = cursor.fetchone()
        if myresult:
            filepath=myresult[0]
        conn.close()
        return filepath

    def get_random_filepath(self):

        conn = sqlite3.connect(self.LIBRARY_DB_PATH)

        query = """
                SELECT filepath FROM library ORDER BY RANDOM() LIMIT 1;
                """
        cursor = conn.execute(query)
        filepath = ''
        myresult = cursor.fetchone()
        if myresult:
            filepath=myresult[0]
        conn.close()
        return filepath

    def kill_collection(self):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        conn.execute('''DROP TABLE library;''')
        conn.commit()
        conn.close()