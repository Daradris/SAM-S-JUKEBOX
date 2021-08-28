import pygame
import os, inspect, time

class MusicPlayer:
    BEEP_FILEPATH =  os.path.join(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)), 'system_setting', 'beep.mp3')

    def __init__(self):
        self.pause_state = False
        self.previous_songs = []
        self.current_song = ''
        self.next_songs = []
        self.playlist_mode = False
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.init()
        self.music_sound = pygame.mixer.Channel(0)
        self.system_sound = pygame.mixer.Channel(1)
        self.beep()

    def beep(self):
        self.system_sound.play(pygame.mixer.Sound(self.BEEP_FILEPATH))

    def unpause(self):
        if self.current_song != '':
            if self.pause_state == True:
                self.beep()
                time.sleep(1.0)
                self.music_sound.unpause()
                self.pause_state = False

    def clear_history(self):
        self.previous_songs = self.previous_songs[0:5]

    def pause(self):
        if self.current_song != '':
            if self.pause_state == False:
                self.music_sound.pause()
                time.sleep(1.0)
                self.beep()
                self.pause_state = True

    def stop(self):
        if self.current_song != '':
            if self.pause_state == False:
                self.music_sound.pause()
                time.sleep(1.0)
                self.beep()
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
            else:
                self.current_song = self.previous_songs[0]
                self.previous_songs.pop(0)
        if self.current_song:
            self.beep()
            time.sleep(1.0)
            self.music_sound.play(pygame.mixer.Sound(self.current_song))

    def play_next(self):
        if self.next_songs:
            self.previous_songs.insert(0, self.current_song)
            self.current_song = self.next_songs[0]
            self.next_songs.pop(0)

            self.music_sound.pause()
            self.beep()
            time.sleep(1.0)
            self.music_sound.play(pygame.mixer.Sound(self.current_song))

    def switch_party_mode(self):
        if self.playlist_mode == False:
            self.playlist_mode = True
            self.beep()

    def play_song(self, song_filepath):
        if self.current_song:
            self.previous_songs.insert(0, self.current_song)
            self.music_sound.pause()
        self.current_song = song_filepath
        self.beep()
        self.pause_state = False
        self.music_sound.play(pygame.mixer.Sound(song_filepath))

    def add_to_play_next(self, song_filepath):
        self.next_songs.append(song_filepath)
        self.beep()

    def idle(self):
        isplaying = self.music_sound.get_busy()
        if isplaying == 0: # NOT PLAYING
            self.current_song = ''
            if self.next_songs:
                self.current_song = self.next_songs[0]
                self.next_songs.pop(0)
                self.music_sound.play(pygame.mixer.Sound(self.current_song))
