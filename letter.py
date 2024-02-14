import string

VALID_LETTERS = string.ascii_uppercase

class GuessedLetters(object):

    def __init__(self, correct_printer, close_printer, missed_printer, unplayed_printer):
        self._correct_printer = correct_printer
        self._close_printer = close_printer
        self._missed_printer = missed_printer
        self._unplayed_printer = unplayed_printer

        self._correct_letters = set()
        self._close_letters = set()
        self._missed_letters = set()

    def correct_letter(self, letter):
        if letter in self._close_letters:
            self._close_letters.remove(letter)
        if letter in self._missed_letters:
            self._missed_letters.remove(letter)
        self._correct_letters.add(letter)

    def close_letter(self, letter):
        if letter not in self._correct_letters:
            self._close_letters.add(letter)
            if letter in self._missed_letters:
                self._missed_letters.remove(letter)

    def missed_letter(self, letter):
        if letter not in self._correct_letters and letter not in self._close_letters:
            self._missed_letters.add(letter)

    def draw(self):
        s = ''
        for letter in VALID_LETTERS:
            printer = self._get_printer(letter)
            s = s + printer(f' {letter} ')
        print(s)

    def _get_printer(self, letter):
        if letter in self._correct_letters:
            return self._correct_printer

        if letter in self._close_letters:
            return self._close_printer

        if letter in self._missed_letters:
            return self._missed_printer

        return self._unplayed_printer



class ConsumedLetters(object):

    def __init__(self, secret_word):
        self._consumed_letters = {
                letter: [secret_word.count(letter), 0]
                for letter in set(secret_word)
            }

    def consume_letter(self, guessed_c):
        self._consumed_letters[guessed_c][1] = self._consumed_letters[guessed_c][1] + 1


    def is_consumed(self, guessed_c):
        max_occurences, guessed_count = self._consumed_letters[guessed_c]
        return guessed_count == max_occurences
