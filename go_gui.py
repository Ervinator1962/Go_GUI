import pygame, sys
from pygame.locals import *
from math import sqrt

pygame.init()

#GLOBAL CONSTANTS
FPS = 30
WINWIDTH = 650
WINHEIGHT = 650
BOARDMARGIN = 20
BOXWIDTH = 34
STONEHEIGHT = 24
STONEWIDTH = 24

#set up display surface and FPS clock
global DISPLAYSURF, FPSCLOCK
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption("GO")
FPSCLOCK = pygame.time.Clock()

#set up player stones and board
STONEWHITE = pygame.image.load("white_stone.png").convert_alpha()
STONEWHITE = pygame.transform.scale(STONEWHITE, (STONEWIDTH, STONEHEIGHT))
STONEBLACK = pygame.image.load("black_stone.png").convert_alpha()
STONEBLACK = pygame.transform.scale(STONEBLACK, (STONEWIDTH, STONEHEIGHT))
BOARDIMG = pygame.image.load("go_board.png").convert()
BOARDIMG = pygame.transform.scale(BOARDIMG, (WINWIDTH, WINHEIGHT))

def main():
	#set up cursor
	cursorX = None
	cursorY = None

	#set up players
	black = Player("black")
	white = Player("white")

	#set up game board data structure
	game_board = [["-" for y in range(19)] for x in range(19)]

	show_board(game_board)

	roundnum = 0

	while True:
		for event in pygame.event.get():
			if event.type == MOUSEMOTION:
				cursorX, cursorY = event.pos
				cursorX -= STONEWIDTH / 2
				cursorY -= STONEHEIGHT / 2
				show_board(game_board)
				if roundnum % 2 == 0:
					DISPLAYSURF.blit(STONEBLACK, (cursorX, cursorY))
				else:
					DISPLAYSURF.blit(STONEWHITE, (cursorX, cursorY))
			elif event.type == MOUSEBUTTONDOWN:
				res = None
				if roundnum % 2 == 0:
					res = place_stone(game_board, event.pos, black)
				else:
					res = place_stone(game_board, event.pos, white)
				if res == 1:	
					roundnum += 1
			elif event.type == KEYDOWN:
				if pygame.key.name(event.key) == "escape":
					roundnum += 1
					break
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		FPSCLOCK.tick(FPS)


def place_stone(board, pos, player):
	LIMITRADIUS = BOXWIDTH / 2
	posx, posy = pos
	posx -= BOARDMARGIN
	posy -= BOARDMARGIN
	#round to nearest int
	colnum = int(posx / BOXWIDTH + 0.5)
	rownum = int(posy / BOXWIDTH + 0.5)
	if colnum < 0:
		colnum = 0
	if colnum > 18:
		colnum = 18
	if rownum < 0:
		rownum = 0
	if rownum > 18:
		rownum = 18
	valid_pos = (colnum * BOXWIDTH + BOARDMARGIN, rownum * BOXWIDTH + BOARDMARGIN)
	DISTANCEFROMVALIDPOS = distance(valid_pos, pos)
	#print(DISTANCEFROMVALIDPOS)
	if DISTANCEFROMVALIDPOS < LIMITRADIUS:
		#print("testing is stone")
		if is_stone(board, (colnum, rownum)) is False:
		#print("Acceptable distance")
		#print(valid_pos)
			player.make_move(board, (colnum, rownum))
			return 1
	return 0


def show_board(board):
	DISPLAYSURF.blit(BOARDIMG, (0, 0))
	for i in range(len(board)):
		for j in range(len(board[0])):
			posx = BOARDMARGIN + BOXWIDTH * i
			posy = BOARDMARGIN + BOXWIDTH * j
			posx -= STONEWIDTH / 2
			posy -= STONEHEIGHT / 2
			if board[i][j] == "@":
				DISPLAYSURF.blit(STONEBLACK, (posx, posy))
			elif board[i][j] == "O":
				DISPLAYSURF.blit(STONEWHITE, (posx, posy))

