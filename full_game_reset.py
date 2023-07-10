import json
from os import listdir


def reset_streak_data():
    streak_dict = {
    'current' : 0,
    'max' : 0,
    }

    with open("streak_data.json", "w") as outfile:
        json.dump(streak_dict, outfile)
    print('... Streaks Reset ...')


def reset_stats():
    stats_dict = {
    1 : 0,
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0,
    'Failed' : 0,
    }

    with open("stats.json", "w") as outfile:
        json.dump(stats_dict, outfile)
    print('... Stats Reset ...')


def _recombine_single(filename : str):
    ''' moves all words from a USED set to its corresponding active set'''
    #build list of all words in used wordset
    used_wordlist = []
    with open("used_wordsets/" + filename[:-4] + '_USED.txt', 'r') as f:
        for word in f:
            word.strip()
            used_wordlist.append(word)

    #clear used wordset
    with open("used_wordsets/" + filename[:-4] + '_USED.txt', 'w') as f:
        pass
    
    #append used word list to the unused wordset
    with open("wordsets/" + filename, 'a') as f:
        for word in used_wordlist:
            f.write(word)


def recombine_all():
    files = listdir('wordsets')
    for f in files:
        _recombine_single(f)
    print('... Used Words put back in original sets ...')


if __name__ == '__main__':
    reset_streak_data()
    reset_stats()
    recombine_all()
    print('Reset Complete.')