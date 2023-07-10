# Command Line Wordle
Recreation of [Wordle](https://www.nytimes.com/games/wordle/index.html) by Josh Wardle that is played in the command line.
Includes multiple wordsets, unlimited plays, and stat tracking.

## Introduction
Core functionality of game comes from a [youtube video](https://www.youtube.com/watch?v=NCgN4qtbh2Q&ab_channel=Replit) and code by [JacobLower3](https://replit.com/@JacobLower3/wordle-tutorial). 
The goal of this program is to add features to the existing code to make it a more fleshed out game.


## Requirements

Program built using Python 3.11.2

External modules outlined in `requirements.txt` and were installed using pip:

```
pip install matplotlib
pip install termcolor
```


## Added/Modified Features

The following features were added to [JacobLower3's](https://replit.com/@JacobLower3/wordle-tutorial) original code:
- display alphabet after each guess with letters printed in appropriate color
- print different win messages based on how many guesses it took to get correct answer
- retrive words from a text file rather than Natural Language Toolkit
- track player stats and record them in JSON files
- ability to display player stats in a nice graphic using matplotlib
- created tool to pull all five letter words from a text file and format them in a wordlist to be used in game
- added 5 total wordsets to game. Players can select which wordset they'd like to use in an in-game menu
- implemented wordsets using OOP to allow for easy inclusion of new sets


## Documentation


## License

This program uses MIT license
