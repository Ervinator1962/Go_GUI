import pygame, sys
from pygame.locals import *
from math import sqrt

pygame.init()

def main():
	#CONSTANTS
	WINWIDTH = 650
	WINHEIGHT = 650
	STONEHEIGHT = 24
	STONEWIDTH = 24
	STONEWHITEX = None
	STONEWHITEY = None
	STONEWHITE = pygame.image.load("white_stone.png")
	STONEWHITE = pygame.transform.scale(STONEWHITE, (STONEWIDTH, STONEHEIGHT))

	#set up display surface
	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption("GO")
	board_img = pygame.image.load("go_board.png").convert()
	board_img = pygame.transform.scale(board_img, (WINWIDTH, WINHEIGHT))
	DISPLAYSURF.blit(board_img, (0, 0))

	while True:
		for event in pygame.event.get():
			if event.type == MOUSEMOTION:
				STONEWHITEX, STONEWHITEY = event.pos
				STONEWHITEX -= STONEWIDTH / 2
				STONEWHITEY -= STONEHEIGHT / 2
				DISPLAYSURF.blit(board_img, (0, 0))
				#DISPLAYSURF.blit(STONEWHITE, (STONEWHITEX, STONEWHITEY))
			elif event.type == MOUSEBUTTONDOWN:
				place_stone(event.pos)
				#print(event.pos)
				pass
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

# extra row for x-axis coordinates
game_board = [["+" for x in range(20)] for y in range(20)]
for i in range(len(game_board) - 1):
	game_board[i][19] = i
for i in range(len(game_board[0]) - 1):
	game_board[19][i] = i
game_board[19][19] = ""

def place_stone(pos):
	# TODO: MAKE STONEWIDTH AND STONEHEIGHT GLOBAL
	STONEHEIGHT = 24
	STONEWIDTH = 24
	BOARDMARGIN = 20
	BOXWIDTH = 35
	LIMITRADIUS = BOXWIDTH / 2
	posx, posy = pos
	posx -= BOARDMARGIN
	posy -= BOARDMARGIN
	if posx < 0:
		posx = 0
	if posy < 0:
		posy = 0
	#round to nearest int
	rownum = int(posy / BOXWIDTH + 0.5)
	colnum = int(posx / BOXWIDTH + 0.5)
	valid_pos = (colnum * BOXWIDTH + BOARDMARGIN, rownum * BOXWIDTH + BOARDMARGIN)
	DISTANCEFROMVALIDPOS = sqrt(pow(valid_pos[0] - pos[0], 2) + pow(valid_pos[1] - pos[1], 2)) 
	print(DISTANCEFROMVALIDPOS)
	if DISTANCEFROMVALIDPOS < LIMITRADIUS:
		#print("Acceptable distance")
		newstone = pygame.image.load("white_stone.png")
		newstone = pygame.transform.scale(newstone, (STONEWIDTH, STONEHEIGHT))
		DISPLAYSURF.blit(newstone, valid_pos)
	else:
		pass
		#print("Invalid distance")
	return (rownum, colnum)
	#print("pos =", valid_pos)

def print_board(board):
	print("\n\n\n")
	for i in range(len(board)):
		for j in range(len(board[0])):
			print("{:<4}".format(board[i][j]), end="")
		print("\n")


def on_board(pos):
	return 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18


def is_stone(pos, board):
	assert on_board(pos)
	return board[pos[0]][pos[1]] == "@" or board[pos[0]][pos[1]] == "O"


def same_colour(pos1, pos2, board):
	assert is_stone(pos1, board), "pos1 is not a valid stone"
	assert is_stone(pos2, board), "pos2 is not a valid stone"
	return board[pos1[0]][pos1[1]] == board[pos2[0]][pos2[1]]


def remove_stones(coordinate_list, board, stones_played_list):
	# TODO: Check to see if stones_played_list is working properly
	for (row, col) in coordinate_list:
		# indicate the current round's captured stones with '.'
		board[row][col] = "."
		stones_played_list.remove((row, col))
	return len(coordinate_list)


# remove the "."'s that indicate the last round's captured positions
def remove_capture_indicators(board):
	for i in range(19):
		for j in range(19):
			if board[i][j] == ".":
				board[i][j] = "+"


# TODO: Check stones_played_list
def check_liberties(pos, board, stones_played_list):
	assert on_board(pos) is True, "Position does not lie on the board"
	# print("New src = %d %d" % (row, col))
	if is_stone(pos, board) is False:
		return 0
	visited = [pos]
	has_liberties = is_free(pos, board, visited)
	# print("is_free = %s" % str(has_liberties))
	# print("visited =", visited)
	num_removed = 0
	if has_liberties is False:
		# print("is_free must be false: is_free = %s" % str(has_liberties))
		num_removed = remove_stones(visited, board, stones_played_list)
	# print("Num removed == %d" % num_removed)
	return num_removed


