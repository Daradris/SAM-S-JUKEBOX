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
        self.drop_table_if_exist()
        self.create_library()

    def drop_table_if_exist(self):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        conn.execute( ''' DROP TABLE IF EXISTS library ''')
        conn.commit()
        conn.close()

    def create_library(self):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        conn.execute('''CREATE TABLE library
                (hash_code  CHAR(32)   PRIMARY KEY  NOT NULL,
                 filepath   CHAR(250)               NOT NULL,
                 owned      INT                     NOT NULL);''')
        conn.commit()
        conn.close()

    def update(self):
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
                                song_info['albumartist'][0]
                            )
                            print(stringf)
                            hasheds = str(self.song_hash(stringf))
                            query = '''
                            UPDATE library SET filepath="%s" WHERE hash_code="%s"
                            ''' % (music_filepath, hasheds)
                            result = conn.execute(query)
                            if result.rowcount > 0:
                                print('Existing row updated.')
                            else:
                                query = '''
                                        INSERT INTO library (hash_code, filepath, owned) VALUES ("%s","%s", 0)
                                        ''' % (hasheds, music_filepath)
                                conn.execute(query)
        conn.commit()
        conn.close()

    def song_hash(self, song_info):
        hash_object = hashlib.md5(song_info.encode())
        return hash_object.hexdigest()

    def find_music_path_from_library(self, hashcode):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        query = """
                SELECT filepath, owned FROM library WHERE hash_code = '%s'
                """ % sqlescape(hashcode)
        cursor = conn.execute(query)
        filepath = ''
        owned = 0
        myresult = cursor.fetchone()
        if myresult:
            filepath=myresult[0]
            owned = myresult[1]
        conn.close()
        return filepath, owned

    def get_random_owned_card(self):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        query = """
                SELECT filepath FROM library WHERE owned =1 ORDER BY RANDOM() LIMIT 1;
                """
        cursor = conn.execute(query)
        filepath = ''
        myresult = cursor.fetchone()
        if myresult:
            filepath=myresult[0]
        conn.close()
        return filepath

    def add_card_to_owned_collection(self, hashed_qr_code):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        query = """
        UPDATE library SET owned=1 WHERE hash_code='%s'
        """ % hashed_qr_code
        conn.execute(query)
        conn.commit()
        conn.close()

    def remove_card_from_library(self, hash_code):
        conn = sqlite3.connect(self.LIBRARY_DB_PATH)
        query = """
        UPDATE library SET owned=0 WHERE hash_code='%s'
        """ % hash_code
        conn.execute(query)
        conn.commit()
        conn.close()
