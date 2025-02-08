def check_song_match(user_input, correct_song):
    # checks if the song from user input is correct or if there is any at that
    if not user_input or not correct_song:
        return False 
    
    # removes punctuation and converts to lowercase for case-insensitive comparison
    return user_input.strip().lower() == correct_song.strip().lower()
