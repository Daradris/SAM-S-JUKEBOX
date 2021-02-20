import os
import configparser

class Setting:

    INI_FILEPATH = 'system_setting/option.ini'
    PLAYLIST_FOLDER = 'Playlists'
    @staticmethod
    def set_library_path(music_library_path):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {}
        config['PATH'] = {}
        config['PATH']['MUSIC_LIBRARY'] = os.path.normpath(music_library_path)
        config['PATH']['PLAYLISTS'] = os.path.join(os.path.normpath(music_library_path), Setting.PLAYLIST_FOLDER)

        with open(Setting.INI_FILEPATH, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def library_path():
        config = configparser.ConfigParser()
        config.read(Setting.INI_FILEPATH)
        return config['PATH']['MUSIC_LIBRARY']

    @staticmethod
    def playlist_path():
        config = configparser.ConfigParser()
        config.read(Setting.INI_FILEPATH)
        return config['PATH']['PLAYLISTS']