def distance(pos1, pos2):
	return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))

def on_board(pos):
	#print("pos[0] =", pos[0])
	return 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18


def is_stone(board, pos):
	assert on_board(pos)
	#print(pos, board[pos[0]][pos[1]])
	return board[pos[0]][pos[1]] == "@" or board[pos[0]][pos[1]] == "O"


def same_colour(board, pos1, pos2):
	assert is_stone(board, pos1), "pos1 is not a valid stone"
	assert is_stone(board, pos2), "pos2 is not a valid stone"
	return board[pos1[0]][pos1[1]] == board[pos2[0]][pos2[1]]


def remove_stones(board, coordinate_list, stones_played_list):
	for (col, row) in coordinate_list:
		# indicate the current round's captured stones with '.'
		board[col][row] = "."
		stones_played_list.remove((col, row))
	return len(coordinate_list)


# remove the "."'s that indicate the last round's captured positions
def remove_capture_indicators(board):
	for i in range(19):
		for j in range(19):
			if board[i][j] == ".":
				board[i][j] = "+"


def check_liberties(board, pos, stones_played_list):
	assert on_board(pos) is True, "Position does not lie on the board"
	# print("New src = %d %d" % (col, row))
	if is_stone(board, pos) is False:
		return 0
	visited = [pos]
	has_liberties = is_free(board, pos, visited)
	# print("is_free = %s" % str(has_liberties))
	# print("visited =", visited)
	num_removed = 0
	if has_liberties is False:
		# print("is_free must be false: is_free = %s" % str(has_liberties))
		num_removed = remove_stones(board, visited, stones_played_list)
	# print("Num removed == %d" % num_removed)
	return num_removed


def is_free(board, pos, visited):
	has_liberties = False
	# print("New call")
	# print("visited = ", visited)
	pos_above = (pos[0], pos[1] - 1)
	pos_below = (pos[0], pos[1] + 1)
	pos_left = (pos[0] - 1, pos[1])
	pos_right = (pos[0] + 1, pos[1])
	positions = [pos_above, pos_below, pos_left, pos_right]
	positions_iter = list(positions)

	# remove positions not on board, i.e. all pos in list positions will be valid thereafter
	for adj_pos in positions_iter:
		if on_board(adj_pos) is False:
			positions.remove(adj_pos)
		elif is_stone(board, adj_pos) is False:
			# if pos is on the board and does not hold stone then it is a liberty
			has_liberties = True
			return has_liberties

	for adj_pos in positions:
		if same_colour(board, pos, adj_pos) and adj_pos not in visited:
			visited.append(adj_pos)
			has_liberties = is_free(board, adj_pos, visited)
			if has_liberties is True:
				break

	return has_liberties


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

	#inputs: board is a 2-d square array of size 19, pos is a tuple of coordinates
	def make_move(self, board, pos):
		col, row = pos
		board[col][row] = self.symbol
		#print(self.symbol)
		#create iterable list to scan through
		white_stones_played_iter = list(Player.white_stones_played)
		black_stones_played_iter = list(Player.black_stones_played)

		if self.colour == "black":
			Player.black_stones_played.append((col, row))
			Player.black_stones_left -= 1
			# print("Checking white liberties")
			for pos in white_stones_played_iter:
				Player.black_num_stones_capt += check_liberties(board, pos, Player.white_stones_played)
			# print("Checking black liberties")
			for pos in black_stones_played_iter:
				Player.white_num_stones_capt += check_liberties(board, pos, Player.black_stones_played)
		else:
			Player.white_stones_played.append((col, row))
			Player.white_stones_left -= 1

			# print("Checking black liberties")
			for pos in black_stones_played_iter:
				Player.white_num_stones_capt += check_liberties(board, pos, Player.black_stones_played)
			# print("Checking white liberties")
			for pos in white_stones_played_iter:
				Player.black_num_stones_capt += check_liberties(board, pos, Player.white_stones_played)

if __name__ == '__main__':
	main()