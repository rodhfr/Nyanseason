import nltk
nltk.download('punkt_tab')  # Only need to download this once for word_tokenize

word = "ranma"
word_list = ["appare-ranman", "ranma 1/2", "dogaricious"]

# Tokenize each string in the list and check for exact matches
matches = [item for item in word_list if word in nltk.word_tokenize(item)]

# If there are matches, return the shortest match
if matches:
    print(min(matches, key=len))  # Select the shortest match
