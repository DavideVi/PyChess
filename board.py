from colors import bcolors

class MoveError(Exception):

	def __init__(self, arg):
		self.msg = arg

class GameBoard:

	def __init__(self):
		self.board = []
		self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
		self.emptyCell = "-"

	def loadGame(self, externalBoard):

		for columnIndex in range(0, 8):
				row = []
				for rowIndex in range(0, 8):
					row.append(externalBoard[columnIndex][rowIndex])
				self.board.append(row)
				
	def newGame(self):

		piecesRow = ['r', 'h', 'b', 'Q', 'K', 'b', 'h', 'r']

		for columnIndex in range(0, 8):
			row = []
			for rowIndex in range(0, 8):
				if rowIndex == 0:
					row.append(bcolors.BLUE + piecesRow[columnIndex] + bcolors.ENDC)
				elif rowIndex == 1:
					row.append(bcolors.BLUE + "p" + bcolors.ENDC)
				elif rowIndex == 6:
					row.append(bcolors.RED + "p" + bcolors.ENDC)
				elif rowIndex == 7:
					row.append(bcolors.RED + piecesRow[columnIndex] + bcolors.ENDC)
				else:
					row.append(self.emptyCell)
			self.board.append(row)

	def drawBoard(self):
		
		for rowIndex in range(7, -1, -1):
			row = bcolors.BOLD + bcolors.OKGREEN + str(rowIndex + 1) + ": " + bcolors.ENDC
			for columnIndex in range(0, 8):
				row = row + self.getPosition(columnIndex, rowIndex) + " "
			print row
		print bcolors.BOLD + bcolors.OKGREEN + "   . . . . . . . ."
		print "   A B C D E F G H" + bcolors.ENDC

	def setPosition(self, column, row, piece):
		self.board[column][row] = piece

	def getPosition(self, column, row):
		return self.board[column][row]

	def performPlayerMove(self, moveString): 

		try:
			fromColumn = self.letterToNumber(moveString[0])
			fromRow = int(moveString[1]) - 1
			toColumn = self.letterToNumber(moveString[3])
			toRow = int(moveString[4]) - 1
		except (ValueError, IndexError) as e:
			print "Invalid syntax, check your move string again"
			return 0

		try:
			if self.isMoveValid(fromColumn, fromRow, toColumn, toRow):
				
				self.movePiece(fromColumn, fromRow, toColumn, toRow)
				return 1

		except MoveError as err:
			print "Invalid move: " + err.msg
			return 0

		return 0

	def movePiece(self, fromColumn, fromRow, toColumn, toRow):
		
		fromPiece = self.getPosition(fromColumn, fromRow)
		self.setPosition(fromColumn, fromRow, "-")
		self.board[fromColumn][fromRow] = self.emptyCell
		self.setPosition(toColumn, toRow, fromPiece)

	def letterToNumber(self, letter):
		return self.letters.index(letter)

	# 1 if player, 2 if computer
	def getPlayerFromPiece(self, piece):
		if piece in self.emptyCell:
			return 0	# Empty
		if "94m" in piece: 
			return 1	# User
		else:
			return 2	# Enemy AI

	def getPlayerFromPosition(self, column, row):
		return self.getPlayerFromPiece(self.getPosition(column,row))

	def isCoordinateValid(self, coordinate):
		if coordinate >= 0 and coordinate < 8:
			return 1
		return 0

	def isMoveValid(self, fromColumn, fromRow, toColumn, toRow):
	
		piece = self.getPosition(fromColumn, fromRow)
		player = self.getPlayerFromPiece(piece)

		# Making sure coordinates are valid
		if not (self.isCoordinateValid(fromColumn) and self.isCoordinateValid(fromRow) and self.isCoordinateValid(toColumn) and self.isCoordinateValid(toRow)):
			raise MoveError("Invalid coordinates provided")

		# Finding piece that's being moved 
		if self.getPlayerFromPiece(piece) is not player:
			raise MoveError("That is not your piece")

		# Destination must be empty or enemy
		if self.getPlayerFromPosition(toColumn, toRow) is player:
			raise MoveError("Destination must be empty or enemy")

		enemy = 0
		if player is 1:
			enemy = 2
		elif player is 2:
			enemy = 1

		# PAWN
		if 'p' in piece:

			# Can only move forward
			if (toRow is fromRow + 1 and player is 1) or (toRow is fromRow - 1 and player is 2):

				# Moves forward and nothing is there
				if toColumn is fromColumn and self.getPlayerFromPosition(toColumn,toRow) is 0:
					return 1
				
				# If it's attacking
				elif self.getPlayerFromPosition(toColumn, toRow) is enemy:

					# If it's going diagonally to the right or left
					if toColumn is fromColumn + 1 or toColumn is fromColumn - 1:
						return 1

			raise MoveError("Pawn can only move forward and attack diagonally")

		# ROOK
		if 'r' in piece:

			# Can only move straight
			if (toColumn is fromColumn and toRow is not fromRow) or (toColumn is not fromColumn and toRow is fromRow):
				# Can't jump
				if not self.arePiecesInBetween(fromColumn, fromRow, toColumn, toRow):
					return 1
				else:
					raise MoveError("There are pieces in between")
			else:
				raise MoveError("Rook can only move straight")

		# BISHOP
		if 'b' in piece:

			# Can only move diagonally
			if (abs(toColumn - fromColumn) is abs(toRow - fromRow)):
				# Can't jump
				if not self.arePiecesInBetween(fromColumn, fromRow, toColumn, toRow):
					return 1
				else:
					raise MoveError("There are pieces in between")
			else:
				raise MoveError("Bishop can only move diagonally")

		# PONY
		if 'h' in piece:

			# Can only move in L shape
			if toRow is fromRow + 1 or toRow is fromRow - 1:
				if toColumn is fromColumn + 2 or toColumn is fromColumn - 2:
					return 1

			if toColumn is fromColumn + 1 or toColumn is fromColumn - 1:
				if toRow is fromRow + 2 or toRow is fromRow - 2:
					return 1

			raise MoveError("Horse can only move in L shape")

		# QUEEN
		if 'Q' in piece: 
	
			# Can't jump
			if not self.arePiecesInBetween(fromColumn, fromRow, toColumn, toRow):
				return 1

			# Error is raised in the arePiecesInBetween() method 
			# because it detects wether the movement
			# wasn't either straight or diagonal

		# KING
		if 'K' in piece:

			# Only one piece distance movement
			if (toColumn - fromColumn <= 1) and (toRow - fromRow <= 1):
				# Cannot be in the vicinity of another King
				for i in range(toColumn - 1, toColumn + 2):
					for j in range(toRow - 1, toRow + 2):
						try:
							cell = self.getPosition(i, j)
							if 'K' in cell and self.getPlayerFromPiece(cell) is enemy:
								raise MoveError("Move is too close to enemy king")
						except ValueError as e:
							pass
			return 1

	# NOT IMPLEMENTED
	def arePiecesInBetween(self, fromColumn, fromRow, toColumn, toRow):

		# Check straight
		if (toColumn is fromColumn and toRow is not fromRow) or (toColumn is not fromColumn and toRow is fromRow):
			return 0
		# Check diagonally
		elif (abs(toColumn - fromColumn) is abs(toRow - fromRow)):
			return 0
		else:
			raise MoveError("Ambigous move, it's neither straight nor diagonal")

		return 0

	def getValidMovesForPosition(self, column, row):

		if self.getPlayerFromPosition(column, row) is 0:
			return []

		piece = self.getPosition(column,row)
		player = self.getPlayerFromPiece(piece)
		validMoves = []

		# PAWN
		if 'p' in piece:
			for i in range(column - 1, column + 2):
				try:
					move = []
					move.append(column)
					move.append(row)
					if player is 1:
						if (self.isMoveValid(column, row, i, row + 1)):
							move.append(i)
							move.append(row + 1)
							validMoves.append(move)
					elif player is 2:
						if (self.isMoveValid(column, row, i, row - 1)):
							move.append(i)
							move.append(row - 1)
							validMoves.append(move)
				except MoveError:
					pass

		# ROOK
		if 'r' in piece or 'Q' in piece:
			for i in range(0, 8):
				try:
					move = [] 
					move.append(column)
					move.append(row)

					if (self.isMoveValid(column, row, i, row)) and column is not i:
						move.append(i)
						move.append(row)
						validMoves.append(move)

					if (self.isMoveValid(column, row, column, i)) and row is not i:
						move.append(i)
						move.append(row)
						validMoves.append(move)
				
				except MoveError:
					pass

		# PONY
		if 'h' in piece:
			possibleMoves = [ [column, row, column + 2, row + 1],
								[column, row, column - 2, row + 1],
								[column, row, column + 2, row - 1],
								[column, row, column - 2, row - 1],
								[column, row, column + 1, row + 2],
								[column, row, column + 1, row - 2],
								[column, row, column - 1, row - 2],
								[column, row, column - 1, row + 2] ]

			for move in possibleMoves:
				try:
					if self.isMoveValid(move[0], move[1], move[2], move[3]):
						validMoves.append(move)
				except MoveError:
					pass

		# BISHOP
		if 'b' in piece or 'Q' in piece:
			for i in range(0, 8):
				try:
					if self.isMoveValid(column, row, column + i, row + i):
						validMoves.append([column, row, column + i, row + i])
				except MoveError:
					pass
				try:
					if self.isMoveValid(column, row, column + i, row - i):
						validMoves.append([column, row, column + i, row - i])
				except MoveError:
					pass
				try:
					if self.isMoveValid(column, row, column - i, row + i):
						validMoves.append([column, row, column - i, row + i])
				except MoveError:
					pass
				try:
					if self.isMoveValid(column, row, column - i, row - i):
						validMoves.append([column, row, column - i, row - i])
				except MoveError:
					pass

		# KING
		if 'K' in piece:
			for newCol in range(column - 1, column + 2):
				for newRow in range(row - 1, row + 2):
					try: 
						if self.isMoveValid(column, row, newCol, newRow):
							validMoves.append([column, row, newCol, newRow])
						except MoveError:
							pass

		return validMoves

	def getAllValidMoves(self):

		validMoves = []

		for i in range(0, 8):
			for j in range(0, 8):
				vm = self.getValidMovesForPosition(i, j)
				validMoves = validMoves + vm

		return validMoves




