"""The game of target: the Ukrainian version."""
import random
from typing import List, Literal


def generate_grid() -> List[str]:
    """
    Generates list of 5 unique lowercase letters - i.e. grid for the game.
    """
    alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    letters = random.sample(alphabet, 5)
    return letters


def get_words(path: str, letters: List[str]) -> List[tuple[str, str]]:
    """
    Reads the dictionary. Checks the words with rules and returns a list of words.
    """
    # Read the dictionary file
    with open(path, "r", encoding="utf-8") as file:
        words = {
            (
                word.strip(),
                [
                    f_part
                    for abbreviation, f_part in (
                        ("n", "noun"),
                        ("v", "verb"),
                        ("adj", "adjective"),
                        ("adv", "adverb"),
                    )
                    if part.strip("/").startswith(abbreviation)
                ][0],
            )
            for line in file
            if (word := line.split(" ")[0])
            and (part := line.split(" ")[1])
            and any(part.strip("/").startswith(tag) for tag in ("n", "v", "adj", "adv"))
            and len(word) <= 5
            and any(word.startswith(letter) for letter in letters)
        }
    return sorted(words)


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
            word = input().lower()
        except EOFError:
            break
        else:
            output.append(word)
    return output


def check_user_words(
    user_words: List[str],
    language_part: Literal["noun", "verb", "adjective", "adverb"],
    letters: List[str],
    dict_of_words: List[tuple[str, str]],
) -> tuple[List[str], List[str]]:
    """Check the given words against a dictionary
    and returns a tuple of two lists: correct and missed words."""
    user_words = [
        word
        for word in user_words
        if any(word.startswith(letter) for letter in letters)
    ]
    correct_words = []
    for word in user_words:
        dict_entries = [entry for entry in dict_of_words if entry[0] == word]
        if dict_entries:
            if any(part == language_part for _, part in dict_entries):
                correct_words.append(word)
    missed_words = [
        word
        for word, part in dict_of_words
        if word not in correct_words and part == language_part
    ]
    return correct_words, missed_words


def results():
    """Play the game

    1. Generate the letters
    2. Generate the language part
    3. Ask user for input
    4. Output the summary
    """
    letters = generate_grid()
    language_part = random.choice(["noun", "verb", "adjective", "adverb"])
    print(f"Letters: {' '.join(letters)}")
    print(f"Language part: {language_part}")
    dict_of_words = get_words("base.lst", letters)
    user_words = get_user_words()
    correct_words, missed_words = check_user_words(
        user_words, language_part, letters, dict_of_words
    )
    print(f"Correct words: {', '.join(correct_words)}")
    print(f"Missed words: {', '.join(missed_words)}")


if __name__ == "__main__":
    results()
