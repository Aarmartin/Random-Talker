# Written by: Aaron Martin
# Date: 10/7/2020
#
# Overall: Takes in NGram number and a desired number of sentences and input text and generates random sentences based on the NGram model
#
# Example:
# λ py talker.py 3 1 1342-0.txt 135-0.txt 1399-0.txt 2554-0.txt 2600-0.txt 863-0.txt
# great advantage over them .
# 
# Algorithm:
# 1: Take text as input
# 2: Format input text to separate punctuation, eliminate excess items and set to all lowercase
# 3: Store text as a list of tokens
# 4: If it is a Bigram:
# 		Create a dictionary, where each word is a key, whose value is a list of words that are immediate successors to the key in the sample texts
#	 If it is a Trigram:
#		Create a dictionary, where each pair of words is a key (ie. "The quick brown fox" ["The quick", "quick brown", "brown fox", "fox"]),
#		whose value is a list of words that are immediate successors to the key in the sample texts
# 5: If it is a Unigram:
#		Pick a random word from the token list and output it until an end character is reached
#	 If it is an N-gram where N > 1:
#		Pick a random word from the list of words that are at a specified key, based on the previous word, in the N-gram dictionary until an end character is reached

import sys
import re
import random

# Method for outputting Unigram Sentence
def createSentence(words, num):
	word = ""
	for i in range(num):
		
		# First word
		word = random.choice(words)
		while not re.match(r"[.!?]", word):
			print(word, end=" ")

			# Grab random word from list
			word = random.choice(words)
		print(word)

# Method for outputting Bigram Sentence
def createBiSentence(words, wordDict, num):
	word = ""
	for i in range(num):
		# First word
		word = random.choice(words)
		while not re.match(r"[.!?]", word):
			print(word, end=" ")

			# Grab random word from list at key 'word' in dictionary 'wordDict'
			word = random.choice(wordDict[word])
		print(word)


# Method for outputting Trigram Sentence
def createTriSentence(words, wordDict, num):
	word = ""
	for i in range(num):

		# First word
		word = random.choice(list(wordDict.keys()))
		while not re.search(r"[.!?]", word):

			# Split key value of format "{} {}" into a list of two words ["{}", "{}"]
			tokens = word.split()

			# Print first word of key
			print(tokens[0], end=" ")

			# Combine last word of key with a random word from list at key 'word' in dictionary 'wordDict'
			word = tokens[1] + " " +  random.choice(wordDict[word])
		print(word)

# Method for turning list of tokens into a Bigram Dictionary object
def makeBigram(words):
	biDict = {}

	for i in range(len(words)):

		# Establish word from list as key
		key = words[i]

		# Establish the next word in the list as nextWord
		nextWord = " ".join(words[i + 1:i + 2])

		# At key 'key' (create if not found) add 'nextWord' to value list
		biDict.setdefault(key, []).append(nextWord)

	return biDict

# Method for turning list of tokens into a Trigram Dictionary object
def makeTrigram(words):
	triDict = {}

	for i in range(len(words)):

		# Establish word and its immediate successor as key
		key = " ".join(words[i:i + 2])

		# Establish the next successor as nextWord
		nextWord = " ".join(words[i + 2:i + 3])

		# At key 'key' (create if not found) add 'nextWord' to value list
		triDict.setdefault(key, []).append(nextWord)

	return triDict

# Main function
def main(argv):

	# Take in input parameters
	# argv[1] == which style of ngram
	# argv[2] == amount of sentences to generate
	# argv[3:] == list of the rest of the input strings
	ngram = int(argv[1])
	numSen = int(argv[2])
	files = argv[3:]

	# Open and read all of the input files and add them to full
	full = ""
	for f in files:
		with open(f, "r") as file:
			full += file.read()

	# Format text to separate punctuation and remove unnecessary tokens
	result = re.sub(r"([.?!,])", r" \1", full).lower()
	result = re.sub(r"([^a-z.,?!])", '\n', result)

	# Turn text into list of tokens
	L = result.split()

	# Perform output
	if ngram == 1:
		createSentence(L, numSen)
	if ngram == 2:
		makeBigram(L)
		createBiSentence(L, makeBigram(L), numSen)
	if ngram == 3:
		makeTrigram(L)
		createTriSentence(L, makeTrigram(L), numSen)

main(sys.argv)	
