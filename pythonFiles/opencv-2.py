import cv2
import numpy as np

squareSize = 64
squares = 8
boardSize = squareSize * squares

colours = [[0,0,0],[0,0,255]]

while True:
	frame = np.zeros([boardSize,boardSize,3], dtype=np.uint8)
	colour = 1
	for y in range(0,squares):
		colour = 1 - colour
		for x in range(0,squares):
			frame[y*squareSize:(y+1)*squareSize,x*squareSize:(x+1)*squareSize] = colours[colour]
			colour = 1 - colour
	cv2.imshow('Colour cam', frame)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break
