import random
import sys
from string import ascii_lowercase
import os
import json

from termcolor import colored
import matplotlib.pyplot as plt

#######################################
# Classes
#######################################
#handles the display of the colored alphabet after each word guess
class Alphabet:
    def __init__(self):
        self.alphabet_dict = dict.fromkeys(ascii_lowercase, 'white') #keys are letters, values are their colors

    def reset_alpha(self):
        self.alphabet_dict = dict.fromkeys(ascii_lowercase, 'white') #set all colors to white

    def print_alpha(self):
        print() #print new line before alphabet
        for key in self.alphabet_dict.keys():
            print(colored(key, self.alphabet_dict[key], "on_black"), end="")

    def modify_letter_color(self, letter: str, color: str):
        self.alphabet_dict[letter] = color
        

class Wordset:
    def __init__(self, key : str, filename : str, description : str):
        """
        Object that handles displaying the menu information for a wordset and
        switching to a wordset when needed

        Args:
            key (str): short string that user will type in to select the set
            filename (str): name of wordset text file in wordsets folder. DO NOT INCLUDE "wordsets/"
            description (str): description pf set that will appear in menu
        """
        self.__key = key
        self.__filename = filename
        self.__description = description
        
        self.__total_length, self.__used_length = self.get_lengths()

    def get_key(self):
        return self.__key

    def get_lengths(self):
        """
        Returns the length of the full wordset as well as the number of words that have 
        been used from that set

        Returns:
            tuple containing

            total (int) : Number of words in full set
            used (int) : Number of words used from set
        """
        unused_count = 0
        with open("wordsets/" + self.__filename, 'r') as f:
            for line in f:
                if line.strip():
                    unused_count += 1
    
        used_count = 0
        with open("used_wordsets/" + self.__filename[:-4] + '_USED.txt', 'r') as f:
            for line in f:
                if line.strip():
                    used_count +=1

        total = used_count + unused_count
        return total, used_count
    
    def print_menu_entry(self): 
        #Example of what this print statment looks like:
        #   'basic - standard word set. 57/2321
        print("\t" + self.__key + ' - ' + self.__description +
              " {0}/{1}".format(self.__used_length, self.__total_length))

    def make_active_set(self): #make this wordset the current wordset
        global current_wordset
        current_wordset = 'wordsets/' + self.__filename
        print("wordset changed to: {0}".format(self.__key))

#######################################
# Global variables
#######################################
GUESS_LIMIT = 6
State = 'Welcome' #initial state; not an actual game state, game will crash if not properly initialized
current_wordset = 'wordsets/words.txt'

#######################################
# Helper Functions
#######################################
######### General ##############
def clear_prev_line():
    sys.stdout.write('\x1b[1A') #move cursor to previous line
    sys.stdout.write('\x1b[2K') #clear line cursor is on


def print_green_word(word : str):
    print(colored(word, 'green', 'on_black'))

######### Wordsets ##############
def move_word_to_used_set(used_word : str):
    global current_wordset
    with open(current_wordset, 'r') as from_file:
        with open("used_wordsets/" + current_wordset[9:-4] + '_USED.txt', 'a') as to_file:
            unused_list = [] 
            for word in from_file:
                word = word.strip()
                if word != used_word: #the used word won't get recorded to be rewritten
                    unused_list.append(word) #make list of all words that weren't used

            to_file.write(used_word + "\n")
    
    with open(current_wordset, 'w') as f: #reopen to clear old file
        for w in unused_list:
            f.write(w + "\n") #write unused words onto file


######### Stat Tracking ##############
def get_stats_from_JSON() -> dict:
    with open("stats.json", 'r') as openfile: #load dict from json
        stats_dict = json.load(openfile)
    return stats_dict


def save_stats_to_JSON(stats_dict : dict):
    with open("stats.json", "w") as outfile:
        json.dump(stats_dict, outfile)

######### Streak Tracking ##############
def get_streaks_from_JSON() -> dict:
    with open("streak_data.json", 'r') as openfile: #load dict from json
        streak_dict = json.load(openfile)
    return streak_dict


def save_streaks_to_JSON(streak_dict : dict):
    with open("streak_data.json", "w") as outfile:
        json.dump(streak_dict, outfile)


def add_to_win_streak():
    streak_dict = get_streaks_from_JSON()
    streak_dict['current'] += 1
    if streak_dict['current'] > streak_dict['max']:
        streak_dict['max'] = streak_dict['current']
    save_streaks_to_JSON(streak_dict)


def break_win_streak():
    streak_dict = get_streaks_from_JSON()
    streak_dict['current'] = 0
    save_streaks_to_JSON(streak_dict)


#######################################
# Gameplay Functions
#######################################
def get_word():
    #pull random word from text file
    global current_wordset
    with open(current_wordset, "r") as f:
        words = f.read().split()
        return random.choice(words)


def print_win_message(attempt_number : int):
    response_dict = {
        1 : 'YOU GOT IT ON YOUR FIRST TRY!!!! THATS SO CRAZY',
        2 : 'You got the wordle in 2! Superb job',
        3 : 'You got the wordle in 3. Very Impressive',
        4 : 'You got the wordle in 4. Nice',
        5 : 'You got the wordle in 5',
        6 : 'You got the wordle in 6. Cutting it close!',
    }
    win_message = response_dict[attempt_number]
    print(colored("\n{0}".format(win_message), "blue", "on_black"))


def record_win(attempt_number : int):
    stats_dict = get_stats_from_JSON()
    
    attempt_key = str(attempt_number) #keys are str so need to convert
    stats_dict[attempt_key] += 1 #add to dictionary value

    save_stats_to_JSON(stats_dict)
    add_to_win_streak()


