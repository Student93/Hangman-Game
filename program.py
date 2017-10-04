import numpy 
import re
import sys
import time
from collections import Counter
import collections

start_time = time.time()
start_time1 = time.time()
tt = 0.0
file = open("words_50000.txt","r")
words = (file.read()).split()
numLetters = 26
threshold = 6
numOfWords = len(words)
largestWord = max(words,key=len)
lenLargestWord = len(largestWord)
orderedDic = [[] for i in range(lenLargestWord)]
dictionary = []
firstGuess = []
generalOrder = numpy.zeros(numLetters)
board = []

for i in range(lenLargestWord):
	firstGuess.append('a')


def setGeneralOrder():
	for word in words:
		for i in range(numLetters):
			tempChr = chr(int(i+97))
			if tempChr in word:
				generalOrder[i] = generalOrder[i] + 1



	sortedListWithIndexes = sorted((k,j) for j,k in enumerate(generalOrder[:]))

	for j in range(numLetters):

		generalOrder[numLetters - j - 1] = sortedListWithIndexes[j][1]

	


def makeDictionary():
	global orderedDic
	global firstGuess
	for word in words:
		lenWord = len(word)
		orderedDic[lenWord-1].append(word)

	

	for i in range(lenLargestWord):
		tempDic = orderedDic[i-1][:]
		tempOrdered = collections.defaultdict(int)
		for word in tempDic:
		
			for tempChr in word:
				#i = ord(tempChr) - 97
				tempOrdered[tempChr] = tempOrdered[tempChr] + 1

		tempOrdered = sorted(tempOrdered.items(),key=lambda x:x[1])

		tempLen = len(tempOrdered)
		
		if tempLen != 0:
			firstGuess[i] = tempOrdered[tempLen-1][0]
		else:
			firstGuess[i] = firstGuess[i-1]
		


	


def findGuessesByFrequency():
	global dictionary
	global start_time
	global board
	
	pattern = ""
	boardStatus = board[:]
	#ordered = numpy.zeros(numLetters)
	ordered = collections.defaultdict(int)

	if unMatchedLetters:
		pattern = "[^"+ "".join(unMatchedLetters) + "]{"
	else:
		pattern = "[a-z]{"
	
	status = []
	temp = ""
	boardLen = len(boardStatus)
	#for i in range(boardLen):
	i = 0
	while i < boardLen:
		lenCount = 1
		#print i,boardLen
		if boardStatus[i][0] == "_":
			#boardStatus[i] = pattern + str(len(boardStatus[i])) + "}"
			temp = pattern 
			while i < boardLen-1 and boardStatus[i+1][0] ==boardStatus[i][0]:
				lenCount = lenCount + 1
				i = i + 1
			#print i
			temp = temp + str(lenCount) + "}"
			status.append(temp)
		else:
			status.append(boardStatus[i][0])
		i = i + 1


	
	status.append("$")
	
	patternReg = re.compile("".join(status))

	dictionary = [word for word in dictionary if patternReg.match(word) is not None]
	
	
	for word in dictionary:
		#word = list(set(word))
		for tempChr in word:
			#i = ord(tempChr) - 97
			ordered[tempChr] = ordered[tempChr] + 1

	ordered = sorted(ordered.items(),key=lambda x:x[1])
	


	orderLen = len(ordered)

	for i in range(orderLen-1,-1,-1):
		
		if ordered[i][0] not in board and ordered[i][0] not in unMatchedLetters:
			return ordered[i][0]

	for i in range(numLetters):
		tempChr = chr(int(generalOrder[i] + 97))
		if tempChr not in board and tempChr not in unMatchedLetters:
			return tempChr





