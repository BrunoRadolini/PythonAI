import cv2
import time
print(cv2.__version__)
width = 1200
height = 720
halfh = (int)(height/2)
halfw = (int)(width/2)
quarth = (int)(height/4)
quartw = (int)(width/4)
msg = 'IDENTIFIED AS: Brian'
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
tLast = time.time()
dT = 0
frameCount = 0
fps = 0
while True:

	dT = time.time() - tLast
	ignore, frame = cam.read()
	if dT > 0.9999:
		fps = frameCount
		tLast = time.time()
		print(fps)
		frameCount = 0

	# frame[200:600,400:800] = (255,255,255)
	cv2.rectangle(frame, (quartw,quarth), (quartw + halfw,quarth + halfh), (0,255,255), 2)
	cv2.circle(frame, (halfw,halfh), halfh, (0,0,255), 2)
	cv2.putText(frame, msg, (quartw, quarth - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 1)
	cv2.putText(frame, str(int(fps)) + ' fps', (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 1)
	cv2.namedWindow('Colour cam', flags=cv2.WINDOW_GUI_NORMAL)
	cv2.imshow('Colour cam', frame)
	frameCount = frameCount + 1
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

cam.release()