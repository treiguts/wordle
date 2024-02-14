import os
import string
import json
import random

from color import ColoredPrinter
from letter import GuessedLetters, ConsumedLetters


MAX_ALLOWED_GUESSES = 6
VALID_LETTERS = string.ascii_uppercase


class WordleGame(object):
    def __init__(self):
        with open('words.json', 'r') as file:
            self.word_pool = json.load(file)
        self.word_pool = [x.upper() for x in self.word_pool]

        self.secret_word = random.choice(self.word_pool)
        self.guessed_words = []
        self.guesses_remaining = MAX_ALLOWED_GUESSES

        self.correct_printer = ColoredPrinter('White/Green')
        self.close_printer = ColoredPrinter('White/Yellow')
        self.missed_printer = ColoredPrinter('White/DarkGray')
        self.unplayed_printer = ColoredPrinter('White/LightGray')

        self.guessed_letters = GuessedLetters(
            self.correct_printer,
            self.close_printer,
            self.missed_printer,
            self.unplayed_printer)

        self.last_played_word = None


    def run(self):
        os.system('cls')
        while True:
            if self.guesses_remaining == 0:
                print('No more guesses. You lost :(')
                break
            if self.play_next_round():
                self.guesses_remaining = self.guesses_remaining - 1

                if self.last_played_word == self.secret_word:
                    print('You won!')
                    break


    def play_next_round(self):
        word = self.read_input()

        print(f'You guessed \'{word}\'')
        if len(word) < 5:
            print(f'Word too short - {len(word)}')
            self.render_board()
            return False

        if not self.is_word_valid(word):
            print('Your guessed word is not in word pool. This doesn\'t count!')
            self.render_board()
            return False

        consumed_letters = ConsumedLetters(self.secret_word)
        letter_printers = []

        for guessed_c, secret_c in zip(word, self.secret_word):
            if secret_c == guessed_c:
                consumed_letters.consume_letter(guessed_c)
                letter_printers.append(self.correct_printer)
                self.guessed_letters.correct_letter(guessed_c)
            else:
                if guessed_c in self.secret_word and not consumed_letters.is_consumed(guessed_c):
                    consumed_letters.consume_letter(guessed_c)
                    letter_printers.append(self.close_printer)
                    self.guessed_letters.close_letter(guessed_c)
                else:
                    letter_printers.append(self.missed_printer)
                    self.guessed_letters.missed_letter(guessed_c)

        self.guessed_words.append((word, letter_printers))

        self.render_board()
        self.last_played_word = word
        return True


    def read_input(self):
        # print('Secret word is ' + self.secret_word)

        tries = 'tries' if self.guesses_remaining > 1 else 'try'
        word = input(f'\n> You have {self.guesses_remaining} {tries} remaining. Enter yor guess: ')
        os.system('cls')

        word = word.upper()
        word = ''.join([x for x in word if x in VALID_LETTERS])
        word = word[:5]

        return word


    def render_board(self):
        print('')

        for i in range(MAX_ALLOWED_GUESSES):
            if i < len(self.guessed_words):
                word, letter_printers = self.guessed_words[i]
                s = ''
                for letter, printer in zip(word, letter_printers):
                    s = s + printer(f' {letter} ')
                print(s)
            else:
                print('')

        print('\nGuessed letters:')
        self.guessed_letters.draw()
        print('')


    def is_word_valid(self, word):
        return word in self.word_pool


if __name__ == '__main__':
    game = WordleGame()
    game.run()
