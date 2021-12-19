import cv2
print(cv2.__version__)
evt = 0
def mouseClick(event, xPos, yPos, flags, params):
	global evt
	global pnt
	if event == cv2.EVENT_LBUTTONDOWN:
		pnt = (xPos, yPos)
		evt = event
	if event == cv2.EVENT_LBUTTONUP:
		evt = event
 
width = 1200
height = 720
halfh = (int)(height/2)
quarth = (int)(height/4)
tqh = halfh + quarth
halfw = (int)(width/2)
quartw = (int)(width/4)
tqw = halfw + quartw
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))


while True:

	ignore, frame = cam.read()
	if evt == 1:
		cv2.circle(frame, pnt, 25, (255,0,0), 2)
	frameROI = frame[quarth+2:tqh-2,quartw+2:tqw-2]
	cv2.rectangle(frame, (quartw,quarth), (tqw,tqh), (0,255,255), 2)

	cv2.imshow('Colour cam', frame)
	cv2.imshow('ROI', frameROI)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

cam.release()