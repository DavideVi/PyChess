
import os, sys
from board import GameBoard
from ai import AIPlayer

# Main program logic
board = GameBoard()
enemy = AIPlayer(1)

board.newGame()

while 1:

	# UI 
	os.system("clear")
	board.drawBoard()

	# Player Move 
	validMove = 0
	while not validMove:
		sys.stdout.write("Type your move: ")
		validMove = board.performPlayerMove(raw_input())

	#TODO: Check if check or check mate

	# UI 
	os.system("clear")
	board.drawBoard()

	# AI Move
	enemy.performMove(board)



'''
import speech_recognition as sr
r = sr.Recognizer()

with sr.Microphone() as source:                # use the default microphone as the audio source
    audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

try:
    print("You said " + r.recognize(audio))    # recognize speech using Google Speech Recognition
except LookupError:                            # speech is unintelligible
    print("Could not understand audio")

'''
