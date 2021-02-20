from pygame import mixer
import time

class MusicPlayer:
    def __init__(self):
        self.pause_state = False
        self.previous_songs = []
        self.current_song = ''
        self.next_songs = []
        self.playlist_mode = False

        mixer.init()
        self.music_sound = mixer.Channel(0)
        self.system_sound = mixer.Channel(1)
        self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))

    def unpause(self):
        if self.current_song != '':
            if self.pause_state == True:
                self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                time.sleep(2.0)

                self.music_sound.unpause()
                self.pause_state = False

    def clear_history(self):
        self.previous_songs = self.previous_songs[0:5]

    def pause(self):
        if self.current_song != '':
            if self.pause_state == False:
                self.music_sound.pause()
                time.sleep(2.0)
                self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                self.pause_state = True

    def stop(self):
        if self.current_song != '':
            if self.pause_state == False:
                self.music_sound.pause()
                time.sleep(2.0)
                self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
        self.pause_state = False
        self.previous_songs = []
        self.current_song = ''
        self.next_songs = []
        self.playlist_mode = False

    def play_previous(self):
        if self.previous_songs:
            if self.current_song:
                self.next_songs.insert(0, self.current_song)
                self.previous_songs[0] = self.current_song
                self.previous_songs.pop(0)
                self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                time.sleep(2.0)
                self.music_sound.play(mixer.Sound(self.current_song))
            else:
                self.current_song = self.previous_songs[0]
                self.previous_songs.pop(0)
                self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                time.sleep(2.0)
                self.music_sound.play(mixer.Sound(self.current_song))
        else:
            self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
            time.sleep(2.0)
            self.music_sound.play(mixer.Sound(self.current_song))

    def play_next(self):
        if self.playlist_mode == True:
            if self.current_song:
                if self.next_songs:
                    self.previous_songs.insert(0, self.current_song)
                    self.current_song = self.next_songs[0]
                    self.next_songs.pop(0)
                    self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
                    time.sleep(2.0)
                    self.music_sound.play(mixer.Sound(self.current_song))

    def switch_party_mode(self):
        if self.playlist_mode == False:
            self.playlist_mode = True
            self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))

    def play_song(self, song_filepath):
        if self.playlist_mode == False:
            if self.current_song:
                self.previous_songs.insert(0, self.current_song)
            self.current_song = song_filepath

            self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))
            time.sleep(2.0)
            self.music_sound.play(mixer.Sound(song_filepath))

        if self.playlist_mode == True:
            self.next_songs.append(song_filepath)
            self.system_sound.play(mixer.Sound("system_setting/beep.mp3"))

    def idle(self):
            isplaying = self.music_sound.get_busy()

            if isplaying == 0 : # NOT PLAYING
                if self.next_songs:
                    self.current_song = self.next_songs[0]
                    self.next_songs.pop(0)
                    self.music_sound.play(mixer.Sound(self.current_song))
                else:
                    self.current_song = ''

