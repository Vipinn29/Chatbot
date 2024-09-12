from better_profanity import profanity

def filter_profanity(text):
    profanity.load_censor_words()  # Load default bad words list
    return profanity.censor(text)
