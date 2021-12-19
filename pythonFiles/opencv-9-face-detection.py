import numpy as np
import cv2
import os

print(cv2.__version__)
 
def onTrack1(val):
	global hue
	hue=val
	print('Hue',hue)
def onTrack2(val):
	global hueRange
	hueRange=val
	print('Hue Range',hueRange)
def onTrack3(val):
	global sat
	sat=val
	print('Sat',sat)
def onTrack4(val):
	global satRange
	satRange=val
	print('Sat Range',satRange)
def onTrack5(val):
	global valVal
	valVal=val
	print('Val',valVal)
def onTrack6(val):
	global valRange
	valRange=val
	print('Val Range',valRange)

def mouseClick(event, xPos, yPos, flags, params):
	global xVal
	global yVal
	global evt
	if event == cv2.EVENT_LBUTTONDOWN:
		xVal = xPos
		yVal = yPos
	evt = event

def getMin(val, min):
	if val < min:
		return min
	return val

def getMax(val, max):
	if val > max:
		return max
	return val

width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

faceCascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))
eyeCascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_eye.xml'))

cv2.namedWindow('myTracker')
cv2.moveWindow('myTracker',width,0)
cv2.namedWindow('my WEBcam')
cv2.setMouseCallback('my WEBcam', mouseClick)
 
hue=200
hueRange=20
sat=210
satRange=25
valVal=200
valRange=20
xVal = 0
yVal = 0
evt = 0
 
cv2.createTrackbar('Hue','myTracker',hue,179,onTrack1)
cv2.createTrackbar('Hue Range','myTracker',hueRange,150,onTrack2)
cv2.createTrackbar('Sat','myTracker',sat,255,onTrack3)
cv2.createTrackbar('Sat Range','myTracker',satRange,255,onTrack4)
cv2.createTrackbar('Val','myTracker',valVal,255,onTrack5)
cv2.createTrackbar('Val Range','myTracker',valRange,255,onTrack6)
 
while True:
	ignore,  frame = cam.read()

	frameGrey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(frameGrey, 1.1, 3)
	
	hueLow1 = hue - hueRange;
	hueHigh1 = hue + hueRange;
	doTwo = False

	if hueLow1 < 0:
		hueLow2 = 180 + hueLow1 
		hueLow1 = 0
		hueHigh2 = 179
		doTwo = True

	if hueHigh1 > 179:
		hueHigh2 = hueHigh1 - 180
		hueHigh1 = 179
		hueLow2 = 0
		doTwo = True

	satLow = getMin(sat - satRange, 0)
	satHigh = getMax(sat + satRange, 255)
	valLow = getMin(valVal - valRange, 0)
	valHigh = getMax(valVal + valRange, 255)

	frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
	lowerBound = np.array([hueLow1,satLow,valLow])
	upperBound = np.array([hueHigh1,satHigh,valHigh])

	myMask=cv2.inRange(frameHSV,lowerBound,upperBound)

	# if the sat range means we've wrapped round, use two masks
	if doTwo:
		lowerBound = np.array([hueLow2,satLow,valLow])
		upperBound = np.array([hueHigh2,satHigh,valHigh])
		myMask2 = cv2.inRange(frameHSV,lowerBound,upperBound)

		myMask = myMask | myMask2

	contours, junk = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#
	# cv2.drawContours(frame, contours,-1,[205,0,0], 2)

	for contour in contours:
		area = cv2.contourArea(contour)
		if area > 200:
			#cv2.drawContours(frame, [contour],0,[205,0,0], 2)
			x,y,w,h = cv2.boundingRect(contour)
			cv2.rectangle(frame, [x,y], [x+w,y+h], [255,0,0], 2)

	maxFace = 0
	for face in faces:
		x,y,w,h = face
		if w > maxFace:
			maxFace = w
	
	for face in faces:
		x,y,w,h = face
		if w == maxFace:
			cv2.rectangle(frame, [x,y], [x+w,y+h], [255,0,0], 2)
			eyes = eyeCascade.detectMultiScale(frameGrey[y:y+h,x:x+w], 1.1, 3)
			for eye in eyes:
				xe,ye,we,he = eye
				cv2.rectangle(frame, [x+xe,y+ye], [x+xe+we,y+ye+he], [0,0,255], 2)

	myObject=cv2.bitwise_and(frame,frame,mask=myMask)
	myObjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
	cv2.imshow('My Object',myObjectSmall)
	cv2.moveWindow('My Object',int(width/2),int(height))
	myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
	cv2.imshow('My Mask',myMaskSmall)
	cv2.moveWindow('My Mask',0,height)
	cv2.imshow('my WEBcam', frame)
	cv2.moveWindow('my WEBcam',1920,0)
	if evt == cv2.EVENT_LBUTTONDOWN:
		col2 = frameHSV[yVal, xVal]
		hueVal = col2[0]
		satVal = col2[1]
		valVal = col2[2]

		print('hue', col2[0], 'sat', col2[1], 'val', col2[2] )

		cv2.setTrackbarPos('Hue','myTracker',hueVal)
		cv2.setTrackbarPos('Sat','myTracker',satVal)
		cv2.setTrackbarPos('Val','myTracker',valVal)

	if cv2.waitKey(1) & 0xff ==ord('q'):
		break
cam.release()
