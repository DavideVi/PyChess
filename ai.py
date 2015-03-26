
from board import GameBoard

class AIPlayer:

	def __init__(self, difficulty):
		self.movesAhead = difficulty


	def performMove(self, board):		
		self.performBestMove(board, 0)

	def performBestMove(self, board, currentDepth):

		(currentOffence, currentRisk, selfStrength, enemyStrength, possibleMoves) =  self.assessBoard(board)

		if currentDepth is self.movesAhead:
			return (currentOffence, currentRisk, selfStrength, enemyStrength)

		moveResults = []

		# For all possible moves
		for move in possibleMoves:
			imaginaryBoard = GameBoard()
			imaginaryBoard.loadGame(board.board)

			# If the moves are for the AI
			if imaginaryBoard.getPlayerFromPosition(move[0], move[1]) is 2:
				
				possibleResults = []

				# Perform every possible AI move
				imaginaryBoard.movePiece(move[0], move[1], move[2], move[3])

				# Check how good the situation is after each move
				(newOffenceRate, newRiskRate, newSelfStrength, newEnemyStrength, newPossibleMoves) =  self.assessBoard(imaginaryBoard)
			
				# For all possible player moves
				for newMove in newPossibleMoves:

					newImaginaryBoard = GameBoard()
					newImaginaryBoard.loadGame(imaginaryBoard.board)

					# Perform all possible player moves
					if newImaginaryBoard.getPlayerFromPosition(newMove[0], newMove[1]) is 1:

						newImaginaryBoard.movePiece(move[0], move[1], move[2], move[3])

						possibleResults.append(self.performBestMove(newImaginaryBoard, currentDepth + 1))

				if currentDepth is not 0:
					return possibleResults
				else:
					moveResults.append([move, possibleResults])

		# TODO: Go through all move results, check best outcome, perform move

		bestMoveIndex = - 1
		(bestMoveOffence, bestMoveRisk, bestMoveSStrength, bestMoveEStrength) = (-9999, 9999, -9999, 9999)

		for move in moveResults:
			(avgOff, avgRisk, avgSStr, avgEStr) = (0,0,0,0)
			for (t1, t2, t3, t4) in move[1]:
				avgOff += t1
				avgRisk += t2
				avgSStr += t3
				avgEStr += t4
			(avgOff, avgRisk, avgSStr, avgEStr) = (avgOff / len(move[1]), avgRisk / len(move[1]), avgSStr / len(move[1]), avgEStr / len(move[1]))
			
			# Update best move
			if (self.compareSituation((bestMoveOffence, bestMoveRisk, bestMoveSStrength, bestMoveEStrength), (newOffenceRate, newRiskRate, newSelfStrength, newEnemyStrength))):
				bestMoveIndex = moveResults.index(move)
				bestMoveOffence = avgOff
				bestMoveRisk = avgRisk
				bestMoveSStrength = avgSStr
				bestMoveEStrength = avgEStr

		bestMove = moveResults[bestMoveIndex][0]
		board.movePiece(bestMove[0], bestMove[1], bestMove[2], bestMove[3])

	# Returns 1 if second is better
	def compareSituation(self, (firstOffence, firstRisk, firstSStr, firstEStr), (secondOffence, secondRisk, secondSStr, secondEStr) ):

		# Second is better if improvement is greater than loss

		improvement = 0
		loss = 0

		diffOffence = secondOffence - firstOffence
		if (diffOffence > 0):
			improvement += diffOffence
		else:
			loss += abs(diffOffence)

		diffRisk = secondRisk - firstRisk
		if (diffRisk < 0):
			improvement += abs(diffRisk)
		else:
			loss += diffRisk

		diffSStr = secondSStr - firstSStr
		if (diffSStr > 0):
			improvement += diffSStr
		else:
			loss += abs(diffSStr)

		diffEStr = secondEStr - firstEStr
		if (diffEStr < 0):
			improvement += abs(diffEStr)
		else:
			loss += diffEStr

		if improvement > loss:
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