def guess(guessThis, input):
	global words
	global unMatchedLetters
	global board
	wordLen = len(guessThis)
	missing = 0

	if wordLen > lenLargestWord:
		missedGuesses = " missed: "
		board = []
		for i in range(wordLen):
			board.append("_")
		actualWord = guessThis
		for i in range(numLetters):
			nextGuess = chr(int(generalOrder[i] + 97))
			if input == 1:
				print "".join(board), missedGuesses
				print "guess :", nextGuess
			if nextGuess in guessThis:

				indexList = [i for i, letter in enumerate(actualWord) if letter == nextGuess]
			
				#print "list",indexList
				#print "board",board
				for k in indexList:
					board[k] = nextGuess 

				guessThis = guessThis.replace(nextGuess,"")
				if len(guessThis) == 0:
					if input == 1:
						print "".join(board),missedGuesses
						print "Guessed word correctly!"
					return 1
			else:
				missedGuesses = missedGuesses + " " + nextGuess
				missing = missing + 1
				if missing == threshold:
					if input == 1:
						print "".join(board),missedGuesses
						print "Sorry! missed it."
					return 0



	else:
		# update dictionary according to length
		global dictionary
		#dictionary = [word for word in words if len(word) == wordLen]
		
		dictionary = orderedDic[wordLen-1][:]
		
		missedGuesses = " missed: "
		
		unMatchedLetters = []
		gameOver = 0
		board = []
		actualWord = guessThis
		for i in range(wordLen):
			board.append("_")

		# first guess
		
		nextGuess = firstGuess[wordLen-1]
		if input == 1:
			print "".join(board),missedGuesses
			print "guess: ",nextGuess

		if nextGuess in guessThis:
				
			indexList = [i for i, letter in enumerate(actualWord) if letter == nextGuess]
			
			#print "list",indexList
			#print "board",board
			for k in indexList:
				board[k] = nextGuess 
			
			guessThis = guessThis.replace(nextGuess,"")
			
			if len(guessThis) == 0:
				if input == 1:
					print "".join(board),missedGuesses
				return 1

		else:

			missedGuesses = missedGuesses + " " + nextGuess
			unMatchedLetters.append(nextGuess)
			
			missing = missing + 1
			if missing == threshold:
				return 0
		
		
		while gameOver == 0:
			
			
			nextGuess = findGuessesByFrequency()
			

			if input == 1:
				print "".join(board),missedGuesses
				print "guess: ",nextGuess
			#print nextGuess
			if nextGuess in guessThis:
				
				indexList = [i for i, letter in enumerate(actualWord) if letter == nextGuess]
				
				#print "list",indexList
				#print "board",board
				for k in indexList:
					board[k] = nextGuess 
				
				guessThis = guessThis.replace(nextGuess,"")
				
				if len(guessThis) == 0:
					if input == 1:
						print "".join(board),missedGuesses
						print "Guessed correctly!"

					return 1

			else:
				
				unMatchedLetters.append(nextGuess)
				missedGuesses = missedGuesses + " " + nextGuess
				missing = missing + 1
				if missing == threshold:
					if input == 1:
						print "".join(board),missedGuesses
						print "sorry missed it!"
					return 0
					
								
		


		
		



if __name__ == "__main__":
	correctGuesses = 0
	makeDictionary()
	setGeneralOrder()

	inputWord = str(sys.argv[1])

	# 1 signifies it's input word thus we have to print board status and missed guesses
	guess(inputWord,1)

	
	print "Testing on given dictionary..."
	
	for word in words:
		correctGuesses += guess(word,0)
		

	print "\nNumber of words tested: ", numOfWords
	print "Number of words guessed correctly: ", correctGuesses
	print "Correct Guesses (%): ", (float(correctGuesses)/numOfWords) * 100
	print "Time to run: ", (time.time() - start_time)
	

	# Enter test filename, It will print result after every 1000 iterations
	correctGuesses = 0
	iter = 0
	testFilename = input('\nEnter test filename: ')
	testFile = open(testFilename,"r")
	testWords = (testFile.read()).split()
	numOfWords = len(testWords)
	start_time = time.time()
	print "#words tested	guessed correctly"
	for word in testWords:
		correctGuesses += guess(word,0)
		iter = iter + 1
		if iter % 1000 == 0:
			print "   ",iter,"	   ",correctGuesses
			

	print "\nNumber of words tested: ", numOfWords
	print "Number of words guessed correctly: ", correctGuesses
	print "Correct Guesses (%): ", (float(correctGuesses)/numOfWords) * 100
	print "Time to run: ", (time.time() - start_time)




