# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    # inFile: file
    inFile = open("D:\school\diseño de  programacion\words.txt", 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word,n):
    word=(word.lower())
    word_length=0
    primer_componente=0
    for letter in word:
        primer_componente+=SCRABBLE_LETTER_VALUES.get(letter,0)
        word_length+=1
    if 1 < (7*word_length-3*(n-word_length)):
        segundo_componente=7*word_length-3*(n-word_length)
    else:
        segundo_componente=1
    puntuacion=primer_componente*segundo_componente
        
                          
    return puntuacion

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#


def deal_hand(n):
    hand={}
    num_vowels = int(math.ceil(n / 4))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
        hand["*"]=1
    
    for i in range(num_vowels+1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#

def update_hand(hand, word):
    new_hand=hand.copy()
    word=word.lower()
    for letters in word:
        if word in  load_words() and letters in new_hand :
            
                if new_hand[letters]>=2 and letters in new_hand :
                    new_hand[letters]-=1
                elif new_hand[letters]<=1 and letters in new_hand:
                    new_hand[letters]=0
        elif word not in   load_words() or letters not in new_hand:
                if letters in new_hand and new_hand[letters]>=2:
                    new_hand[letters]-=1
                elif letters in new_hand and new_hand[letters]<=1:
                    new_hand[letters]=0
    return new_hand

# Problem #3: Test word validity
#
#validar palabras
def is_valid_word(word, hand, word_list):
    hand1=hand.copy()
    word1=word.lower()
    word_existe=False
    for letters in word1:
        if "*"in word and word_existe is False:
            for vocal in VOWELS:
                word_with_vowels=str(word.replace("*",vocal))
                
                if word_with_vowels in word_list :
                    word_existe=True
                    word1=word_with_vowels
                    break
        if hand1.get(letters,0)==0 or word1 not in word_list :
            word_existe=False
            break
        if letters in hand1   and hand1[letters]>=2 :
            hand1[letters]-=1
            word_existe=True
        elif letters in hand1  and hand1[letters]<=1 :
            hand1[letters]=0
            word_existe=True
    return word_existe
# Problem #5: Playing a hand
#
#calcular la longutid de la mano
def calculate_handlen(hand):
    n=0
    for letters in hand.keys():
        n+=hand[letters]
    return n
    


def play_hand(hand, word_list):
    puntuacion_total=0
    n=calculate_handlen(hand)
    while n != 0:
        display_hand(hand)
        word=input("Enter word, or !! to indicate that you are finished:").lower()
        if word =="!!":
            break
        else:
            if is_valid_word(word, hand, word_list):
                puntuacion=get_word_score(word,n)
                puntuacion_total+=puntuacion
                print(f"The word has a value of {puntuacion} points ,total score :{puntuacion_total}")
                hand=update_hand(hand, word)
            else:
                print("¡¡Attention!!, invalid word ;you will be penalized")
                hand=update_hand(hand, word)
            n=calculate_handlen(hand)
            if n==0 :
                print("¡¡The hand is empty!!")
    print(f" total score of hand={puntuacion_total}")
    return puntuacion_total

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    hand1=hand.copy()
    value=hand1[letter]
    letters=list(SCRABBLE_LETTER_VALUES.keys())
    letras_disponibles=[letter for letter in letters if letter not in hand1 or hand1[letter]!=value]
    sustitute_letter=random.choice(letras_disponibles)  
    hand1[sustitute_letter]=hand1.pop(letter)
    return hand1
    
       
    
def play_game(word_list):
    print("welcome to the word game ")
    hand_to_play=int(input("Enter total number of hands:"))
    total_score_all_hands=0
    n=int(input("enter hand size :"))
    for i in range(hand_to_play):
        print(f"hand {i}:")
        hand=deal_hand(n)
        display_hand(hand)
        choice=str(input("Would you like to substitute a letter?")).lower()
        if choice=="yes":
            letter=str(input("Which letter would you like to replace:")).lower()
            hand=substitute_hand(hand, letter)
        puntuacion_total=play_hand(hand, word_list)
        total_score_all_hands+=puntuacion_total
        opcion=str(input("Would you like to replay the hand?")).lower()
        if opcion =="yes":
            if choice=="no":
                display_hand(hand)
                choice=str(input("Would you like to substitute a letter?")).lower()
                if choice=="yes":
                    letter=str(input("Which letter would you like to replace:")).lower()
                    hand=substitute_hand(hand, letter)
            total_score_all_hands=0
            puntacion_total=play_hand(hand, word_list)
            total_score_all_hands+=puntuacion_total
    print(f"the total score for the series of hands {total_score_all_hands}")

    return total_score_all_hands







    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)