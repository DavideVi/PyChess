
from board import GameBoard

class AIPlayer:

	def __init__(self, difficulty, enemyType):
		self.movesAhead = difficulty
		self.personality = enemyType

		# 1 - Suicide Aggressive
		# 2 - Cautious Aggressive


	def performMove(self, board):
		
		(currentOffence, currentRisk, selfStrength, enemyStrength, possibleMoves) =  self.assessBoard(board)

		# TODO: Assess all moves up to self.movesAhead
		# perform the one with best score

		bestMoveIndex = -1
		bestMoveOffence = -9999
		bestMoveRisk = 9999
		bestMoveSStrength = -9999
		bestMoveEStrength = 9999

		for move in possibleMoves:
			imaginaryBoard = GameBoard()
			imaginaryBoard.loadGame(board.board)
			if imaginaryBoard.getPlayerFromPosition(move[0], move[1]) is 2:
				imaginaryBoard.movePiece(move[0], move[1], move[2], move[3])

				(newOffenceRate, newRiskRate, newSelfStrength, newEnemyStrength, newPossibleMoves) =  self.assessBoard(imaginaryBoard)

				if (self.compareMoveScoring((bestMoveOffence, bestMoveRisk, bestMoveSStrength, bestMoveEStrength), (newOffenceRate, newRiskRate, newSelfStrength, newEnemyStrength))):
					bestMoveIndex = possibleMoves.index(move)
					bestMoveOffence = newOffenceRate
					bestMoveRisk = newRiskRate
					bestMoveSStrength = newSelfStrength
					bestMoveEStrength = newEnemyStrength

		bestMove = possibleMoves[bestMoveIndex]
		board.movePiece(bestMove[0], bestMove[1], bestMove[2], bestMove[3])

	def compareMoveScoring(self, (firstOffence, firstRisk, firstSStr, firstEStr), (secondOffence, secondRisk, secondSStr, secondEStr) ):

		# Suicide Agressive 
		if self.personality is 1:
			pass

		# Cautious Agressive
		elif self.personality is 2:

			if (secondEStr < firstEStr) and (secondRisk <= firstRisk):
				return 1
			elif (secondSStr >= firstEStr) and (secondOffence >= firstOffence):
				return 1
			elif (secondEStr < firstEStr) and (secondRisk >= firstRisk) and (secondOffence > firstOffence):
				return 1
			elif (secondRisk < firstRisk):
				return 1

		return 0

	def assessBoard(self, board):
		offenceRate = 0
		riskRate = 0
		selfStrengthRate = 0
		enemyStrengthRate = 0

		possibleMoves = board.getAllValidMoves()

		for move in possibleMoves:
			piece = board.getPosition(move[2], move[3])

			if piece is not board.emptyCell:
				pieceOwner = board.getPlayerFromPiece(piece)

				if pieceOwner is 1:
					offenceRate += self.getPieceValue(piece)	
				elif pieceOwner is 2:
					riskRate += self.getPieceValue(piece)

		for column in range(0, 8):
			for row in range(0, 8):
				value = self.getPieceValue(board.getPosition(column, row))
				cellOwner = board.getPlayerFromPosition(column, row)

				if cellOwner is 1:
					enemyStrengthRate += value
				elif cellOwner is 2:
					selfStrengthRate += value

		''' 
		Foreach piece, get all valid moves, calculate which ones
		are in danger of being taken, extract values 
		'''

		return (offenceRate, riskRate, selfStrengthRate, enemyStrengthRate, possibleMoves)

	def getPieceValue(self, piece):
		if 'p' in piece:
			return 1
		elif 'r' in piece or 'h' in piece or 'b' in piece:
			return 3
		elif 'Q' in piece:
			return 6
		elif 'K' in piece: 
			return 10
		else:
			return 0