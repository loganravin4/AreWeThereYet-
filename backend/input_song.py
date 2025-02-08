import re
def check_song_match(user_input, correct_song):
    # checks if the song from user input is correct or if there is any at that
    # if not user_input or not correct_song:
    #     return False 
    
    # removes punctuation and converts to lowercase for case-insensitive comparison


    user_input_cleaned = re.sub(r'\s+', ' ', user_input).strip().lower()
    correct_song_cleaned = re.sub(r'\s+', ' ', correct_song).strip().lower()

    print(f"User Input: '{user_input_cleaned}'")
    print(f"Correct Song: '{correct_song_cleaned}'")
    print(user_input_cleaned == correct_song_cleaned)
    
    return user_input_cleaned == correct_song_cleaned

    # return user_input.strip().lower() == correct_song.strip().lower()
