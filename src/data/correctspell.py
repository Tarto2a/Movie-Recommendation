import nltk
from nltk.corpus import words
from nltk.metrics.distance import edit_distance
import string

# Download the English words corpus
nltk.download('words')

# Load the list of English words
word_list = set(words.words())

def correct_word(word):
    """
    Checks the spelling of a single word and suggests the closest match.
    :param word: The input word to check.
    :return: The closest correct word or the input word if it's already correct.
    """
    if word in word_list:
        return word  # The word is correct
    else:
        # Find the closest word in the dictionary
        closest_word = min(word_list, key=lambda w: edit_distance(word, w))
        return closest_word

def spell_checker(sentence):
    """
    Checks the spelling of a sentence and suggests corrections for each word.
    :param sentence: The input sentence to check.
    :return: The corrected sentence.
    """
    words_in_sentence = sentence.split()
    corrected_words = []

    for word in words_in_sentence:
        # Remove punctuation from the word for checking
        clean_word = word.strip(string.punctuation)
        corrected_word = correct_word(clean_word.lower())  # Handle case sensitivity
        # Add back the punctuation
        if word[-1] in string.punctuation:
            corrected_word += word[-1]
        corrected_words.append(corrected_word)

    return " ".join(corrected_words)

# Test the spell checker
input_sentence = input("Enter a sentence: ")
corrected_sentence = spell_checker(input_sentence)

print(f"Corrected sentence: {corrected_sentence}")
