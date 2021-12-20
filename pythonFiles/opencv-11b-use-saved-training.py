import cv2
import face_recognition as fr
import pickle
import os

font = cv2.FONT_HERSHEY_SIMPLEX

knownEncodings = []
names = []

with open('training_data.pk1','rb') as file:
	names = pickle.load(file)
	knownEncodings = pickle.load(file)

unknownSubfolder = 'demoImages\\unknown';
unknownFolder = os.path.join(os.getcwd(), unknownSubfolder);
unknownFiles = [f for f in os.listdir(unknownFolder) if os.path.isfile(os.path.join(unknownFolder, f))]

for faceFile in unknownFiles:
	faceName = os.path.splitext(faceFile)[0]
	faceFile = os.path.join(unknownFolder, faceFile)
	faceImage = fr.load_image_file(faceFile)
	faceBGR = cv2.cvtColor(faceImage, cv2.COLOR_RGB2BGR)
	faceLocations = fr.face_locations(faceImage)
	faceEncodings = fr.face_encodings(faceImage, faceLocations)

	for faceLocation, faceEncoding in zip(faceLocations, faceEncodings):
		top, right, bottom, left = faceLocation
		cv2.rectangle(faceBGR, (left, top), (right,bottom), (0,255,255), 2)
		name = '?'
		matches = fr.compare_faces(knownEncodings, faceEncoding)
		if True in matches:
			matchIndex = matches.index(True)
			name = names[matchIndex];

		cv2.putText(faceBGR, name, (left + 3,top - 5), font, 1, (0,255,255),2)
	cv2.imshow('Recognise', faceBGR)
	cv2.waitKey(5000)

