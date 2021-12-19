import cv2
print(cv2.__version__)

def xCallback(val):
	global xPos
	xPos = val
	print('x', val)

def yCallback(val):
	global yPos
	yPos = val
	print('y', val)

def rCallback(val):
	global cRad
	cRad = val
	print('r', val)

def tCallback(val):
	global cThi
	cThi = val
	print('t', val)

width = 1200
height = 720
xPos = int(width/2)
yPos = int(height/2)
cRad = 25
cThi = 2
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cv2.namedWindow('trackbars')
cv2.resizeWindow('trackbars',400,160)
cv2.moveWindow('trackbars',width,0)
cv2.createTrackbar('xPos', 'trackbars', xPos, width, xCallback)
cv2.createTrackbar('yPos', 'trackbars', yPos, height, yCallback)
cv2.createTrackbar('cRad', 'trackbars', cRad, 380, rCallback)
cv2.createTrackbar('cThi', 'trackbars', cThi, 8, tCallback)

while True:

	ignore, frame = cam.read()
	cv2.circle(frame, (xPos, yPos), cRad, (0,255,255),cThi)
	cv2.imshow('Colour cam', frame)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

cam.release()