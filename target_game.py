"""The game of target."""
from typing import List


def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    """
    pass


def get_words(path: str, letters: List[str]) -> List[str]:
    """
    Reads the dictionary. Checks the words with rules and returns a list of words.
    """
    # Read the dictionary file
    with open(path, "r", encoding="utf-8") as file:
        all_words = set(file.read().split("\n"))
    # Check the words with rules
    # 1. The word must contain at least 4 letters
    all_words = {word for word in all_words if len(word) >= 4}
    # 2. The word must contain the central letter
    central = letters[len(letters) // 2]
    all_words = {word for word in all_words if central in word}
    # 3. The word must only contain the letters in the grid
    # (and at most as many of each letter as there are in the grid)
    all_words = {
        word
        for word in all_words
        if all(word.count(letter) <= letters.count(letter) for letter in word)
    }
    return list(all_words)


def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish for *nix or Ctrl-Z+Enter
    for Windows.
    Note: the user presses the enter key after entering each word.
    """
    output = []
    while True:
        try:
            word = input()
        except EOFError:
            break
        else:
            output.append(word)
    return output


def get_pure_user_words(
    user_words: List[str], letters: List[str], words_from_dict: List[str]
) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    """
    pass


def results():
    pass
