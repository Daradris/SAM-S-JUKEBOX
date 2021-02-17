from pygame import mixer

if __name__ == '__main__':
    mixer.init()
    music_sound = mixer.Channel(0)
    system_sound = mixer.Channel(1)
    system_sound.play(mixer.Sound("beep.mp3"))

    pause_state = False
    previous_songs = []

    current_song = ''
    next_songs = []
    playlist_mode = False

    while True:
        #cleanup_steps
        previous_songs = previous_songs[0:5]


        isplaying = music_sound.get_busy()
        print("Press 'p' to pause")
        print("Press 'r' to resume")
        print("Press 'v' set volume")
        print("Press 'e' to exit")
        print(isplaying)
        print("current song being played", current_song)
        print("played songs ", previous_songs)
        print("next songs to play", next_songs)
        # mqr code detection


        qr_code_input = input("['p','r','v','e']>>>")
        if qr_code_input == "p":
            current_song = "15 - All Along the Watchtower.mp3"
            music_sound.play(mixer.Sound(current_song))
        elif qr_code_input == "e":
            music_sound.stop()
            break

        if qr_code_input == 'A 1':# play/ unpause
            if current_song != '':
                if pause_state == True:
                    system_sound.play(mixer.Sound("beep.mp3"))
                    music_sound.unpause()
                    pause_state = False
            pass

        elif qr_code_input == 'A 2':# PAUSE
            if current_song != '':
                if pause_state == False:
                    music_sound.pause()
                    system_sound.play(mixer.Sound("beep.mp3"))
                    pause_state = True
                pass

        elif qr_code_input == 'A 3': # STOP
            if current_song != '':
                if pause_state == False:
                    music_sound.pause()
                    system_sound.play(mixer.Sound("beep.mp3"))
            pause_state = False
            previous_songs = []
            current_song = ''
            next_songs = []
            playlist_mode = False

        elif qr_code_input == 'A 4':# previous
            if previous_songs:
                if current_song:
                    next_songs.insert(0, current_song)
                    previous_songs[0] = current_song
                    previous_songs.pop(0)
                    system_sound.play(mixer.Sound("beep.mp3"))
                    music_sound.play(mixer.Sound(current_song))
                else:
                    current_song = previous_songs[0]
                    previous_songs.pop(0)
                    system_sound.play(mixer.Sound("beep.mp3"))
                    music_sound.play(mixer.Sound(current_song))
            else:
                system_sound.play(mixer.Sound("beep.mp3"))
                music_sound.play(mixer.Sound(current_song))
            pass

        elif qr_code_input == 'A 5':# next
            if playlist_mode == True:
                if current_song:
                    if next_songs:
                        previous_songs.insert(0, current_song)
                        current_song = next_songs[0]
                        next_songs.pop(0)
                        system_sound.play(mixer.Sound("beep.mp3"))
                        music_sound.play(mixer.Sound(current_song))
            pass

        elif qr_code_input == 'A 6': #playlist mode ON
            if playlist_mode == False:
                playlist_mode = True
                system_sound.play(mixer.Sound("beep.mp3"))


        elif qr_code_input == 'A 7':
            #feeling lucky
            pass

        elif qr_code_input.startswith('M'):
            song_to_play = qr_code_input.split(' ')[1]
            print (song_to_play)
            if playlist_mode == False:
                song_to_play = song_to_play + ".mp3"
                if current_song:
                    previous_songs.insert(0, current_song)
                current_song = song_to_play

                system_sound.play(mixer.Sound("beep.mp3"))
                music_sound.play(mixer.Sound(song_to_play))

            if playlist_mode == True:
                song_to_play = song_to_play + ".mp3"
                next_songs.append(song_to_play)
                system_sound.play(mixer.Sound("beep.mp3"))
            pass



        isplaying = music_sound.get_busy()

        if isplaying == 0 : # NOT PLAYING
            if next_songs:
                current_song = next_songs[0]
                next_songs.pop(0)
                music_sound.play(mixer.Sound(current_song))
            else:
                current_song = ''







