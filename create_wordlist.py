from string import ascii_lowercase, punctuation

def add_to_wordset(filepath : str, new_filename : str):
    with open(filepath, 'r') as f:
        raw_text = f.read()

    #replace all punctuation with spaces
    #this removes contractions, possesives, etc
    raw_text_clean = ''
    for ch in raw_text:
        if ch in punctuation: raw_text_clean += " "
        else: raw_text_clean += ch

    #remove everything thats not in alphabet from text
    #this is mostly for tab and newline breaks
    new_text = ''
    for ch in raw_text_clean.lower():
        if ch in ascii_lowercase + ' ': new_text += ch

    #Isolate 5 letter words
    full_word_list = new_text.split()
    word_list = [word for word in full_word_list if len(word) == 5]
    word_set = set(word_list) #convert to set to remove duplicates

    with open('wordsets/' + new_filename, 'a') as newFile:
        for word in word_set:
            newFile.write("\n" + word)


def remove_duplicates(wordset_filepath : str):
    with open(wordset_filepath, 'r') as f:
        words = set() #the set type doesn't allow duplicates
        for word in f:
            word.strip() #remove \n at end of line
            words.add(word)
        
    with open(wordset_filepath, 'w') as f: #reopen to delete old words
        for w in words:
            f.write(w)


### Make Star Wars wordset ###
# add_to_wordset('raw_text/new_hope.txt', 'star_wars.txt')
# add_to_wordset('raw_text/empire.txt', 'star_wars.txt')
# add_to_wordset('raw_text/jedi.txt', 'star_wars.txt')
# add_to_wordset('raw_text/phantom_menace.txt', 'star_wars.txt')
# add_to_wordset('raw_text/aotc.txt', 'star_wars.txt')
# add_to_wordset('raw_text/revenge.txt', 'star_wars.txt')
# remove_duplicates('wordsets/star_wars.txt')

### Make Shrek Wordset ###
# add_to_wordset('raw_text/shrek.txt', 'shrek_movies.txt')
# add_to_wordset('raw_text/shrek2.txt', 'shrek_movies.txt')
# add_to_wordset('raw_text/shrek3.txt', 'shrek_movies.txt')
# add_to_wordset('raw_text/shrek4.txt', 'shrek_movies.txt')
# remove_duplicates('wordsets/shrek_movies.txt')

