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
