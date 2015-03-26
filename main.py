

import os, sys
from board import GameBoard
from ai import AIPlayer
import speech_recognition as sr

# Main program logic
board = GameBoard()
enemy = AIPlayer(1)

board.newGame()

r = sr.Recognizer()
voiceEnabled = 0

while 1:

	# UI 
	os.system("clear")
	board.drawBoard()

	# Player Move 
	validMove = 0
	while not validMove:

		if voiceEnabled is 1:
			with sr.Microphone() as source:                # use the default microphone as the audio source
				print "Speak now"
				audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
				print "Done recording"

			try:
				move = r.recognize(audio)
				moveStr = move[0:2] + "-" + move[3:5]
				print ("You said: " + moveStr)
				validMove = board.performPlayerMove(moveStr)
			except LookupError:
				print "Couldn't understand. Retry."
		else:
			sys.stdout.write("Type your move: ")
			validMove = board.performPlayerMove(raw_input())

	#TODO: Check if check or check mate

	# UI 
	os.system("clear")
	board.drawBoard()

	# AI Move
	enemy.performMove(board)



'''

try:
    print("You said " + r.recognize(audio))    # recognize speech using Google Speech Recognition
except LookupError:                            # speech is unintelligible
    print("Could not understand audio")
'''