def record_loss():
    stats_dict = get_stats_from_JSON()
    stats_dict['Failed'] += 1
    save_stats_to_JSON(stats_dict)

    break_win_streak()


def play_game():
    play_allowed = True
    try:
        secret = get_word() #get new word
    except IndexError: #handles error if wordset is empty
        print("It looks like you've done every word in this set!\n"
              "Congrats!!!!!!!\n"
              "Try going to 'menu' and selecting a new set to continue playing.")
        play_allowed = False
    
    alpha = Alphabet()
    if play_allowed:
        for attempt in range(1, GUESS_LIMIT+1):
            guess = input().lower()

            clear_prev_line()
            if attempt != 1: clear_prev_line() #clears alphabet line

            #print each letter in guess with appropriate color
            for i in range( min(len(guess), 5) ):
                if guess[i] == secret[i]:
                    print(colored(guess[i], 'green', "on_black"), end="")
                    alpha.modify_letter_color(guess[i], 'green')
                elif guess[i] in secret:
                    print(colored(guess[i], 'yellow', "on_black"), end="")
                    alpha.modify_letter_color(guess[i], 'yellow')
                else:
                    print(colored(guess[i], 'white', "on_black"), end="")
                    alpha.modify_letter_color(guess[i], 'dark_grey')

            alpha.print_alpha()

            if guess == secret:
                move_word_to_used_set(secret)
                print_win_message(attempt)
                if current_wordset == 'wordsets/words.txt': record_win(attempt) #only record win for default set
                break

            print("") #print new line after word is printed

        else: #runs if for loop runs out naturally
            print(colored(f"You didn't get it :( ... The word was {secret}", 'red', 'on_black'))
            if current_wordset == 'wordsets/words.txt': record_loss()


#######################################
# Menu items
#######################################
def display_stats():
    ############# Setup ##############
    #get guess distribution
    stats_dict = get_stats_from_JSON()
    titles = list(stats_dict.keys())
    values = list(stats_dict.values())

    #retrive streak stats
    streak_dict = get_streaks_from_JSON()
    current_streak = streak_dict['current']
    max_streak = streak_dict['max']

    #calculate secondary stats
    played = sum(values)
    failed = stats_dict['Failed']
    if played == 0:
        win_percent = 0
    else:
        win_percent = int(((played-failed) / played) * 100)

    #plot setup
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(nrows= 2, ncols=1, height_ratios = [1, 3.5])

    ############# Summary Statistics ##############
    #Configure Plot
    ax1.set_title('STATISTICS', weight = 'bold')
    ax1.spines['top'].set_visible(False) #remove top border of plot area
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.get_yaxis().set_visible(False) #remove y ticks and labels
    ax1.get_xaxis().set_visible(False)

    #Display Summary Statistics
    numbers = [played, win_percent, current_streak, max_streak]
    labels = ['Played', 'Win %', 'Current\nStreak', 'Max\nStreak']
    for i in range(len(numbers)):     
        ax1.text(0.2*(i+1), 0.5, str(numbers[i]), ha='center', va='bottom', size = 'xx-large')
        ax1.text(0.2*(i+1), 0.5, labels[i], ha='center', va='top')

    ############# Guess Distribution ##############
    ax2.set_title('GUESS DISTRIBUTION', weight = 'bold')
    ax2.barh(range(len(stats_dict)), values, tick_label=titles, color = '#3A3A3C')
    ax2.invert_yaxis() #put bars in ascending order from top to bottom
    ax2.spines['top'].set_visible(False) #remove top border of bar chart
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.tick_params(left = False) #remove y ticks
    ax2.get_xaxis().set_visible(False) #remove x ticks and labels
    
    #put value labels at end of bars
    for i in range(len(stats_dict)):
        if values[i] > 0:
            plt.text(values[i] - 0.1, i, values[i],
                    ha='left', va='center', weight = 'bold')

    plt.show()


def menu():
    #create wordset objects that store the info for the menu
    basic = Wordset('basic', 'words.txt', 'standard word set.')
    past = Wordset('2022', '2022_words.txt', 'words that appeared as answers in 2022.')
    force = Wordset('force', "star_wars.txt", 'words from a galaxy far far away.')
    swamp = Wordset('swamp', 'shrek_movies.txt', "words from everyone's favorite ogre.")
    relax = Wordset('relax', 'common.txt', 'words from everyday vocabulary.')
    wordset_list = [basic, relax, past, force, swamp]

    #print menu items
    print("stats - display stats (stats only recorded for standard word set)\n", 
          "Word sets:")
    for words in wordset_list:
        words.print_menu_entry()

    choice = input('>>').lower()

    #create dictionary of possible menu choices and their functions
    options_dict = {'stats' : display_stats}
    for words in wordset_list:
        options_dict[words.get_key()] = words.make_active_set
    
    if choice in options_dict.keys():
        clear_prev_line()
        print_green_word(choice) #make valid choice green
        options_dict[choice]() #call function associated with choice


#######################################
# Game Structure
#######################################
def get_state():
    global State
    #get code for new state
    new = input('Type "menu" to see options, "q" to quit, or press enter to begin play >> ').lower()

    #use code to assign value to state variable
    if new == 'menu':
        State = 'menu'
    elif new == 'q':
        State = 'quit'
    else: State = 'play'
    os.system('cls')


def game_loop():
    global State
    get_state()
    while True:
        if State == 'play':
            play_game()
            get_state()
        elif State == 'menu':
            menu()
            get_state()
        elif State == 'quit':
            break
            

if __name__ == "__main__":
    print("Welcome to Wordle!")
    game_loop()