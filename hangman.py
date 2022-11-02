# Problem Set 2, hangman.py
# Name: Artem Pikovets
# Collaborators: 🐋
# Time spent: who knows🤷

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program

wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    guessed_letters = set(letters_guessed)
    secret_word_letters = set(secret_word)
    
    result = False
    if secret_word_letters.intersection(guessed_letters) == secret_word_letters:
      result = True

    return result


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = ""

    for letter in secret_word:
      if letter in letters_guessed:
        result = result + letter
      else:
        result = result + "_ "

    return result


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase

    result = ""
    for letter in all_letters:
      if letter not in letters_guessed:
        result = result + letter

    return result


def is_vowel(letter):
  '''
  letter: one-element string, alphabetic letter
  returns: boolean, True if letter is vowel(a, e, i, o, and u. y does not count as a vowel.);
      False otherwise
  '''
  vowel_list = ['a', 'e', 'i', 'o', 'u']

  result = False
  if letter.lower() in vowel_list:
    result = True

  return result


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings_remaining = 3
    guesses_remaining = 6
    letters_guessed = []

    # start of the game:
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.") 
    print(f"You have {warnings_remaining} warnings left.")
    print("-------------")
    

    end = False
    while not end:

      print(f"You have {guesses_remaining} guesses left.")
      print(f"Available letters: {get_available_letters(letters_guessed)}")
      inp_letter = input("Please guess a letter: ")

      if (len(inp_letter) == 1) and (inp_letter.isalpha()):
        inp_letter = inp_letter.lower()

        if inp_letter in letters_guessed:
          # users input is incorrect
          warnings_remaining -= 1

          if warnings_remaining >= 0:
            print(f"Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: ", end = "")
          else:
            guesses_remaining -= 1
            print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess: ", end = "")

        else:
          # users input is correct
          letters_guessed.append(inp_letter)

          if inp_letter in secret_word:
            print("Good guess: ", end = "")
          else:
            print("Oops! That letter is not in my word: ", end = "")

            if is_vowel(inp_letter):
              # inp_letter is vowel
              guesses_remaining -= 2
              guesses_remaining = max(0, guesses_remaining)
            else:
              # inp_letter is consonant or 'y'
              guesses_remaining -= 1

      else:
        # users input is incorrect
        warnings_remaining -= 1

        if warnings_remaining >= 0:
          print(f"Oops! That is not a valid letter. You have {warnings_remaining} warnings left: ", end = "")
        else:
          guesses_remaining -= 1
          print("Oops! That is not a valid letter. You have no warnings left so you lose one guess: ", end = "")


      print(get_guessed_word(secret_word, letters_guessed))
      print("------------")
      
      if is_word_guessed(secret_word, letters_guessed):
        # user has won the game!

        unique_letters_count = len(set(secret_word))
        total_score = guesses_remaining * unique_letters_count
        print("Congratulations, you won!") 
        print(f"Your total score for this game is: {total_score}")
        end = True


      if (guesses_remaining <= 0) and (not end):
        # user has lost the game!

        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
        end = True
      




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    # delete all spaces from my_word
    my_word = my_word.replace(" ", "")
    
    result = True
    my_word_letters = set(my_word)

    if (len(my_word) != len(other_word)):
      result = False
    else:

      for i, ele in enumerate(my_word):
        if ele == "_":
          if other_word[i] in my_word_letters:
            result = False
        else:
          if ele != other_word[i]:
            result = False

    return result



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = list(filter(lambda x: match_with_gaps(my_word, x), wordlist))

    if len(matches) == 0:
      print("No matches found")
    else:
      print(" ".join(matches))



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings_remaining = 3
    guesses_remaining = 6
    letters_guessed = []

    # start of the game:
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.") 
    print(f"You have {warnings_remaining} warnings left.")
    print("-------------")
    

    end = False
    while not end:

      print(f"You have {guesses_remaining} guesses left.")
      print(f"Available letters: {get_available_letters(letters_guessed)}")
      inp_letter = input("Please guess a letter: ")

      if (len(inp_letter) == 1) and (inp_letter.isalpha()):
        inp_letter = inp_letter.lower()

        if inp_letter in letters_guessed:
          # users input is incorrect
          warnings_remaining -= 1

          if warnings_remaining >= 0:
            print(f"Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: ", end = "")
          else:
            guesses_remaining -= 1
            print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess: ", end = "")

        else:
          # users input is correct
          letters_guessed.append(inp_letter)

          if inp_letter in secret_word:
            print("Good guess: ", end = "")
          else:
            print("Oops! That letter is not in my word: ", end = "")

            if is_vowel(inp_letter):
              # inp_letter is vowel
              guesses_remaining -= 2
              guesses_remaining = max(0, guesses_remaining)
            else:
              # inp_letter is consonant or 'y'
              guesses_remaining -= 1

      else:
        if inp_letter != '*':
          # users input is incorrect
          warnings_remaining -= 1

          if warnings_remaining >= 0:
            print(f"Oops! That is not a valid letter. You have {warnings_remaining} warnings left: ", end = "")
          else:
            guesses_remaining -= 1
            print("Oops! That is not a valid letter. You have no warnings left so you lose one guess: ", end = "")
        else:
          # user wants to see all matches
          print("Possible word matches are: ")
          my_word = get_guessed_word(secret_word, letters_guessed)
          show_possible_matches(my_word)


      print(get_guessed_word(secret_word, letters_guessed))
      print("------------")
      
      if is_word_guessed(secret_word, letters_guessed):
        # user has won the game!

        unique_letters_count = len(set(secret_word))
        total_score = guesses_remaining * unique_letters_count
        print("Congratulations, you won!") 
        print(f"Your total score for this game is: {total_score}")
        end = True


      if (guesses_remaining <= 0) and (not end):
        # user has lost the game!

        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
        end = True



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
