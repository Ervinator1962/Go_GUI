import pygame, sys
from pygame.locals import *

pygame.init()



def main():
	#CONSTANTS
	WINWIDTH = 800
	WINHEIGHT = 600

	#set up display surface
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption("GO")
	board_img = pygame.image.load("go_board.png").convert()
	board_img = pygame.transform.scale(board_img, (WINWIDTH, WINHEIGHT))
	DISPLAYSURF.blit(board_img, (0, 0))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

if __name__ == '__main__':
    main()