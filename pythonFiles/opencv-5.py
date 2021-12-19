import cv2
print(cv2.__version__)
evt = 0
pntStart = (0,0)
pntEnd = (0,0)
dragging = False
haveRIO = False
killRIO = False
def mouseClick(event, xPos, yPos, flags, params):
	global evt
	global pntStart
	global pntEnd
	global dragging
	global haveRIO
	global killRIO
	if event == cv2.EVENT_LBUTTONDOWN:
		pntStart = (xPos, yPos)
		pntEnd = (xPos, yPos)
		dragging = True
		haveRIO = False
	if event == cv2.EVENT_LBUTTONUP:
		dragging = False
		left = pntStart[0]
		right = pntEnd[0]
		if left > right:
			right = pntStart[0]
			left = pntEnd[0]

		top = pntStart[1]
		bottom = pntEnd[1]
		if top > bottom:
			top = pntEnd[1]
			bottom = pntStart[1]

		pntStart = (left, top)
		pntEnd = (right, bottom)
		haveRIO = True

	if event == cv2.EVENT_MOUSEMOVE:
		if dragging == True:

			pntEnd = (xPos, yPos)
	if event == cv2.EVENT_RBUTTONDOWN:
		if haveRIO:
			killRIO = True
		dragging = False
		haveRIO = False
 
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
cv2.namedWindow('Colour cam')
cv2.setMouseCallback('Colour cam', mouseClick)

while True:

	ignore, frame = cam.read()

	if dragging == True:
		cv2.rectangle(frame, pntStart, pntEnd, (0,255,255), 2)

	cv2.imshow('Colour cam', frame)

	if haveRIO == True:
		print('Have ROI', pntStart, pntEnd)
		frameROI = frame[pntStart[1]:pntEnd[1],pntStart[0]:pntEnd[0]]
		cv2.imshow('ROI', frameROI)
	
	if killRIO == True:
		killRIO = False
		cv2.destroyWindow('ROI')
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

cam.release()