def is_free(pos, board, visited):
	has_liberties = False
	# print("New call")
	# print("visited = ", visited)
	pos_above = (pos[0] - 1, pos[1])
	pos_below = (pos[0] + 1, pos[1])
	pos_left = (pos[0], pos[1] - 1)
	pos_right = (pos[0], pos[1] + 1)
	positions = [pos_above, pos_below, pos_left, pos_right]
	positions_iter = list(positions)

	# remove positions not on board, i.e. all pos in list positions will be valid thereafter
	for adj_pos in positions_iter:
		if on_board(adj_pos) is False:
			positions.remove(adj_pos)
		elif is_stone(adj_pos, board) is False:
			# if pos is on the board and does not hold stone then it is a liberty
			has_liberties = True
			return has_liberties

	for adj_pos in positions:
		if same_colour(pos, adj_pos, board) and adj_pos not in visited:
			visited.append(adj_pos)
			# input("pos: %d %d" % (row - 1, col))
			has_liberties = is_free(adj_pos, board, visited)
			if has_liberties is True:
				break

	return has_liberties


def num_strings(text):
	num_spaces = 0
	for letter in text:
		if letter == " ":
			num_spaces += 1

	return num_spaces + 1


# noinspection PyBroadException
def is_int(string):
	try:
		int(string)
	except:
		return False
	return True


def is_valid_coordinates(text):
	if num_strings(text) != 2:
		return False

	strings = text.split()
	for string in strings:
		if is_int(string) is False:
			return False

	return True


class Player(object):
	# TODO: Work out a way to count and change the variables between black and white so they don't have to be
	# TODO: class variables.
	white_stones_played = []
	black_stones_played = []
	white_stones_left = 180
	black_stones_left = 181
	white_num_stones_capt = 0
	black_num_stones_capt = 0

	def __init__(self, colour):
		self.colour = colour
		if self.colour == "black":
			self.symbol = "@"
		else:
			self.symbol = "O"

	def show_num_captured(self):
		if self.colour == "black":
			print(Player.black_num_stones_capt)
		else:
			print(Player.white_num_stones_capt)

	def make_move(self, board):
		user_input = input("Ok, %s, place your stone.\n" % self.colour)
		while True:
			if user_input.lower().find("pass") >= 0:
				return
			elif is_valid_coordinates(user_input):
				coordinates = user_input.split()
				# print("user_input = \"%s\"" % user_input)
				# print("coordinates = %s\n" % coordinates)
				row = int(coordinates[0])
				col = int(coordinates[1])
				if row > 18 or row < 0 or col > 18 or col < 0:
					user_input = input("Invalid position, try again.\n")
					continue
				elif is_stone((row, col), board) is True:
					user_input = input("Position occupied, try again.\n")
					continue
				else:
					break
			else:
				user_input = input("Please input 'pass' or TWO numbers: row col\n")

		board[row][col] = self.symbol
		white_stones_played_iter = list(Player.white_stones_played)
		black_stones_played_iter = list(Player.black_stones_played)
		if self.colour == "black":
			Player.black_stones_played.append((row, col))
			Player.black_stones_left -= 1
			# print("Checking white liberties")
			for pos in white_stones_played_iter:
				Player.black_num_stones_capt += check_liberties(pos, board, Player.white_stones_played)
			# print("Checking black liberties")
			for pos in black_stones_played_iter:
				Player.white_num_stones_capt += check_liberties(pos, board, Player.black_stones_played)
		else:
			Player.white_stones_played.append((row, col))
			Player.white_stones_left -= 1

			# print("Checking black liberties")
			for pos in black_stones_played_iter:
				Player.white_num_stones_capt += check_liberties(pos, board, Player.black_stones_played)
			# print("Checking white liberties")
			for pos in white_stones_played_iter:
				Player.black_num_stones_capt += check_liberties(pos, board, Player.white_stones_played)

"""
black = Player("black")
white = Player("white")

print("\n\n\n")
print("Hello! Welcome to Go! Please start now.")

while black.black_stones_left > 0 and white.white_stones_left > 0:
	if __debug__:
		print_board(game_board)
	remove_capture_indicators(game_board)
	print("Player 1's turn. (%d stones left, %d stone(s) captured)" % (black.black_stones_left, black.black_num_stones_capt))
	black.make_move(game_board)
	if __debug__:
		print_board(game_board)
	remove_capture_indicators(game_board)
	print("Player 2's turn. (%d stones left, %d stone(s) captured)" % (white.white_stones_left, white.white_num_stones_capt))
	white.make_move(game_board)


while black.black_stones_left > 0:
	if __debug__:
		print_board(game_board)
	remove_capture_indicators(game_board)
	print("Player 1's turn. (%d stones left, %d stone(s) captured)" % (black.black_stones_left, black.black_num_stones_capt))
	black.make_move(game_board)


while white.white_stones_left > 0:
	if __debug__:
		print_board(game_board)
	remove_capture_indicators(game_board)
	print("Player 2's turn. (%d stones left, %d stone(s) captured)" % (white.white_stones_left, white.white_num_stones_capt))
	white.make_move(game_board)


if __debug__:
	print_board(game_board)

if black.black_num_stones_capt == white.white_num_stones_capt:
	print("Congratulations, you have tied")
elif black.black_num_stones_capt > white.white_num_stones_capt:
	print("Congratulations %s, you won!" % "PLayer 1")
else:
	print("Congratulations %s, you won!" % "Player 2")

print("Game over!")
"""

if __name__ == '__main__':
	main()