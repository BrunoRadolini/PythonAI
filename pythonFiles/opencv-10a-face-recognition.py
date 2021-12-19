import cv2
import face_recognition as FR
from os import listdir
from os.path import isfile, join, splitext

font = cv2.FONT_HERSHEY_SIMPLEX

knownfiles = [f for f in listdir('D:/Source/Python/demoImages/known') if isfile(join('D:/Source/Python/demoImages/known', f))]

knownEncodings = []
names = []

for faceFile in knownfiles:
	faceName = splitext(faceFile)[0]
	faceFile = join('D:/Source/Python/demoImages/known', faceFile)
	faceImage = FR.load_image_file(faceFile)
	faceLocation = FR.face_locations(faceImage)[0]
	faceEncoding = FR.face_encodings(faceImage)[0]
	knownEncodings.append(faceEncoding)
	names.append(faceName)
	print('Encoded ', faceName)


unknownfiles = [f for f in listdir('D:/Source/Python/demoImages/unknown') if isfile(join('D:/Source/Python/demoImages/unknown', f))]

for unknownFile in unknownfiles:
	unknownName = splitext(faceFile)[0]
	unknownFaceFile = join('D:/Source/Python/demoImages/unknown', unknownFile)
	unknownFace = FR.load_image_file(unknownFaceFile)
	unknownFaceBGR = cv2.cvtColor(unknownFace, cv2.COLOR_RGB2BGR)
	unknownFaceLocations = FR.face_locations(unknownFace)

	unknownFaceEncodings = FR.face_encodings(unknownFace, unknownFaceLocations)

	for faceLocation, unknownFaceEncoding in zip(unknownFaceLocations, unknownFaceEncodings):
		top, right, bottom, left = faceLocation
		print(faceLocation)
		cv2.rectangle(unknownFaceBGR, (left, top), (right,bottom), (0,255,255), 2)
		name = 'Unknown person'
		matches = FR.compare_faces(knownEncodings, unknownFaceEncoding)
		print('matches', matches)
		if True in matches:
			matchIndex = matches.index(True)
			name = names[matchIndex];
			print('Matched', name)

		cv2.putText(unknownFaceBGR, name, (left + 3,top - 5), font, 1, (0,255,255),2)
	cv2.imshow('Recognise', unknownFaceBGR)
	cv2.waitKey(5000)

