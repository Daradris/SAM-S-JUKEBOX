import configparser

class Setting:

    INI_FILEPATH = 'system_setting/option.ini'

    @staticmethod
    def set_library_path(music_library_path):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {}
        config['PATH'] = {}
        config['PATH']['MUSIC_LIBRARY'] = music_library_path

        with open(Setting.INI_FILEPATH, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def library_path():
        config = configparser.ConfigParser()
        config.read(Setting.INI_FILEPATH)
        return config['PATH']['MUSIC_LIBRARY']
