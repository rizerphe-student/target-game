"""The game of target: the Ukrainian version."""
import random
from typing import List


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


def get_pure_user_words(
    user_words: List[str], letters: List[str], words_from_dict: List[str]
) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    """
    # 1. The word must contain at least 4 letters
    words = {word for word in user_words if len(word) >= 4}
    # 2. The word must contain the central letter
    central = letters[len(letters) // 2]
    words = {word for word in words if central in word}
    # 3. The word must only contain the letters in the grid
    # (and at most as many of each letter as there are in the grid)
    words = {
        word
        for word in words
        if all(word.count(letter) <= letters.count(letter) for letter in word)
    }
    # 4. The word must not be in the dictionary
    words = {word for word in words if word not in words_from_dict}
    return list(words)


def results():
    """Prints the results of the game.

    1. Generate the grid
    2. Show the grid
    3. Get the words from the user
    4. Show all possible words
    5. Show the words that the user entered
    6. Show the words that are not in the dictionary
    7. Save the summary to results.txt
    """
    grid = generate_grid()
    for row in grid:
        print(" ".join(row))
    user_words = get_user_words()

    letters = sum(grid, start=[])
    letters = [letter.lower() for letter in letters]

    dictionary = get_words("en", letters)
    str_dict = ", ".join(dictionary)
    summary = f"Possible words: {str_dict}\n"
    str_user_words = ", ".join(user_words)
    summary += f"User words: {str_user_words}\n"
    pure_user_words = get_pure_user_words(user_words, letters, dictionary)
    str_pure_user_words = ", ".join(pure_user_words)
    summary += f"Pure user words: {str_pure_user_words}\n"

    with open("results.txt", "w", encoding="utf-8") as file:
        file.write(summary)

    print(summary)
